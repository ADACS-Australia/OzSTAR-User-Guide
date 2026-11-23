# Requesting Resources and Interactive Jobs

Configure CPU, memory, GPU, local scratch (`$JOBFS`), and walltime requests for batch jobs, or start interactive sessions with `sinteractive` and `srun` on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor.

## Before you start

- Know how to write and submit a basic batch script — see [Creating and Submitting Jobs](creating-jobs.md).
- Log in to the login node matching your target cluster (`nt.swin.edu.au` for NT, `ozstar.swin.edu.au` for OzSTAR, or jump to `trevor` via `ssh trevor` from NT or OzSTAR for Trevor) — see [Connecting via SSH](../access/ssh-access.md).

## Memory requests

Always specify how much memory your job requires using either `--mem=<size>` (total memory per allocated node) or `--mem-per-cpu=<size>` (memory per allocated CPU core):

```bash
#SBATCH --mem=8G
```

or:

```bash
#SBATCH --mem-per-cpu=2G
```

- **Default allocation:** `100 MiB` per CPU core (`DefMemPerCPU=100`). This is intentionally small so you supply a realistic estimate.
- **Units:** Bare numbers are interpreted in **MiB**. Suffix `M` means **MiB** and `G` means **GiB** (`1G` = `1024 MiB`).
- **Enforcement:** Slurm enforces memory limits using Linux kernel `cgroup` controls. If your job exceeds its requested memory, the kernel terminates a process (out-of-memory kill), which usually causes the job to fail.

:::{note}
Compute nodes on NT and OzSTAR run jobs from multiple users simultaneously. Accurate memory requests help Slurm schedule your jobs faster via backfill and prevent you from blocking other researchers on shared nodes (see [Policies](../1-getting_started/Policies.rst)).
:::

### Sizing memory accurately

If you do not know how much memory a workflow needs:

1. Run a representative test job with a modest estimate (for example, `--mem-per-cpu=4G`).
2. Check the job's peak memory usage in the [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) (see [Monitoring and Managing Jobs](monitoring.md)).
3. Set your production memory request to roughly **125% of the observed peak** to allow safe headroom without wasting cluster capacity.

:::{warning}
Slurm rejects jobs that request **64 GiB or more per CPU core**, as well as `--mem=0` or `--mem-per-cpu=0`. If your job requires more than 64 GiB of memory in total, request additional CPU cores so that memory per core stays below 64 GiB.
:::

### Maximum requestable memory by node tier

Part of each node's physical RAM is reserved for the operating system, so the maximum requestable memory is slightly below installed RAM. Requesting more memory than standard nodes provide automatically routes your job to high-memory nodes (which have fewer nodes and longer queue times).

| Cluster and node tier | Maximum requestable memory (MiB) | Approximate GiB |
|---|---|---|
| NT (`milan`) standard | `256,500 MiB` | ~250 GiB |
| NT (`milan`) high-memory | `1,030,000 MiB` | ~1,005 GiB |
| NT (`milan`) GPU | `514,500 MiB` | ~502 GiB |
| NT (`milan`) GPU high-memory | `1,030,000 MiB` | ~1,005 GiB |
| OzSTAR (`skylake`) standard | `191,000 MiB` | ~186 GiB |
| OzSTAR (`skylake`) high-memory (384 GB nodes) | `384,000 MiB` | 375 GiB |
| OzSTAR (`skylake`) high-memory (768 GB nodes) | `768,000 MiB` | 750 GiB |
| Trevor | `26,000 MiB` | ~25 GiB |

Inspect live node core counts, requestable memory ceilings, and GPU resources at any time:

```bash
sinfo -o "%P %c %m %G"
```

## CPU and multi-node rules

Request exact CPU resources using `--ntasks` (MPI processes) and `--cpus-per-task` (threads per task). Slurm enforces the following rules at submission time:

- **`--exclusive` is not permitted on `sbatch`:** Submitting a batch script with `--exclusive` is rejected. Request the exact number of cores your job needs with `--cpus-per-task` or `--ntasks` instead.
- **OzSTAR per-node CPU limit:** Although OzSTAR (`skylake`) nodes have 36 physical cores, single jobs are limited to **32 cores per node** to leave cores available for system and GPU communication.
- **Multi-node CPU jobs:** Jobs spanning more than one node must request exact multiples of **64 cores** on NT (`milan`) or **32 cores** on OzSTAR (`skylake`), and `--cpus-per-task` must evenly divide the per-node core count (64 on NT, 32 on OzSTAR).
- **OpenMP thread count:** `OMP_NUM_THREADS` defaults to `1`. Export `OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK` inside multi-threaded scripts (see [Creating and Submitting Jobs](creating-jobs.md)).

## Requesting GPUs

Request GPUs with Slurm Generic Resource Scheduling (`--gres`). Do not specify `--partition` — Slurm automatically routes GPU jobs on the cluster of your login node (`tooarrana1/2` for NT A100 GPUs, `farnarkle1/2` for OzSTAR P100 GPUs; see [Swinburne HPC Systems](../getting-started/systems.md)):

