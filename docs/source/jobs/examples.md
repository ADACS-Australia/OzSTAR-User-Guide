# Job Script Examples

Copy and adapt tested Slurm batch scripts for serial, MPI, OpenMP, hybrid, job array, packed, master/worker, GPU, and interactive workloads on Ngarrgu Tindebeek (NT) and OzSTAR.

## Before you start

- Review [Creating and Submitting Jobs](creating-jobs.md) for script anatomy and automatic cluster routing (never specify `--partition`).
- Review [Requesting Resources and Interactive Jobs](resources-and-interactive.md) for memory ceilings, multi-node core multiples, GPU flags, and `$JOBFS` (`--tmp`).
- Use `module spider <package>` on your target login node to look up exact available module versions before replacing `<version>` placeholders below (see [Environment Modules and Installing Software](../software/modules.md)).

## Serial job

Use a serial script for single-core programs. Save as `serial.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=serial_example
#SBATCH --output=serial_%j.out
#
#SBATCH --ntasks=1
#SBATCH --time=00:10:00
#SBATCH --mem=1G

module load <application>/<version>

./my_program input.dat
```

Submit with `sbatch serial.sh` and inspect output in `serial_<job_id>.out`.

## Message passing (MPI)

An MPI job launches multiple cooperating processes (`--ntasks`) across one or more nodes. Run `module spider openmpi` on your target cluster to find a matching `gcc/<version>` and `openmpi/<version>` pair, and use the exact same versions for both compiling and running.

To test with Wikipedia's [MPI hello world example](https://en.wikipedia.org/wiki/Message_Passing_Interface#Example_program) saved as `wiki_mpi_example.c`, compile it first:

```bash
module load gcc/<version> openmpi/<version>
mpicc wiki_mpi_example.c -o hello.mpi
```

Save the batch script as `mpi.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=test_mpi
#SBATCH --output=mpi_%j.out
#
#SBATCH --ntasks=4
#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=500M

module load gcc/<version> openmpi/<version>

srun ./hello.mpi
```

Submit with `sbatch mpi.sh`. Once finished, `mpi_<job_id>.out` contains output similar to:

```text
0: We have 4 processors
0: Hello 1! Processor 1 reporting for duty
0: Hello 2! Processor 2 reporting for duty
0: Hello 3! Processor 3 reporting for duty
```

## Shared memory (OpenMP)

An OpenMP job runs one task (`--ntasks=1`) with multiple threads (`--cpus-per-task`) on a single compute node. Because `OMP_NUM_THREADS` defaults to `1`, export it from `$SLURM_CPUS_PER_TASK`.

To test with Wikipedia's [OpenMP hello world example](https://en.wikipedia.org/wiki/OpenMP#C) saved as `wiki_omp_example.c`, compile it with OpenMP enabled:

```bash
module load gcc/<version>
gcc -fopenmp wiki_omp_example.c -o hello.omp
```

Save the batch script as `openmp.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=test_omp
#SBATCH --output=omp_%j.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=500M

module load gcc/<version>
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

./hello.omp
```

Submit with `sbatch openmp.sh`. Once finished, `omp_<job_id>.out` contains output similar to (thread order may vary):

```text
Hello World from thread 0
Hello World from thread 3
Hello World from thread 1
Hello World from thread 2
There are 4 threads
```

## Hybrid MPI and OpenMP

Combine MPI processes (`--ntasks`) with OpenMP threads (`--cpus-per-task`) in a single allocation. Always load explicit versioned modules (check `module spider openmpi`) and set `OMP_NUM_THREADS`.

If your hybrid job spans multiple nodes, ensure total cores (`ntasks × cpus-per-task`) is an exact multiple of **64** on NT or **32** on OzSTAR and that `--cpus-per-task` evenly divides the node core count (see [Requesting Resources and Interactive Jobs](resources-and-interactive.md)).

Save as `hybrid.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=test_hybrid
#SBATCH --output=hybrid_%j.out
#
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=2G

module load gcc/<version> openmpi/<version>
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun ./my_hybrid_program
```

### Job array of hybrid jobs

To run multiple independent hybrid jobs across a parameter set, add `--array` and include `%A_%a` in `--output` (`%A` is the array Job ID; `%a` is the task index):

```bash
#!/bin/bash
#
#SBATCH --job-name=hybrid_array
#SBATCH --output=hybrid_%A_%a.out
#
#SBATCH --array=1-10
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=2G

module load gcc/<version> openmpi/<version>
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun ./my_hybrid_program "$SLURM_ARRAY_TASK_ID"
```

## Job arrays (embarrassingly parallel)

