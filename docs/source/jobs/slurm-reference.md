# Slurm Command Reference

Quick-reference tables of common Slurm commands and `#SBATCH` directives for Ngarrgu Tindebeek (NT), OzSTAR, and Trevor.

## Common Slurm commands

| Command | Purpose | Example |
|---|---|---|
| `sbatch` | Submit a batch script to the queue | `sbatch myjob.sh` |
| `srun` | Launch a parallel job step or interactive program | `srun ./hello.mpi` |
| `sinteractive` | Open an interactive shell on a compute node | `sinteractive --cpus-per-task=4 --time=00:30:00 --mem=4G` |
| `scancel` | Cancel one, pending, or all of your jobs | `scancel <job_id>` / `scancel -u <username>` / `scancel -u <username> -t PD` |
| `squeue` | List queued and running jobs (use `--me` for yours) | `squeue --me` |
| `qinfo` | Show cluster resource allocation status (detailed or summary) | `qinfo -v` / `qinfo -s` |
| `showbf` | List available backfill slots | `showbf` |
| `sinfo` | Inspect partition summary, node states, CPUs, RAM, and GPUs | `sinfo -s` / `sinfo -o "%P %c %m %G"` |
| `sstat` | Check live resource usage of a running job (all steps or `.batch`) | `sstat -a -j <job_id>` / `sstat -j <job_id>.batch` |
| `sjob` | Display detailed status for a running job | `sjob <job_id>` |
| `sacct` | Query accounting history for completed or failed jobs | `sacct -j <job_id>` |
| `jobreport` | Print a resource usage summary for a job | `jobreport <job_id>` |
| `scontrol show job` | Inspect full metadata for an active or recent job | `scontrol show job <job_id>` |

:::{note}
Do not poll `squeue` in tight loops such as `watch squeue`; use the [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) for live updates. Note also that `scontrol update` is disabled for user jobs — cancel and resubmit to change pending job options.
:::

## Common `#SBATCH` directives

Place `#SBATCH` directives immediately after the shebang line (`#!/bin/bash`) at the top of your batch script. Do not specify `--partition` or `--exclusive` on `sbatch` — both are managed or rejected by the scheduler (see [Requesting Resources and Interactive Jobs](resources-and-interactive.md)).

| Short | Long | Description |
|---|---|---|
| `-N <count>` | `--nodes=<count>` | Allocate `<count>` compute nodes (multi-node CPU jobs must match full-node core multiples — see [CPU and multi-node rules](resources-and-interactive.md#cpu-and-multi-node-rules)). |
| `-n <count>` | `--ntasks=<count>` | Request `<count>` tasks (processes, typically MPI ranks). |
| — | `--ntasks-per-node=<count>` | Place `<count>` tasks on each allocated node. |
| `-c <count>` | `--cpus-per-task=<count>` | Allocate `<count>` CPU cores per task (for OpenMP or multi-threaded jobs; defaults to `1`). |
| `-t <time>` | `--time=<DD-HH:MM:SS>` | Maximum walltime (always specify explicitly; check live partition limits with `sinfo -s`). |
| — | `--mem=<size>` | Maximum total RAM per node (default units MiB; `G` = GiB). Cannot be `0`; excessive per-core memory requests are rejected. |
| — | `--mem-per-cpu=<size>` | Maximum RAM per allocated core (always specify explicitly; excessive per-core values are rejected). |
| — | `--tmp=<size>` | Request node-local scratch at `$JOBFS` (omitting allocates only a minimal default; do not use `--gres=tmp:...`). |
| — | `--gres=gpu:<n>` | Request `<n>` GPUs per node (omit `--partition`). |
| `-A <project>` | `--account=<project>` | Charge usage to `<project>` (required for MAS/ASTAC allocations; applies ASTAC QoS automatically). |
| `-J <name>` | `--job-name=<name>` | Set a short job name shown in queue listings and the Web Job Monitor. |
| `-o <file>` | `--output=<file>` | Write standard output (and standard error unless `-e` is set) to `<file>` (default `slurm-%j.out`; `%j` = Job ID, `%A_%a` = array ID/task). |
| `-e <file>` | `--error=<file>` | Write standard error to a separate `<file>`. |
| `-D <dir>` | `--chdir=<dir>` | Set the working directory before running the batch script. |
| `-a <spec>` | `--array=<spec>` | Submit a job array (for example, `0-99` or `1-100:2`; check live `MaxArraySize` via `scontrol show config`). |
| — | `--mail-type=<events>` | Email notifications on state changes (for example, `BEGIN,END,FAIL,TIME_LIMIT_90`; applies to job arrays as a whole). |
| — | `--mail-user=<email>` | Email address for `--mail-type` notifications. |
| — | `--comment=<text>` | Attach a metadata tag to the job (mandatory for LIGO accounting; see [Tracking LIGO Job Usage](ligo-reporting.md)). |

For the complete list of directives and filename replacement symbols, run `man sbatch` on a login node or consult the [Slurm `sbatch` documentation](https://slurm.schedmd.com/sbatch.html).

## Next steps

- [Creating and Submitting Jobs](creating-jobs.md) — write and submit your first batch script.
- [Requesting Resources and Interactive Jobs](resources-and-interactive.md) — memory ceilings, core-multiple rules, GPUs, and interactive limits.
- [Job Script Examples](examples.md) — complete scripts combining these directives for common workflows.
