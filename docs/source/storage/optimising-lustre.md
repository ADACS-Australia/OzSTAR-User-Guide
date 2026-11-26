# Optimising Lustre I/O

Structure file reads and writes on Ngarrgu Tindebeek (NT) and OzSTAR to achieve high throughput on the shared Lustre filesystems (`/home`, `/fred`, and `/aphid/scratch-3month`) without degrading performance for other users.

## Use large sequential reads and writes

Lustre delivers its best throughput on large sequential transfers and large files rather than many small files.

- **Transfer size:** Reads and writes **larger than 4 MB** are ideal, and **10 MB or larger** is best. Avoid small reads and writes (under 100 kB), especially **4 kB random writes**, which cause heavy disk seeking and poor throughput on the underlying RAID and ZFS arrays. (Small sequential reads occasionally benefit from block-device, Lustre, or ZFS read-ahead, but this should not be relied on.)
- **File size:** Optimal cluster file sizes are between **10 MB and 100 GB**.
- **Parallel codes and checkpoints:** Read or write one large `O(GB)` file per process — or, at high process counts, one large file per node. This distributes I/O across the Object Storage Targets (OSTs) in `/fred` for high aggregate bandwidth (see [Project storage](filesystems.md#project-storage), before speed-ups from transparent filesystem compression).
- **Do not configure Lustre striping:** Each individual OST in `/fred` is backed by fast ZFS storage and can sustain high throughput on its own, so Lustre striping provides no advantage.

## Avoid high IOPS and metadata storms

**IOPS** (Input/Output Operations per Second) measures metadata and file operations such as `open()`, `close()`, `seek()`, `read()`, `write()`, and `stat()`.

High IOPS and small files go hand in hand. When files are smaller than 10 MB, I/O time is easily dominated by `open()`/`close()` metadata calls rather than actual data transfer.

Avoid these patterns on Lustre:

- **Directories of tens of thousands of small files:** For example, reading or creating 100,000 files under 8 kB each on `/fred` or `/home` performs poorly on any shared parallel filesystem.
- **Tight `open()`/`close()` loops:** Repeatedly opening and closing files inside an inner loop saturates the shared Lustre Metadata Servers (MDSs). Because the MDS is shared across all users and has finite metadata capacity, metadata storms slow down both your job and the entire cluster.

## Avoid multi-node write lock bouncing

:::{warning}
Do **not** append to the same shared file (such as a shared log file) from multiple compute nodes at the same time.
:::

When multiple nodes append concurrently to one POSIX file, the resulting line order is undefined while Lustre must repeatedly bounce write locks between every appending node to maintain POSIX consistency. This stalls all writing processes and places heavy load on the MDS.

**Rule of thumb:** Write one output or log file per node (or per MPI rank). If multiple nodes must write into a single shared file, use a parallel I/O library such as MPI-IO.

## Reading many small files

If your workflow must read many small files (such as Python environments or machine-learning datasets), package them into a single read-only [SquashFS](https://docs.kernel.org/filesystems/squashfs.html) image. Lustre then sees one large file instead of thousands of small inodes.

### Option 1: Containerise code and data with Apptainer

Packaging your software — and optionally your dataset — into an Apptainer `.sif` image (which is stored as a read-only SquashFS file) eliminates small-file IOPS on Lustre. See [Containers (Apptainer)](../software/apptainer.md) to build and run `.sif` containers, or bind-mount a separate `.sqfs` data image into an existing container (see [Binding directories and images](../software/apptainer.md#binding-directories-and-images)).

:::{warning}
Running Apptainer in **sandbox mode** unpacks the container into an ordinary directory on the host filesystem and completely negates all Lustre I/O benefits. Use sandbox mode only for development and testing, never for production runs.
:::

### Option 2: Create and mount a SquashFS data image

If you need to pack only data (not code), create a SquashFS archive with `mksquashfs` and mount it read-only inside your job using [Linux namespaces](https://www.redhat.com/en/blog/7-linux-namespaces) and `squashfuse`. This is often faster than unpacking a tarball into `$JOBFS` at job start.

1. Pack your directory of small files into a single SquashFS file:

   ```bash
   mksquashfs training-data/ data.sqfs
   ```

2. Mount `data.sqfs` inside your batch script with `unshare` and `squashfuse`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=squashfs-read
   #SBATCH --nodes=1
   #SBATCH --ntasks-per-node=1
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=4G
   #SBATCH --time=0-00:30:00

   # Load any required modules here

   mkdir -p "$JOBFS/data"

   unshare --user --pid --map-root-user --fork --mount-proc bash <<'EOF'
   squashfuse /fred/<project>/data.sqfs "$JOBFS/data"
   ls "$JOBFS/data"
   # Run your code reading from "$JOBFS/data"
   EOF
   ```

You can shorten the `unshare` flags to `unshare -Uprf --mount-proc bash`.

## Writing many small files

If your job must write many small files, stage them on fast local compute-node storage (`$JOBFS`), archive them into a single tarball at the end of the job, and move the tarball to `/fred/<project>/` (see [Local job scratch](filesystems.md#local-job-scratch)).

:::{warning}
`$JOBFS` is deleted automatically as soon as your job finishes or times out. Request enough `--tmp` space to hold both the uncompressed output files and the final archive, and allow enough wall time to pack and move the tarball to `/fred/<project>/`.
:::

```bash
#!/bin/bash
#SBATCH --job-name=jobfs-write
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=0-00:30:00
#SBATCH --tmp=20G

# Load any required modules here

mkdir -p "$JOBFS/data"

# Direct your code to write small files to $JOBFS/data
./mycode --output_dir="$JOBFS/data"

# Pack the output into one archive and move it to /fred
tar -cf "$JOBFS/data.tar" -C "$JOBFS" data
mv "$JOBFS/data.tar" "/fred/<project>/<username>/"
```

Using `tar -cf` avoids double-compressing data stored on `/fred`, which already uses [transparent compression](filesystems.md#transparent-compression). Use `tar -czf` if you plan to copy the archive off the cluster.

## Next steps

- [Filesystems and Storage](filesystems.md) — compare `/home`, `/fred`, `/aphid/scratch-3month`, and `$JOBFS`.
- [Containers (Apptainer)](../software/apptainer.md) — package Python and scientific software into single-file `.sif` images.
- [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) — configure `--tmp`, memory, and wall time for your jobs.
