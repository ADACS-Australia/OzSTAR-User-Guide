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

- **Default allocation:** Omitting `--mem` and `--mem-per-cpu` gives only a minimal per-core default memory allocation, intentionally small so you supply a realistic estimate.
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
Slurm rejects jobs that request an excessively high amount of memory per CPU core, as well as `--mem=0` or `--mem-per-cpu=0`. Keep memory-per-core requests modest; if Slurm rejects a job for exceeding the per-core memory limit, request additional CPU cores or reduce your memory request.
:::

### Checking maximum requestable memory

Part of each node's physical RAM is reserved for the operating system, so the maximum memory you can request in Slurm is slightly below the installed physical RAM. Requesting more memory than standard nodes provide automatically routes your job to high-memory nodes (which are fewer in number and generally have longer queue waits).

Inspect live node core counts, exact requestable memory ceilings (`MEMORY`, shown in MiB), and GPU resources directly from Slurm before submitting large-memory jobs:

```bash
sinfo -o "%P %c %m %G"
```

## CPU and multi-node rules

Request exact CPU resources using `--ntasks` (MPI processes) and `--cpus-per-task` (threads per task). Slurm enforces the following rules at submission time:

- **`--exclusive` is not permitted on `sbatch`:** Submitting a batch script with `--exclusive` is rejected. Request the exact number of cores your job needs with `--cpus-per-task` or `--ntasks` instead.
- **OzSTAR per-node CPU limit:** Single jobs on OzSTAR are limited to **32 cores per node** (out of 36 physical cores) to leave cores available for system and GPU communication.
- **Multi-node CPU jobs:** Jobs spanning more than one node must request exact multiples of **64 cores** on NT or **32 cores** on OzSTAR, and `--cpus-per-task` must evenly divide the per-node core count (64 on NT, 32 on OzSTAR).
- **OpenMP thread count:** `OMP_NUM_THREADS` defaults to `1`. Export `OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK` inside multi-threaded scripts (see [Creating and Submitting Jobs](creating-jobs.md)).

## Requesting GPUs

Request GPUs with Slurm Generic Resource Scheduling (`--gres`). Do not specify `--partition` — Slurm automatically routes GPU jobs on the cluster of your login node (`tooarrana1/2` for NT, `farnarkle1/2` for OzSTAR; see [Swinburne HPC Systems](../getting-started/systems.md) for GPU models):

```bash
#SBATCH --gres=gpu:1
```

To request two GPUs on each allocated node, use `#SBATCH --gres=gpu:2`. GPU access is isolated with Linux `cgroup` controls so only your job can use its allocated GPUs. For advanced GPU options, see the [Slurm GRES documentation](https://slurm.schedmd.com/gres.html).

:::{note}
On OzSTAR, 4 CPU cores per node are reserved for system and GPU communication, and the scheduler does not guarantee optimal CPU-to-GPU locality across allocations. GPU performance on OzSTAR can therefore vary slightly depending on which CPU cores and GPUs are assigned.
:::

## Requesting local scratch (`$JOBFS`)

Every job is allocated a private temporary directory on fast node-local storage (SSD/NVMe), pointed to by the `$JOBFS` environment variable. Using `$JOBFS` for heavy temporary reads and writes avoids slowing down the shared Lustre filesystem (see [Filesystems and Storage](../storage/filesystems.md) and [Optimising Lustre I/O](../storage/optimising-lustre.md)).

:::{warning}
`$JOBFS` is deleted automatically as soon as your job ends. Copy any output files you need to keep back to `/fred/<project>` before your script finishes.
:::

Omitting `--tmp` allocates only a minimal default `$JOBFS` space. Request the local scratch capacity your job needs with `--tmp=<size>` (for example, 20 GiB per node):

```bash
#SBATCH --tmp=20G
```

:::{important}
Always use `--tmp=<size>` to request local scratch space. Passing `--gres=tmp:...` is rejected by Slurm.
:::

## Walltime and scheduler limits

Always specify `--time=<DD-HH:MM:SS>` (or `<HH:MM:SS>`) in every batch script — omitting `--time` assigns only a very short default walltime. Realistic, shorter walltimes help Slurm backfill your job sooner.

- **Compute cluster maximum walltime:** **7 days** (`7-00:00:00`) on NT, OzSTAR, and Trevor.
- **Data-mover batch jobs:** Transfer jobs submitted on the data-mover queue (`datamover`) have a shorter maximum walltime than compute queues.
- **Job arrays:** Slurm enforces a cluster-wide maximum array index (`MaxArraySize`).

Inspect live partition walltime limits, Slurm configuration defaults, and per-user/project concurrency caps directly on the cluster:

```bash
sinfo -s
qinfo -v     # or qinfo -s for a compact summary
scontrol show config | grep -E 'DefMemPer|MaxArraySize'
sacctmgr show qos format=Name,MaxTRESPU,MaxSubmitPU
sacctmgr show assoc where user=<username> format=Account,User,QOS,GrpTRES
```

## Interactive jobs (`sinteractive` and `srun`)

NT and OzSTAR do not have dedicated interactive compute nodes. Instead, request an interactive compute allocation from a login node with a matching CPU architecture (`tooarrana1` or `tooarrana2` for NT; `farnarkle1` or `farnarkle2` for OzSTAR).

:::{important}
Interactive allocations (`sinteractive` or standalone `srun`) are limited to short sessions based on total core-time — the more CPU cores you request, the shorter the permitted walltime. If Slurm rejects an interactive request for exceeding the interactive time limit, reduce your core count or `--time`, or submit a batch job with `sbatch`.
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
