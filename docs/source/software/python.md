# Python and Conda

Set up isolated, reproducible Python environments on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor using Python modules with `venv` or Apptainer containers (strongly preferred over bare Conda environments on Lustre).

Choose the method that fits your workflow:

1. **Python module and `venv` (recommended default)** — lightweight, fast to load on Lustre, and built against cluster toolchains.
2. **Apptainer container (recommended for large stacks or Conda packages)** — packages an entire `pip` or Micromamba/Conda environment into a single `.sif` file, avoiding Lustre small-file slowdowns and inode exhaustion while ensuring portability.
3. **Bare Conda / Mamba on Lustre (last resort)** — use directly on the host filesystem only if neither `venv` nor an Apptainer container is feasible for your workflow; bare Conda environments create tens of thousands of tiny files that slow down imports, strain shared Lustre metadata servers, and rapidly consume file-count quotas.

:::{note}
Avoid using the operating-system Python at `/usr/bin/python`. Choosing one of the managed methods above keeps your packages isolated and reproducible.
:::

## Python modules and virtual environments

Discover available Python modules on your target cluster before creating an environment:

```bash
# List standalone Python modules
module spider python

# List python-scientific toolchains (bundled with common scientific packages)
module spider python-scientific
```

Check the exact packages and required parent modules for any version with:

```bash
module spider python/<version>
```

- `python/<version>` requires loading its parent `gcc/<gcc_version>` module first (listed in the `module spider` output). Some older Python versions also provide a minimal `-bare` variant; run `module spider python/<version>` to inspect included packages.
- `python-scientific/<version>` loads directly and includes widely used scientific libraries (such as SciPy and IPython) compiled against a cluster toolchain.