Job arrays submit many independent runs of the same script (for example, Monte Carlo ensembles, parameter sweeps, or batch file processing). The cluster limit is `MaxArraySize=2048` tasks per array (maximum array index `2047`, i.e. indices `0`–`2047`; see [Walltime and scheduler limits](resources-and-interactive.md#walltime-and-scheduler-limits)).

### Integer parameter sweep

Pass `$SLURM_ARRAY_TASK_ID` directly when your program accepts an integer index:

```bash
#!/bin/bash
#
#SBATCH --job-name=param_sweep
#SBATCH --output=sweep_%A_%a.out
#
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=1G
#SBATCH --array=1-8

srun ./my_program "$SLURM_ARRAY_TASK_ID"
```

### Processing files or custom parameter values

Bash arrays are **0-indexed** (`0` to `N-1`). Match `--array` to 0-based indices so you do not skip the first element or read past the end of the array.

For 8 files in `<path/to/data>`, use `--array=0-7`:

```bash
#!/bin/bash
#
#SBATCH --job-name=array_files
#SBATCH --output=array_files_%A_%a.out
#
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=1G
#SBATCH --array=0-7

FILES=(<path/to/data>/*)
srun ./my_program "${FILES[$SLURM_ARRAY_TASK_ID]}"
```

The same 0-based indexing applies to non-sequential parameter lists (here 7 values → `--array=0-6`):

```bash
#!/bin/bash
#
#SBATCH --job-name=array_params
#SBATCH --output=array_params_%A_%a.out
#
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=1G
#SBATCH --array=0-6

ARGS=(0.05 0.25 0.5 1 2 5 100)
srun ./my_program "${ARGS[$SLURM_ARRAY_TASK_ID]}"
```

:::{tip}
If you prefer 1-based array task IDs (for example, `--array=1-8`), subtract 1 before indexing a Bash array: `idx=$((SLURM_ARRAY_TASK_ID - 1))` and `"${FILES[$idx]}"`.
:::

## Packing short sub-tasks

Choose between job arrays and packed jobs based on sub-task duration:

- **Use a job array** (preferred in almost all cases) when each task runs longer than ~10 minutes, or when task durations vary widely. Job arrays schedule independently via backfill and avoid leaving cores idle while slow tasks finish.
- **Pack sub-tasks inside one allocation** only when you have hundreds or thousands of very short sub-tasks (each running a few minutes or less) of roughly uniform duration, where individual Slurm jobs would create excessive scheduler overhead.

:::{warning}
Never pass `--exclusive` to `sbatch` or `--gres=tmp:...` to `sbatch`/`srun` — both are rejected by Slurm. Request shared local scratch at the job level with `#SBATCH --tmp=<size>`, isolate each sub-task's temporary files in its own subdirectory under `$JOBFS`, and ensure the per-step `--mem` multiplied by concurrent steps does not exceed the job's total `--mem`.
:::

The example below allocates 8 cores and 2 GiB of RAM on a single node (`--nodes=1`), then uses `xargs` to run up to `$SLURM_NTASKS` (8) concurrent `srun --exact` steps at a time across 1,000 short inputs:

```bash
#!/bin/bash
#
#SBATCH --job-name=packed_tasks
#SBATCH --output=packed_%j.out
#
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=01:00:00
#SBATCH --mem=2G
#SBATCH --tmp=1G

seq 1 1000 | xargs -n 1 -P "$SLURM_NTASKS" \
    srun -n 1 --cpus-per-task=1 --mem=250M --exact ./my_program
```

To process a directory of files safely (including filenames with spaces), pair `find -print0` with `xargs -0`:

```bash
#!/bin/bash
#
#SBATCH --job-name=packed_files
#SBATCH --output=packed_files_%j.out
#
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=01:00:00
#SBATCH --mem=2G
#SBATCH --tmp=1G

find <path/to/data> -maxdepth 1 -type f -print0 | xargs -0 -n 1 -P "$SLURM_NTASKS" \
    srun -n 1 --cpus-per-task=1 --mem=250M --exact ./my_program
```

If you prefer GNU `parallel` (check availability with `module spider parallel`), you can replace the `xargs` line with:

```bash
parallel -j "$SLURM_NTASKS" \
    srun -n 1 --cpus-per-task=1 --mem=250M --exact ./my_program ::: {1..1000}
```

## Master/worker (`--multi-prog`)

Use `srun --multi-prog` for producer/consumer workflows where rank `0` runs a coordinator (master) program and the remaining ranks run worker programs.

Create a configuration file named `multi.conf`:

```text
0      echo I am the master
1-3    echo I am worker %t
```

Slurm replaces `%t` with each task's rank (`0` through `3`). Save the batch script as `master_worker.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=test_mw
#SBATCH --output=master_worker_%j.out
#
#SBATCH --ntasks=4
#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=200M

srun --multi-prog multi.conf
```

Submit with `sbatch master_worker.sh`. Once finished, `master_worker_<job_id>.out` contains lines similar to (order may vary):

```text
I am worker 2
I am worker 3
I am worker 1
I am the master
```

## GPU job

Submit GPU jobs from `tooarrana1`/`tooarrana2` (`nt.swin.edu.au`) for NT NVIDIA A100 GPUs, or from `farnarkle1`/`farnarkle2` (`ozstar.swin.edu.au`) for OzSTAR NVIDIA P100 GPUs. Request GPUs with `--gres=gpu:<n>` and do **not** set `--partition`.

Save as `gpu.sh`:

```bash
#!/bin/bash
#
#SBATCH --job-name=gpu_example
#SBATCH --output=gpu_%j.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --gres=gpu:1

module load <application>/<version>

./my_gpu_program input.dat
```

:::{tip}
Inspect live GPU nodes and memory ceilings before submitting with `sinfo -o "%P %c %m %G"`. You can also add `nvidia-smi` inside your batch script to log the assigned GPU model and driver version in `gpu_<job_id>.out`.
:::

## Interactive session

To test or debug interactively on a compute node, run `sinteractive` from the login node matching your target cluster (`tooarrana1`/`tooarrana2` for NT, `farnarkle1`/`farnarkle2` for OzSTAR):

```bash
sinteractive --ntasks=4 --time=00:20:00 --mem=4G
```

Interactive sessions are limited to short core-time allocations (see [Interactive jobs (`sinteractive` and `srun`)](resources-and-interactive.md#interactive-jobs-sinteractive-and-srun)). Run `sinteractive --help` (or `man srun`) to view all supported options.

## Next steps

- [Requesting Resources and Interactive Jobs](resources-and-interactive.md) — memory ceilings, multi-node core multiples, `$JOBFS`, and interactive limits.
- [Monitoring and Managing Jobs](monitoring.md) — inspect CPU, memory, and GPU efficiency once your job starts.
- [Slurm Command Reference](slurm-reference.md) — concise lookup of common Slurm commands and `#SBATCH` directives.
