# Environment Modules and Installing Software

Load pre-installed compilers, libraries, and scientific applications on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor using the Lmod module system, or compile and install your own software on top of the provided toolchains.

## Discovering and loading modules

NT, OzSTAR, and Trevor use [Lmod](https://lmod.readthedocs.io/en/latest/) (an implementation of [Environment Modules](https://modules.sourceforge.net/)) to update `PATH`, `LD_LIBRARY_PATH`, and related variables dynamically without manual shell configuration.

:::{important}
NT, OzSTAR, and Trevor each maintain their own architecture-specific software tree. Always check available modules and versions on the cluster where your jobs will run (see [Swinburne HPC Systems](../getting-started/systems.md)).
:::

Common `module` commands:

```bash
# List all installed software packages across the entire hierarchy
module spider

# Search for a specific package and view required parent modules
module spider <package>

# List modules loadable in your current environment
module avail

# Load a specific package version
module load <package>/<version>

# Inspect what environment variables and paths a module sets
module show <package>/<version>

# List loaded modules
module list

# Unload one module, or clear all loaded modules
module unload <package>
module purge

# Print all available module subcommands
module
```

**Explicit version numbers are required for software, compiler, and MPI modules.** There are no default versions for versioned packages on Swinburne HPC clusters; requiring `<package>/<version>` prevents your scripts from silently changing behaviour when newer software is installed, and running `module load <package>` without a version prints the available versions instead. A small number of unversioned utility modules — such as `apptainer` and `mamba` — load directly without a version (`module load apptainer`, `module load mamba`).

## Using the `ml` shorthand

Lmod provides [`ml`](https://lmod.readthedocs.io/en/latest/010_user.html#ml-a-convenient-tool) as a concise shorthand for `module` commands:

| `ml` command | Equivalent `module` command |
|---|---|
| `ml` | `module list` |
| `ml <package>/<version>` | `module load <package>/<version>` |
| `ml -<package>` | `module unload <package>` |
| `ml <pkg_a>/<version> -<pkg_b>` | `module unload <pkg_b>; module load <pkg_a>/<version>` |
| `ml spider` | `module spider` |
| `ml avail` | `module avail` |
| `ml show <package>/<version>` | `module show <package>/<version>` |
| `ml load spider` | Load a module literally named `spider` |

## Global module aliases

The module system defines global aliases so common names continue to work:

- `conda` and `anaconda` → `mamba`
- `singularity` → `apptainer`

Both `mamba` and `apptainer` are unversioned utility modules that load directly with `module load mamba` or `module load apptainer` (run `module spider mamba` or `module spider apptainer` to inspect module details on your cluster).

## Hierarchical modules

Swinburne HPC uses a **three-level module hierarchy** to prevent incompatible compiler and MPI combinations from being loaded together:

- **Core:** Modules built with the system compiler. Includes compilers (such as `gcc`), system utilities, and pre-compiled binaries.
- **Compiler:** Modules built with a specific Core compiler (this level does *not* contain compilers). Includes MPI libraries (such as `openmpi`) and serial libraries or applications compiled with that compiler.
- **MPI:** Modules built with a specific compiler and MPI combination. Includes parallel libraries (such as parallel `hdf5`) and most MPI-enabled HPC applications.

### `module avail` versus `module spider`

- `module avail` shows only modules that can be loaded given your already-loaded parent modules. Compiler-level modules appear only after you load a Core compiler, and MPI-level modules appear only after you load both a compiler and an MPI library.
- `module spider` searches the **entire** software tree regardless of what is loaded, and `module spider <package>/<version>` prints the exact parent modules needed to load that version.

### Automatic versus multi-parent loading

- If a module version exists under only **one** compiler/MPI parent combination, `module load <package>/<version>` loads its required parent modules automatically.
- If a module version exists under **multiple** parent combinations, loading it without its parents first displays the valid parent combinations so you can load your chosen parents explicitly.

For example, to discover and load an MPI-enabled library such as `hdf5`:

```bash
# 1. List all available versions of hdf5 on your cluster
module spider hdf5

# 2. Check which compiler and MPI parent modules your chosen version requires
module spider hdf5/<hdf5_version>

# 3. Load the parent compiler, MPI library, and package in order
ml gcc/<gcc_version>
ml openmpi/<openmpi_version>
ml hdf5/<hdf5_version>
```

## Toolchains

A **toolchain** is a coordinated bundle of a compiler, MPI library, and numerical libraries defined by [EasyBuild](https://easybuild.io/). Loading a toolchain loads all of its component modules at once and ensures build compatibility across dependencies.

Common toolchain families on Swinburne clusters include `foss`, `gompi`, `gfbf`, and `python-scientific` (available versions differ between NT, OzSTAR, and Trevor). See the [EasyBuild common toolchains overview](https://docs.easybuild.io/common-toolchains/#common_toolchains_overview) for the components in each family.

Discover the toolchains installed on your cluster by inspecting the **Toolchains** section of `module avail`, or by querying a family with `module spider`:

```bash
module avail
module spider foss
```

Then load the specific toolchain version you want, for example:

```bash
ml foss/<version>
```

## Installing your own software

You are permitted and encouraged to build and install your own software on NT, OzSTAR, and Trevor. Maintaining your own installation lets you control exact versions, build flags, and updates independently of central modules.

Whether compiling your own research code or building an established package from source:

1. Load an appropriate toolchain (for example, `foss/<version>` or `gcc/<version>`) on the cluster where you intend to run jobs, so binaries are optimised for that cluster's CPU architecture (see [Porting between clusters](../getting-started/systems.md#porting-between-clusters)).
2. Install large builds or shared team tools under `/fred/<project>/`, or small personal utilities under `/home/<username>/` (keeping `/home` quota limits in mind; see [Filesystems and Storage](../storage/filesystems.md)).
3. For complex Python stacks or software that creates thousands of small files, consider [Python and Conda](python.md) or [Containers (Apptainer)](apptainer.md).

If you are unsure how to build a package, or would like to request a widely used central module, email `hpc-support@swin.edu.au` (see [User Support](../help/support.md)).

## Next steps

- [Python and Conda](python.md) — set up `venv`, Conda/Mamba, or containerised Python environments.
- [Containers (Apptainer)](apptainer.md) — package complex software stacks or 32-bit applications in `.sif` images.
- [Swinburne HPC Systems](../getting-started/systems.md) — understand CPU/GPU differences across NT, OzSTAR, and Trevor.
- [User Support](../help/support.md) — request help with builds or central module installations.
