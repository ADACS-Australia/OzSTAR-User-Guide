# Filesystems and Storage

Choose the right storage location on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor for your scripts, active job data, temporary scratch files, and shared datasets. All clusters share `/home`, `/fred`, `/aphid/scratch-3month`, and `/datasets`, while `$JOBFS` is local to each compute node.

| Path | Backed up? | Quota / Retention | Best for |
|---|---|---|---|
| `/home/<username>` | Yes | 20 GiB, 200,000 files per user (fixed) | Source code, job scripts, config files, small critical inputs |
| `/fred/<project>` | **No** | 10 TiB, 1,000,000 files per project (default) | Active job inputs and outputs, large datasets, Conda environments |
| `/aphid/scratch-3month/<username>` | **No** | No fixed quota; **90-day** last-access expiry | Temporary, I/O-intensive scratch workloads |
| `$JOBFS` | **No** | Small default; set with `--tmp=<size>`, deleted when job ends | Fast local SSD/NVMe I/O for jobs reading or writing many small files |
| `/datasets` | Managed (read-only) | Shared read-only host storage | Pre-staged scientific datasets (for example, Gaia, LIGO, LSST) |

## Checking your quota

Run `quota` on any login or compute node to see live disk-block and file-count usage against your limits on `/home` and every `/fred/<project>` you belong to:

```bash
quota
```

:::{note}
Because `/home`, `/fred`, and `/aphid/scratch-3month` use [transparent compression](#transparent-compression), quotas count only compressed blocks actually stored on disk. It is common to store more uncompressed data than your quota limit while remaining under quota.
:::

## Home directory

`/home/<username>` is a cluster-wide Lustre + ZFS filesystem that is **backed up**.

- **Quota:** **20 GiB** of disk blocks and **200,000 files** per user. This limit is fixed and cannot be increased so that backups remain feasible.
- **Intended use:** Small source files, job submission scripts, configuration files, and small important inputs.
- **Avoid:** Storing large datasets, job outputs, or Conda environments in `/home`. Move Conda environments to `/fred/<project>` (see [Conda and home directory quota](../software/python.md#conda-and-home-directory-quota)).

## Project storage

`/fred/<project>` is the primary high-throughput cluster-wide Lustre + ZFS storage filesystem, designed for large data files and active compute job I/O.

:::{warning}
`/fred` is **not backed up** and is unsuitable for long-term archival storage. Accidentally deleted files cannot be recovered, and data loss from hardware failure — while unlikely — remains possible. You are responsible for backing up important data to an external location (see [Policies](../1-getting_started/Policies.rst)).
:::

- **Default quota:** **10 TiB** of disk blocks and **1,000,000 files** per project. If your project requires additional storage, email `hpc-support@swin.edu.au` (see [User Support](../help/support.md)).
- **Directory layout:** Project leaders typically create per-member subdirectories inside the project area (for example, `/fred/<project>/<username>`). If you belong to multiple projects, you can access each project's `/fred/<project>` directory.
- **Intended use:** Most batch jobs should read inputs from and write outputs to `/fred/<project>`.

## Three-month scratch

`/aphid/scratch-3month/<username>` is a cluster-wide scratch filesystem designed for temporary, I/O-intensive workloads.

:::{warning}
`/aphid` is **not backed up**, enforces a **90-day file expiry policy**, and is built from repurposed NT hardware. Although configured for resilience, its long-term reliability may be lower than `/home` or `/fred`.
:::

The recommended workflow is to run I/O-intensive jobs in `/aphid/scratch-3month/<username>`, copy valuable results to `/home` (backed up) or `/fred` (not backed up), and delete unnecessary intermediate files or allow them to expire.

`/aphid/scratch-3month` does not enforce a fixed quota, though limits may be introduced if storage usage becomes imbalanced or inconsistent with temporary scratch use.

### Scratch file expiry and reports

Files under `/aphid/scratch-3month/<username>` expire **90 days** after their last access time. You are responsible for copying important outputs to `/home` or `/fred` before they expire.

:::{warning}
It is policy that users must not modify file timestamps or otherwise attempt to circumvent the 90-day (three-month) retention policy. Retaining unnecessary data on the repurposed `/aphid` hardware increases the risk of data loss and degrades filesystem reliability for all users.
:::

A summary of files approaching expiry is shown in the welcome message when you log in. You can also inspect recent nightly expiry reports from the command line. Reports are generated only when you have files in `/aphid/scratch-3month/<username>`.

View your latest expiry report:

```bash
scratch-report
```

List available recent reports:

```bash
scratch-report list
```

Inspect a specific report:

```bash
scratch-report show <report_file>
```

## Local job scratch

Each compute node on NT, OzSTAR, and Trevor has fast local SSD/NVMe storage (formatted as XFS) exposed inside batch and interactive jobs via the `$JOBFS` environment variable.

:::{warning}
`$JOBFS` is created automatically before your job starts and permanently deleted when your job ends (including on timeout or failure). Copy any outputs you need back to `/fred/<project>` before your job exits.
:::

- **Requesting space:** Omitting `--tmp` allocates only a minimal default `$JOBFS` space; request what your job needs with `#SBATCH --tmp=<size>` (for example, `#SBATCH --tmp=20G`). Do not use `--gres=tmp:...`; Slurm rejects it.
- **Typical workflow:** Copy a tarball from `/fred/<project>` to `$JOBFS`, unpack it, process many small files locally at high IOPS, pack the results into a tarball, and move the archive back to `/fred/<project>`.

See [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) for `--tmp` sizing details and [Optimising Lustre I/O](optimising-lustre.md) for complete staging scripts.

## Transparent compression

`/home`, `/fred`, and `/aphid/scratch-3month` have transparent ZFS compression enabled. Every file — regardless of type — is compressed automatically when written to disk and uncompressed automatically when read.

For example, checking a highly compressible ASCII input file with `ls -ls`:

```bash
ls -ls input
```

```text
1 -rw-r--r-- 1 <username> <project> 39894 Mar  5 17:36 input
```

The file is ~40 KB in apparent size, yet occupies less than 1 KB on disk (the first column).

Checking a moderately compressible binary output file with `ls -lsh`:

```bash
ls -lsh output
```

```text
7.8M -rw-rw-r-- 1 <username> <project> 33M Feb 20 18:25 output
```

This 33 MB file uses only 7.8 MB of disk blocks against your quota.

:::{note}
You do not save disk space on `/home`, `/fred`, or `/aphid/scratch-3month` by running `gzip` or `bzip2` on files stored there — double compression is unnecessary and can even make files slightly larger. However, compressing files before transferring them over the network to external machines is still worthwhile to reduce transfer time and remote storage usage.
:::

## Shared datasets

`/datasets` hosts large, commonly used scientific datasets (such as Gaia, LIGO, and LSST) mounted read-only across the clusters. Jobs can read directly from `/datasets`, avoiding lengthy external transfers and conserving your project's `/fred` quota.

List hosted datasets from any node:

```bash
ls /datasets
```

If you would like a widely used scientific dataset hosted in `/datasets`, email `hpc-support@swin.edu.au` (see [User Support](../help/support.md)).

## Next steps

- [Transferring Files](file-transfer.md) — move data onto and off the clusters via the data-mover nodes.
- [Optimising Lustre I/O](optimising-lustre.md) — avoid IOPS bottlenecks with large I/O, SquashFS, and `$JOBFS`.
- [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) — set `--tmp` and other Slurm job resources.
- [Policies](../1-getting_started/Policies.rst) — formal data storage, security, and retention rules.