```bash
#SBATCH --gres=gpu:1
```

To request two GPUs on each allocated node, use `#SBATCH --gres=gpu:2`. GPU access is isolated with Linux `cgroup` controls so only your job can use its allocated GPUs. For advanced GPU options, see the [Slurm GRES documentation](https://slurm.schedmd.com/gres.html).

:::{note}
On OzSTAR (`skylake`) nodes, 4 CPU cores per node are reserved for system and GPU communication, and the scheduler does not guarantee optimal CPU-to-GPU locality across allocations. GPU performance on OzSTAR can therefore vary slightly depending on which CPU cores and GPUs are assigned.
:::

## Requesting local scratch (`$JOBFS`)

Every job is allocated a private temporary directory on fast node-local storage (SSD/NVMe), pointed to by the `$JOBFS` environment variable. Using `$JOBFS` for heavy temporary reads and writes avoids slowing down the shared Lustre filesystem (see [Filesystems and Storage](../storage/filesystems.md) and [Optimising Lustre I/O](../storage/optimising-lustre.md)).

:::{warning}
`$JOBFS` is deleted automatically as soon as your job ends. Copy any output files you need to keep back to `/fred/<project>` before your script finishes.
:::

By default, every job receives **`250M`** of `$JOBFS` space. Request more with `--tmp=<size>` (for example, 20 GiB per node):

```bash
#SBATCH --tmp=20G
```

:::{important}
Always use `--tmp=<size>` to request local scratch space. Passing `--gres=tmp:...` is rejected by Slurm.
:::

## Walltime and scheduler limits

Always specify `--time=<DD-HH:MM:SS>` (or `<HH:MM:SS>`) in every batch script. Realistic, shorter walltimes help Slurm backfill your job sooner.

| Limit | Applies to | Value |
|---|---|---|
| Default walltime (if `--time` is omitted) | All compute clusters | `00:05:00` (5 minutes) |
| Maximum walltime | NT, OzSTAR, and Trevor | `7-00:00:00` (7 days) |
| Maximum walltime | Data-mover queue (`datamover`) | `1-00:00:00` (1 day) |
| Maximum job array size (`MaxArraySize`) | All compute clusters | `2048` tasks per array (indices `0`–`2047`) |

Per-user and per-project concurrency caps (CPU, GPU, and queued job limits) vary across general-access and MAS projects and can change over time. Inspect live limits directly on the cluster:

```bash
qinfo -v
sacctmgr show qos format=Name,MaxTRESPU,MaxSubmitPU
sacctmgr show assoc where user=<username> format=Account,User,QOS,GrpTRES
```

## Interactive jobs (`sinteractive` and `srun`)

NT and OzSTAR do not have dedicated interactive compute nodes. Instead, request an interactive compute allocation from a login node with a matching CPU architecture (`tooarrana1` or `tooarrana2` for NT; `farnarkle1` or `farnarkle2` for OzSTAR).

:::{important}
Interactive allocations (`sinteractive` or standalone `srun`) are capped at **1,280 core-minutes** (minimum 5 minutes). For example, you can request ~21 hours on 1 core, ~5 hours on 4 cores, or 40 minutes on 32 cores. For longer runs, submit a batch job with `sbatch`.
:::

### Open an interactive shell (`sinteractive`)

Use `sinteractive` to start an interactive shell on a compute node for testing, compiling, or debugging. It accepts standard `srun` resource flags:

```bash
sinteractive --time=01:00:00 --cpus-per-task=4 --mem=4G
```

Once the allocation starts, your prompt moves to the assigned compute node. Run `exit` when finished so the resources are released immediately.

### Run a single interactive program (`srun`)

Use `srun` directly from a login node to run an interactive command or MPI test on a compute node while streaming input and output to your terminal:

```bash
srun --time=00:30:00 --ntasks=4 --cpus-per-task=2 --mem-per-cpu=2G ./my-interactive-mpi-program
```

Wait until Slurm allocates the nodes, then interact with the program as though it were running locally.

### X11 forwarding in interactive jobs

Pass `--x11` to `sinteractive` or `srun` to display graphical windows from a compute node (requires an SSH connection with X11 forwarding enabled — see [Graphical Access (X11 and VNC)](../access/graphical-access.md)):

```bash
sinteractive --x11 --time=01:00:00 --cpus-per-task=2 --mem=4G
```

:::{warning}
`--x11` does not work inside `screen` or `tmux` sessions. Connect directly with X11 forwarding enabled before starting `sinteractive --x11`.
:::

## Next steps

- [Job Script Examples](examples.md) — ready-to-use batch scripts for serial, MPI, OpenMP, hybrid, array, packed, GPU, and interactive jobs.
- [Monitoring and Managing Jobs](monitoring.md) — measure actual memory and CPU utilisation in the Web Job Monitor.
- [Slurm Command Reference](slurm-reference.md) — quick-reference table of Slurm commands and `#SBATCH` directives.
