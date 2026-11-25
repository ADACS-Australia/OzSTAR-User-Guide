# Containers (Apptainer)

Package custom software stacks, 32-bit applications, or data-heavy scientific workflows into single-file, reproducible Apptainer containers on Ngarrgu Tindebeek (NT) and OzSTAR.

## Before you start

Load the `apptainer` module (`singularity` is a global alias for `apptainer`):

```bash
module load apptainer
```

For comprehensive upstream documentation, see the [official Apptainer user guide](https://apptainer.org/docs/user/main/).

## Building a container from a definition file

Apptainer `.sif` images are built from plain-text definition (`.def`) files, analogous to Dockerfiles.

The example below packages a Conda environment starting from the [Micromamba Docker image](https://hub.docker.com/r/mambaorg/micromamba). For a `pip`-based Python container example, see [Containerised Python with Apptainer](python.md#containerised-python-with-apptainer); for additional recipes (Astrometry.net, HEASoft, IRAF, SExtractor, and more), see [Apptainer Example Recipes](apptainer-examples.md).

:::{note}
Replace `<tag>` and `<version>` with a current Micromamba Docker image tag and Python version for your workflow (pinning explicit tags keeps builds reproducible). Check the host GLIBC version (`ldd --version`) if a build encounters fakeroot errors (see [Fakeroot and GLIBC compatibility](#fakeroot-and-glibc-compatibility)).
:::

Create a definition file named `bilby.def`:

```singularity
BootStrap: docker
From: mambaorg/micromamba:<tag>

%post
    micromamba install -qy -n base -c conda-forge python=<version> bilby gwpy python-lalsimulation
```

Build the `.sif` image:

```bash
apptainer build bilby.sif bilby.def
```

This downloads the base Docker image, converts it to `.sif` format, installs the specified packages into the container's base Conda environment, and saves the result as `bilby.sif`.

Run a Python script inside the container:

```bash
apptainer run bilby.sif python my-script.py
```

You can also invoke the `.sif` file directly (`./bilby.sif python my-script.py`), or run `./bilby.sif my-script.py` if `my-script.py` is executable and starts with `#!/usr/bin/env python`.

To expose additional host directories, pass `-B`:

```bash
apptainer run -B /fred/<project>,<path/to/other/dir> bilby.sif python my-script.py
```

:::{note}
Everything after the `.sif` filename runs inside the container. Because Apptainer bind-mounts `$PWD` by default, a script in your current working directory is accessible automatically; files located elsewhere on `/fred` require an explicit `-B` bind mount.
:::

## Binding directories and images

By default, host directories outside standard bind paths are hidden inside a container. Use `-B` (`--bind`) to mount host directories into the container at runtime.

Bind `/fred/<project>` at the same path inside the container:

```bash
apptainer run -B /fred/<project> mycontainer.sif
```

Bind `/fred/<project>` to a different path (`/project`) inside the container:

```bash
apptainer run -B /fred/<project>:/project mycontainer.sif
```

Bind multiple paths (comma-separated):

```bash
apptainer run -B /fred/<project>,<path/to/other/dir> mycontainer.sif
```

Apptainer automatically bind-mounts these host paths by default (see [Apptainer bind paths and mounts](https://apptainer.org/docs/user/main/bind_paths_and_mounts.html)):

- `$HOME` and `$PWD`
- `/sys`, `/proc`, `/dev`, `/tmp`, and `/var/tmp`
- `/etc/resolv.conf`, `/etc/passwd`, `/etc/localtime`, and `/etc/hosts`

:::{note}
Because Apptainer mounts `$PWD` automatically (creating the directory inside the container if it does not exist), container behaviour can vary depending on which working directory you launch `apptainer run` from.
:::

You can also [bind external filesystem images](https://apptainer.org/docs/user/main/bind_paths_and_mounts.html#image-mounts) such as a read-only SquashFS data archive (`.sqfs`) directly into a container — ideal for reading datasets of many small files without straining Lustre (see [Optimising Lustre I/O](../storage/optimising-lustre.md)):

```bash
apptainer run -B data.sqfs:/data:image-src=/ app.sif
```

This mounts the root (`/`) of `data.sqfs` at `/data` inside the container, creating `/data` automatically if it does not exist.

## Using GPUs with a container

In a batch or interactive job with NVIDIA GPUs allocated, pass `--nv` to bind the host GPU devices and drivers into your container:

```bash
apptainer run --nv mycontainer.sif
```

Your container may still need its own CUDA runtime libraries matching your application's requirements.

## Staging containers to `$JOBFS`

For I/O-intensive jobs or jobs that invoke a container repeatedly, copying your `.sif` image to fast local compute-node storage (`$JOBFS`) often improves performance (see [Filesystems and Storage](../storage/filesystems.md) and [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md)).

:::{warning}
Request `--tmp` strictly larger than your `.sif` image (plus any temporary files your job writes to `$JOBFS`). If `$JOBFS` runs out of space, your job will crash.
:::

```bash
#!/bin/bash
#SBATCH --job-name=apptainer-jobfs
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=0-01:00:00
#SBATCH --tmp=10G

module load apptainer

cp /fred/<project>/container.sif "$JOBFS/container.sif"
apptainer run -B /fred/<project> "$JOBFS/container.sif" <command>
```

## Running 32-bit applications

NT and OzSTAR do not provide 32-bit system libraries. To build or run legacy 32-bit applications, start from an Enterprise Linux container image (such as `almalinux:<major_version>` or `rockylinux:<major_version>`) matching the host OS major version (`cat /etc/os-release`) and GLIBC, and install the required `.i686` libraries inside the container.

Illustrative `32bit.def` recipe:

```singularity
BootStrap: docker
From: almalinux:<major_version>

%post
    dnf update -y
    dnf install -y csh gcc make flex libXmu-devel libX11-devel \
        glibc.i686 zlib-devel.i686 libcurl-devel.i686 \
        expat-devel.i686 readline-devel.i686
    dnf clean all
```

Build and run your 32-bit binary:

```bash
apptainer build 32bit.sif 32bit.def
apptainer run -B /fred/<project> 32bit.sif <path/to/32bit-binary>
```

For a complete 32-bit IRAF container recipe, see [Apptainer Example Recipes](apptainer-examples.md).

## Using MPI with a container

Read the [Apptainer MPI documentation](https://apptainer.org/docs/user/main/mpi.html) before running containerised MPI jobs.

Use the [hybrid MPI model](https://apptainer.org/docs/user/main/mpi.html#hybrid-model): invoke the host `mpirun` launcher outside the container with a compatible MPI library inside the container. Both must use the **same MPI implementation** and the **same major version**.

NT and OzSTAR provide and support **OpenMPI** only. Install OpenMPI plus the interconnect transport packages inside your container's `%post` section:

::::{tab-set}

:::{tab-item} RHEL / AlmaLinux / Rocky Linux

```bash
dnf install -y openmpi openmpi-devel ucx ucx-cma ucx-ib ucx-rdmacm
dnf group install -y "InfiniBand Support"
```

:::

:::{tab-item} Debian / Ubuntu

```bash
apt-get update
apt-get install -y openmpi-bin libopenmpi-dev infiniband-diags ucx-utils
```

:::

::::

If your container includes a `conda-forge` environment, install the OS OpenMPI packages above and then add the external OpenMPI dummy package (see [Using cluster MPI libraries with Conda](python.md#using-cluster-mpi-libraries-with-conda)) so Conda packages link against the container's OpenMPI libraries.

Discover available host OpenMPI modules on your target cluster:

```bash
module spider openmpi
```

Load a host OpenMPI module in the **same major version** as the container's OpenMPI — at least as recent in minor/patch version (for example, if the container has OpenMPI `4.1.x`, load a host `openmpi/4.1.y` where `y >= x` and `< 5.0.0`). Launch your containerised MPI job with [`--sharens`](https://apptainer.org/docs/user/main/mpi.html#using-sharens-mode):

```bash
module load apptainer
module load gcc/<gcc_version> openmpi/<openmpi_version>
mpirun -n 4 apptainer run --sharens -B /fred/<project> mycontainer.sif <path/to/container/application>
```

Passing `--sharens` ensures all MPI processes on the same node share one user namespace so they can use fast intra-node communication transports.

:::{warning}
High-speed MPI interconnect fabrics differ between clusters: **Ngarrgu Tindebeek (NT)** uses **InfiniBand (Mellanox)** on Milan nodes, whereas **OzSTAR** uses **Omni-Path (OPA)** on Skylake nodes. Each fabric requires different OpenMPI transports. Although cluster environment variables normally select the correct transport automatically, mismatches can still arise depending on the transports compiled into your container's OpenMPI. If you experience errors or poor MPI performance, email `hpc-support@swin.edu.au` (see [User Support](../help/support.md)).
:::

### MPI performance: container versus native

When configured with the hybrid model, MPI container overhead on Swinburne HPC is typically negligible. The [OSU MPI benchmarks](https://mvapich.cse.ohio-state.edu/benchmarks/) below compare a Debian 12 container (GCC 12.2.0, OpenMPI 4.1.4) against native bare-metal execution using the same compiler and OpenMPI version.

:::{figure} ../_static/OSU-MPI-Bandwidth.png
:alt: Grouped bar chart of the OSU MPI Bandwidth Test across 2 nodes and 2 MPI ranks comparing Container and Native performance from 1 KiB to 4 MiB message sizes. Both achieve nearly identical bandwidth, rising from about 30 Gbps at 1 KiB to roughly 196 Gbps at 512 KiB through 4 MiB.
:align: center

OSU MPI Bandwidth benchmark (2 nodes, 2 MPI ranks): containerised versus native OpenMPI.
:::

:::{figure} ../_static/OSU-MPI-Latency.png
:alt: Grouped bar chart of the OSU MPI Latency Test across 2 nodes and 2 MPI ranks comparing Container and Native latency in microseconds from 1 KiB to 4 MiB message sizes. Both show nearly identical latency, rising from under 3 microseconds at 1 KiB to about 195 microseconds at 4 MiB.
:align: center

OSU MPI Latency benchmark (2 nodes, 2 MPI ranks): containerised versus native OpenMPI.
:::

:::{figure} ../_static/OSU-MPI-Allgather.png
:alt: Grouped bar chart of the OSU MPI_Allgather collective test across 4 nodes and 256 MPI ranks comparing Container and Native latency in milliseconds from 1 KiB to 1 MiB message sizes. Both show nearly identical latency across all sizes, reaching roughly 132 milliseconds at 1 MiB.
:align: center

OSU `MPI_Allgather` collective benchmark (4 nodes, 256 MPI ranks): containerised versus native OpenMPI.
:::

## Fakeroot and GLIBC compatibility

Apptainer on NT and OzSTAR combines a root-mapped user namespace with the host `fakeroot` command so unprivileged users can run package installations during builds (see option 3 in the [Apptainer fakeroot documentation](https://apptainer.org/docs/user/main/fakeroot.html)).

Because `fakeroot` is bound in from the host, building from a container image whose GLIBC version differs substantially from the host can fail with an error similar to:

```text
/.singularity.d/libs/faked: /lib64/libc.so.6: version `GLIBC_2.33' not found (required by /.singularity.d/libs/faked)
```

Check the host GLIBC version on NT or OzSTAR with:

```bash
ldd --version
```

and choose a base image with a compatible GLIBC version. If you must build from an older base image, use the [`fakeroot-bootstrap`](https://github.com/dliptai/fakeroot-bootstrap) script to install a container-compatible `fakeroot` inside `%post`, then use that binary for subsequent package installations (see [Apptainer: using fakeroot inside a definition file](https://apptainer.org/docs/user/main/fakeroot.html#using-fakeroot-command-inside-definition-file)).

## Sandbox mode

:::{warning}
**Never use sandbox mode for production runs.** Sandbox mode unpacks a container into a regular directory of thousands of small files on the host filesystem, completely negating Apptainer's Lustre I/O benefits. Convert your sandbox into a `.sif` image before running production jobs.
:::

Apptainer's [sandbox mode](https://apptainer.org/docs/user/main/quick_start.html#building-images-from-scratch) (`--sandbox` with `--writable`) unpacks a container to a writable directory so you can iterate interactively during development and testing without rebuilding from scratch on every edit. Once testing is complete, convert the sandbox directory into a read-only `.sif` image:

```bash
apptainer build mycontainer.sif my_sandbox_dir/
```

## Next steps

- [Apptainer Example Recipes](apptainer-examples.md) — ready-to-adapt `.def` recipes for astronomy and scientific packages.
- [Python and Conda](python.md) — `pip`-based Python container example and `~/.local` warning.
- [Optimising Lustre I/O](../storage/optimising-lustre.md) — combine Apptainer or SquashFS with `$JOBFS` for high I/O throughput.
- [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) — request GPUs and `--tmp` space for container jobs.