Because you do not have write permissions to the central module tree, install extra packages with `pip` inside a [Python virtual environment (`venv`)](https://docs.python.org/3/library/venv.html).

:::{note}
`PIP_REQUIRE_VIRTUALENV=yes` is enforced by default so `pip` cannot accidentally install packages into `~/.local`. Although setting `PIP_REQUIRE_VIRTUALENV=false` overrides this, installing into `~/.local` causes conflicts across Python modules and environments and is not supported.
:::

### Step-by-step `venv` workflow

Replace `<version>` with a `python-scientific` version discovered via `module spider python-scientific` on your target cluster:

1. Load the Python module and verify what is loaded:

   ```bash
   ml python-scientific/<version>
   module list
   ```

2. Create and activate a virtual environment. Include `--system-site-packages` so packages provided by the loaded module (such as SciPy) remain accessible inside your `venv` (omit this flag if you want complete isolation from module-provided Python packages):

   ```bash
   python -m venv --system-site-packages ~/my-venv
   source ~/my-venv/bin/activate
   ```

   Your shell prompt updates to show `(my-venv)` while the environment is active.

3. Install additional packages with `pip` and run your code (or launch `ipython` for interactive prototyping and press `Ctrl+D` to exit):

   ```bash
   pip install <package_name>
   python my_script.py
   ```

4. Deactivate the environment when finished:

   ```bash
   deactivate
   ```

5. In any later login session or batch script, load the **exact same modules first**, then activate the virtual environment:

   ```bash
   ml python-scientific/<version>
   source ~/my-venv/bin/activate
   python my_script.py
   ```

:::{important}
Always load your required modules *before* activating your virtual environment. Activating a `venv` without loading its matching Python module first leaves Python unable to resolve its shared libraries.
:::

## Containerised Python with Apptainer

Large Python and Conda environments contain tens of thousands of small files, which load slowly on Lustre, consume large numbers of file-count inodes, and increase metadata load across the shared cluster (see [Optimising Lustre I/O](../storage/optimising-lustre.md)). Packaging your environment into an Apptainer `.sif` container is strongly recommended whenever you need Conda packages, custom Python versions, or large machine-learning stacks:

1. **Fast Lustre I/O and minimal inode usage**, because Lustre sees a single read-only [SquashFS](https://docs.kernel.org/filesystems/squashfs.html) file rather than tens of thousands of small files.
2. **Reproducibility and portability** across different systems.

See [Building a container from a definition file](apptainer.md#building-a-container-from-a-definition-file) for a Micromamba/Conda container recipe (`bilby.def`), and [Containers (Apptainer)](apptainer.md) for bind mounts and GPU usage.

### Example: `pip`-based Python container

:::{note}
Replace `<version>` with a current pinned Python Docker image tag from [Docker Hub](https://hub.docker.com/_/python) for reproducibility, and check host GLIBC compatibility (`ldd --version`) if a build hits fakeroot errors (see [Fakeroot and GLIBC compatibility](apptainer.md#fakeroot-and-glibc-compatibility)).
:::

Create a definition file named `my_container.def`:

```singularity
BootStrap: docker
From: python:<version>-slim

%post
    pip install wheel "tensorflow[and-cuda]" tensorflow-datasets pandas
```

Load Apptainer and build the `.sif` image:

```bash
module load apptainer
apptainer build my_container.sif my_container.def
```

Run a GPU script inside the container (`--nv` enables GPU access; `$PWD` is bind-mounted automatically so `my_tensorflow_script.py` in your current working directory is visible inside the container):

```bash
apptainer run --nv my_container.sif python my_tensorflow_script.py
```

:::{warning}
A `.sif` container is an **immutable, read-only** SquashFS image — you must edit the `.def` file and rebuild the image to change packages.

Do **not** run `pip install` inside a running container (for example, `apptainer run my_container.sif pip install <package_name>`). Because container `site-packages` is read-only and Apptainer bind-mounts `$HOME` at runtime, `pip` silently prints *"Defaulting to user installation because normal site-packages is not writeable"* and installs packages into your host `~/.local` directory. Those host files then bleed into future container runs and cause difficult environment conflicts.
:::

## Conda and Mamba (last resort)

:::{warning}
Unpacked [Conda](https://docs.conda.io/en/latest/) and Mamba environments create tens of thousands of small files on disk. On shared Lustre filesystems, this causes slow startup and import times, stresses metadata servers for all users, and rapidly exhausts file-count (inode) quotas. Prefer building a **containerised Micromamba environment with Apptainer** (see [Building a container from a definition file](apptainer.md#building-a-container-from-a-definition-file)) or using a lightweight **`python` module + `venv`** above, and treat bare Conda/Mamba environments on Lustre as a last resort.
:::

If you must use an unpacked Conda environment directly on the cluster, load it via the `mamba` module (`conda` and `anaconda` are global aliases for `mamba`):

```bash
module load mamba
```

[Mamba](https://github.com/mamba-org/mamba) is a fast C++ reimplementation of Conda with the same CLI interface. Prefer `mamba install` and `mamba create` over `conda install` to avoid the slower classic solver. For a comparison of Anaconda, Conda, Miniconda, Mamba, Mambaforge, and Micromamba, see the [Bioconda FAQ](https://bioconda.github.io/faqs.html#what-s-the-difference-between-anaconda-conda-miniconda-mamba-mambaforge-micromamba). For full environment-management commands, see the [Conda environment management guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

The default channel is [`conda-forge`](https://conda-forge.org/docs/user/introduction/). To install from the Anaconda `defaults` channel instead, pass `-c defaults`:

```bash
mamba install -c defaults <package_name>
```

If you need an environment containing the [Anaconda](https://www.anaconda.com/docs/main) package distribution:

```bash
mamba install -c defaults anaconda
```

### Conda and home directory quota

:::{warning}
By default, Conda stores environments and package caches in `~/.conda`, which will quickly exhaust your `/home` block and 200,000-file quotas (see [Filesystems and Storage](../storage/filesystems.md)). Always place bare Conda environments on `/fred/<project>/` — and keep old or unused environments cleaned up so they do not exhaust your project's file-count quota either.
:::

Configure Conda in your user configuration (`~/.condarc`) to place environments and package caches in your project directory (after running `module load mamba`):

```bash
conda config --prepend envs_dirs /fred/<project>/<username>/.conda/envs
conda config --prepend pkgs_dirs /fred/<project>/<username>/.conda/pkgs
```

Alternatively, move an existing `~/.conda` directory to `/fred/<project>/<username>/.conda` and link it back:

```bash
mv ~/.conda /fred/<project>/<username>/.conda
ln -s /fred/<project>/<username>/.conda ~/.conda
```

:::{note}
`/home` backups do **not** follow symlinks, and `/fred` is not backed up. To back up your environment definition, export a YAML file into `/home/<username>/`:

```bash
conda env export > ~/environment.yml
```

Recreate the environment later with:

```bash
mamba env create -f ~/environment.yml
```
:::

### Using cluster MPI libraries with Conda

Cluster OpenMPI modules are built specifically for NT and OzSTAR's high-speed interconnects (see [Swinburne HPC Systems](../getting-started/systems.md)). Installing MPI-dependent packages from `conda-forge` pulls in generic Conda MPI binaries by default, which can run poorly or fail across nodes.

Load a cluster OpenMPI module (discover versions with `module spider openmpi`), then install the `conda-forge` external OpenMPI stub matching that version so Conda packages link against the cluster's MPI:

```bash
conda install "openmpi=<openmpi_version>=external_*"
```

For full instructions, see the [conda-forge external MPI documentation](https://conda-forge.org/docs/user/tipsandtricks/#using-external-message-passing-interface-mpi-libraries) and the [mpi4py Conda installation guide](https://mpi4py.readthedocs.io/en/stable/install.html#using-conda).

### Installing CUDA/GPU-enabled packages

CUDA-enabled Conda packages (such as TensorFlow or PyTorch) install GPU builds only when Conda detects an NVIDIA display driver via the `__cuda` [virtual package](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html). Check which virtual packages Conda detects on your node:

```bash
conda info
```

The NT login nodes (`tooarrana1` and `tooarrana2`) do not have GPUs or an NVIDIA display driver installed, whereas OzSTAR login nodes (`farnarkle1` and `farnarkle2`) and GPU compute nodes do.

To install CUDA-enabled packages on `tooarrana1` or `tooarrana2`:

1. Find the maximum CUDA version supported by the GPU driver by running `nvidia-smi` on `farnarkle1`/`farnarkle2` or inside an interactive GPU job on NT (read the `CUDA Version:` field in the header):

   ```bash
   nvidia-smi
   ```

2. Set `CONDA_OVERRIDE_CUDA` to that version when installing with `mamba`:

   ```bash
   CONDA_OVERRIDE_CUDA=<cuda_version> mamba install <package_name>
   ```

Alternatively, create your GPU Conda environment directly on `farnarkle1`/`farnarkle2` or inside an interactive GPU job.

For more detail, see [conda-forge: Installing CUDA-enabled packages](https://conda-forge.org/docs/user/tipsandtricks/#installing-cuda-enabled-packages-like-tensorflow-and-pytorch).

## Next steps

- [Containers (Apptainer)](apptainer.md) — package Conda or `pip` environments into single-file `.sif` containers.
- [Jupyter Notebooks](notebooks.md) — run interactive notebooks from your Python environment.
- [Environment Modules and Installing Software](modules.md) — explore cluster toolchains and Lmod commands.
- [Optimising Lustre I/O](../storage/optimising-lustre.md) — avoid small-file bottlenecks on Lustre.
