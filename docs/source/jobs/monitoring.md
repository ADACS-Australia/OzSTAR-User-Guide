# Monitoring and Managing Jobs

Track queued, running, and completed jobs on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor using the Web Job Monitor and Slurm command-line tools, and cancel jobs when needed.

## Web Job Monitor

The [Swinburne HPC Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) displays live CPU, memory, and GPU utilisation graphs for your jobs in a web browser. Check it whenever you run a new workflow to verify your code uses its allocated resources efficiently.

:::{warning}
Do not run `squeue` in tight polling loops (for example, `watch squeue` or repeated rapid script queries). Frequent polling places heavy load on the Slurm scheduler and slows down the cluster for all users. Use the [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) for real-time updates instead.
:::

### Checking active jobs

1. Select your username (abbreviated to the first 3 letters) from the left-hand list.
2. Review your active jobs in the middle column (showing Job ID, job name, and elapsed time) and select a job.
3. Inspect the graphs in the right-hand column:
   - The **upper section** shows resources used exclusively by your job.
   - The **lower section** shows total resources used across the entire compute node by your job and all other jobs sharing that node.

The Job Monitor automatically flags jobs that are not fully utilising their allocated resources with underutilisation alerts (highlighted in red). If you see an underutilisation alert, reduce your requested CPUs, memory, or GPUs in future submissions or investigate efficiency issues in your code (see [Policies](../1-getting_started/Policies.rst) and [User Support](../help/support.md)).

### Reviewing recent jobs (`Past` tab)

Open the **Past** tab to view a 24-hour timeline of overall cluster usage. Click any point along the timeline to inspect a snapshot of the system at that time, and enter your username in the filter box to see how many of your jobs were running or to find jobs that finished within the past 24 hours.

### Finding backfill slots (`Future` tab)

Open the **Future** tab to inspect available **backfill** slots — gaps in the schedule where smaller or shorter jobs can start immediately without delaying higher-priority queued jobs.

Each bar on the graph represents a backfill slot: the horizontal axis shows available CPU cores and the vertical axis shows available walltime. For example, a 4-core slot lasting 30 minutes means a job requesting up to 4 cores and up to 30 minutes may start immediately.

### Inspecting processes on a compute node with `htop`

While your job is in the `RUNNING` state, you can connect via SSH from a login node to the allocated compute node and inspect live processes with `htop`:

```bash
ssh <compute_node>
htop -u <username>
```

Direct SSH access to a compute node is allowed only while you have an active job running on that node.

## Command-line tools

You can also inspect cluster availability, backfill slots, job priority, and accounting history directly from the login nodes.

### Cluster status and backfill

Display cluster resource allocation status (detailed with `-v`, or a compact summary with `-s`):

```bash
qinfo -v
qinfo -s
```

List available backfill slots:

```bash
showbf
```

Check a compact standard Slurm summary of partition availability, time limits, and node counts (`Allocated/Idle/Other/Total`) with `sinfo -s`:

```bash
sinfo -s
```

Illustrative output on NT (`milan` is marked with `*` as the default partition for NT login nodes; remember that partitions are routed internally and should not be specified with `--partition`):

```text
PARTITION   AVAIL  TIMELIMIT   NODES(A/I/O/T) NODELIST
milan*         up 7-00:00:00     120/20/0/140 dave[1-140]
milan-gpu      up 7-00:00:00       16/4/0/20  gina[1-20]
skylake        up 7-00:00:00       80/20/0/100 john[1-100]
```

To inspect per-node core counts, requestable memory ceilings, and GPUs:

```bash
sinfo -o "%P %c %m %G"
```

For detailed node-by-node output (including `CPUS`, `MEMORY`, `TMP_DISK`, `WEIGHT`, `AVAIL_FE`, and `REASON` if a node is offline), run `sinfo -N -l`. See `man sinfo` for custom `--format` fields.

### Job status, priority, and accounting

List your own running (`R`) and pending (`PD`) jobs (using `--me` keeps output focused on your account):

```bash
squeue --me
```

Illustrative output:

```text
JOBID    PARTITION NAME   USER        ST  TIME  NODES NODELIST(REASON)
12345678 milan     sim1   <username>   R  12:04     1 dave42
12345679 milan     sim2   <username>  PD   0:00     2 (Resources)
12345680 milan     sim3   <username>  PD   0:00     1 (Priority)
```

For running jobs, `NODELIST(REASON)` shows the allocated compute nodes. For pending jobs, it shows why the job is waiting — for example, `(Resources)` when matching free resources are not yet available, or `(Priority)` when higher-priority jobs are ahead in the queue. You can filter `squeue` with flags such as `--states=R`, `--states=PD`, or `--job=<job_id>`.

Check scheduling priority components for a pending job (customisable with `--format`):

```bash
sprio -j <job_id>
```

Inspect near-real-time resource usage of a **running** job with `sstat` (see `man sstat` for `--format` fields) or the cluster helper `sjob`. Pass `-a` (`--allsteps`) to include all running steps (including the `.batch` step for jobs that do not use `srun`), or query a specific step ID such as `<job_id>.batch` or `<job_id>.<step_id>`:

```bash
sstat -a -j <job_id> --format=JobID,MaxRSS,AveCPU,MaxDiskRead,MaxDiskWrite
sstat -j <job_id>.batch --format=JobID,MaxRSS,AveCPU,MaxDiskRead,MaxDiskWrite
sjob <job_id>
```

Review accounting history, exit codes, and peak memory for **completed or failed** jobs with `sacct` or `jobreport`:

```bash
sacct -j <job_id> --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS
jobreport <job_id>
```

### Cancelling and modifying jobs

Cancel a single job by Job ID, or cancel your jobs matching a job name (always scope `--name` with `--me` or `-u <username>`):

```bash
scancel <job_id>
scancel -u <username> --name=<job_name>
```

Cancel all of your jobs:

```bash
scancel -u <username>
```

Cancel only your pending (`PD`) jobs while leaving running jobs untouched:

```bash
scancel -u <username> -t PD
```

:::{important}
`scontrol update` is disabled for user jobs on NT, OzSTAR, and Trevor. To change the resources, walltime, or account of a pending job, cancel it with `scancel <job_id>`, edit your batch script, and resubmit with `sbatch`.
:::

## Next steps

- [Slurm Command Reference](slurm-reference.md) — concise lookup tables for Slurm commands and `#SBATCH` directives.
- [Requesting Resources and Interactive Jobs](resources-and-interactive.md) — refine memory, CPU, or walltime requests based on Job Monitor data.
- [Frequently Asked Questions](../help/faq.md) — troubleshoot common job rejections and errors.
