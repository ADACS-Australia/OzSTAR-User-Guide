# Creating and Submitting Jobs

Write a Slurm batch script and submit it to compute nodes on Ngarrgu Tindebeek (NT), OzSTAR, or Trevor using `sbatch`. Compute nodes do not accept direct SSH logins unless you have an active job running on them.

## Before you start

- Connect via SSH to the login node for the cluster you want to run on (`nt.swin.edu.au` for NT, `ozstar.swin.edu.au` for OzSTAR, or jump to `trevor` via `ssh trevor` from NT or OzSTAR for Trevor). See [Connecting via SSH](../access/ssh-access.md) and [Swinburne HPC Systems](../getting-started/systems.md).
- Store large input and output data under `/fred/<project>` rather than `/home`. See [Filesystems and Storage](../storage/filesystems.md).
- Review the [Policies](../1-getting_started/Policies.rst) on resource efficiency and keeping compute workloads off login nodes.

## How Slurm works

Swinburne HPC uses [Slurm](https://slurm.schedmd.com/) to allocate compute nodes fairly across users. A Slurm job has two parts:

- **Resource requests:** The CPUs, memory, GPUs, local scratch disk, and walltime your job requires.
- **Job steps:** The software setup and commands your job executes once resources are allocated.

You normally define both parts in a **batch script** (a shell script containing `#SBATCH` directives) and submit it with `sbatch`. See `man sbatch` or the [Slurm Command Reference](slurm-reference.md) for a summary of available options.

## Cluster and partition routing

Slurm automatically routes each job to the cluster of the login node where you run `sbatch`:

- `tooarrana1` / `tooarrana2` (`nt.swin.edu.au`) → **Ngarrgu Tindebeek (NT)**
- `farnarkle1` / `farnarkle2` (`ozstar.swin.edu.au`) → **OzSTAR**
- `trevor` *(jump via `ssh trevor` from NT or OzSTAR)* → **Trevor**

:::{important}
Do not specify `--partition` in your batch script. Partitions are managed internally by Slurm based on the login node you submit from and the resources you request (such as memory or GPUs). Manually requesting internal partitions (for example, `milan-gpu` or `milan-c`) is rejected by the scheduler.
:::

## Write and submit a batch script

Every batch script must follow this order:

1. **Line 1 — Shebang:** Start the first line with the script interpreter, such as `#!/bin/bash`.
2. **Next lines — `#SBATCH` directives:** Place all resource requests and Slurm options immediately below the shebang, before any shell commands.
3. **Commands and job steps:** Load required modules, set environment variables, and run your program (using `srun` for Slurm job steps). Define module loads and environment variables inside the batch script rather than in dotfiles so your runs stay reproducible (see [Dotfiles and shell hygiene](../access/linux-environment.md#dotfiles-and-shell-hygiene)).

Save the following example as `myjob.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --output=test_%j.out
#
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=200M

srun hostname
srun sleep 60
```

This script requests 1 CPU core (`--ntasks=1`) for 10 minutes (`--time=00:10:00`) with 200 MiB of RAM (`--mem-per-cpu=200M`). When the job starts, the first `srun` step prints the allocated compute node name, and the second step sleeps for 60 seconds.

- `--job-name=test` assigns a label shown in queue listings and the Web Job Monitor.
- `--output=test_%j.out` directs standard output and standard error to a file where `%j` is replaced by the numeric Slurm Job ID.

:::{note}
If you omit `--output`, Slurm writes to `slurm-%j.out` by default. Always keep `%j` (or `%A_%a` for job arrays) in the output filename so simultaneous jobs never write to the same file. Concurrent writes to one file from multiple nodes corrupt output and trigger Lustre lock bouncing (see [Optimising Lustre I/O](../storage/optimising-lustre.md)).
:::

Submit `myjob.sh` to Slurm:

```bash
sbatch myjob.sh
```

Slurm confirms submission and returns your Job ID:

```text
Submitted batch job 12345678
```

You can also pass Slurm options directly on the command line (for example, `sbatch --time=00:30:00 myjob.sh`), which overrides matching `#SBATCH` lines in the script. Keeping options inside your script makes experiments easier to reproduce.

:::{tip}
A running batch script can submit follow-up jobs to Slurm by calling `sbatch` inside the script, which is useful for multi-stage workflows.
:::

## Verify it works and inspect output

Check whether your job is queued or running:

```bash
squeue --me
```

While a job is running, you can inspect live resource usage with `sstat -a -j <job_id>` (or `sstat -j <job_id>.batch` for the batch script step) or the [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) (see [Monitoring and Managing Jobs](monitoring.md)).

Slurm appends output to the output file while the job runs. Replace `<job_id>` with the ID returned by `sbatch` to read the output:

```bash
cat test_<job_id>.out
```

## Job lifecycle states

After you run `sbatch`, your job moves through these states:

1. **`PENDING` (`PD`):** The job is queued and waiting for priority or matching resources to become available.
2. **`RUNNING` (`R`):** Slurm has allocated compute resources and your batch script is executing.
3. **`COMPLETED` (`CD`)** or **`FAILED` (`F`):** The job finished cleanly with exit code `0` (`COMPLETED`), or exited with a non-zero error / exceeded a resource limit such as memory or walltime (`FAILED`).

## Merit Allocation Scheme (MAS) projects

If your research group has been awarded compute time under the ASTAC Merit Allocation Scheme (MAS), specify the MAS project ID in your batch script:

```bash
#SBATCH --account=<mas_project>
```

Slurm automatically applies that project's ASTAC priority quality of service (QoS) and bills usage against the MAS allocation.

Also ensure your job writes output files into `/fred/<mas_project>` (where the directory group ID is set to the MAS project) so storage is charged to the MAS project quota, or switch your active group before submitting if required. See [Accounts and Projects](../getting-started/accounts.md) for project membership details.

If you are running LIGO-related jobs, you must also include a LIGO accounting tag with `#SBATCH --comment=...` — see [Tracking LIGO Job Usage](ligo-reporting.md).

## Parallel job models

The `myjob.sh` example above runs a **serial** job on a single CPU core. To use multiple cores or multiple nodes, choose the parallel model that matches your code:

- **Multi-process ([MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) / SPMD):** Multiple cooperating processes launched across one or more nodes. In Slurm, each process is a **task** requested with `--ntasks`. Tasks may be placed on separate compute nodes unless constrained.
- **Multi-threaded (shared memory / [OpenMP](https://en.wikipedia.org/wiki/OpenMP) / pthreads):** One process (`--ntasks=1`) spawning multiple threads on the **same** compute node, requested with `--cpus-per-task`. Slurm never splits a single task across multiple nodes.
- **Embarrassingly parallel (job arrays):** Many independent runs of the same program across different files or parameter values using `#SBATCH --array`.
- **Hybrid (MPI + OpenMP):** Multiple MPI tasks (`--ntasks`), each using multiple OpenMP threads (`--cpus-per-task`).

For OpenMP and hybrid jobs, `OMP_NUM_THREADS` defaults to `1` on NT and OzSTAR. Export it in your batch script so your code uses all allocated cores per task:

```bash
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
```

For full resource rules (memory ceilings, multi-node core multiples, GPUs, and `$JOBFS`), see [Requesting Resources and Interactive Jobs](resources-and-interactive.md). For complete templates of each parallel model, see [Job Script Examples](examples.md).

## Next steps

- [Requesting Resources and Interactive Jobs](resources-and-interactive.md) — set memory, CPU, GPU, local scratch (`$JOBFS`), walltime, and interactive allocations.
- [Job Script Examples](examples.md) — copy-paste scripts for serial, MPI, OpenMP, hybrid, job array, packed, and GPU workloads.
- [Monitoring and Managing Jobs](monitoring.md) — track job efficiency in the Web Job Monitor and command-line tools.
