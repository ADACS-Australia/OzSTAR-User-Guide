# Swinburne HPC Systems

Swinburne operates three compute clusters — **Ngarrgu Tindebeek (NT)**, **OzSTAR**, and **Trevor** — plus dedicated **data-mover** nodes for file transfers. All systems run AlmaLinux (run `cat /etc/os-release` to inspect the exact OS version) and share the same accounts, project directories, and Lustre storage.

## System overview

| System | Login / submit host | Architecture and role | Compute internet |
| --- | --- | --- | --- |
| **Ngarrgu Tindebeek (NT)** | `nt.swin.edu.au` (`tooarrana1/2`) | AMD EPYC (Milan) CPU, high-memory, and A100 GPU compute | No |
| **OzSTAR** | `ozstar.swin.edu.au` (`farnarkle1/2`) | Intel Xeon (Skylake) CPU, high-memory, and P100 GPU compute | No |
| **Trevor** | `trevor` *(jump from NT or OzSTAR)* | Private cloud (virtual machine) Intel (Haswell) nodes for low-resource jobs | Yes |
| **Data-movers** | `data-mover01.hpc.swin.edu.au`, ... | Dedicated nodes for external data transfers (interactive or batch) | Yes |

All clusters and data-movers share `/home`, `/fred`, and `/aphid` storage as well as the same account and project management system. See [Filesystems and Storage](../storage/filesystems.md) for storage paths and limits.

## Ngarrgu Tindebeek (NT)

Ngarrgu Tindebeek (NT) is Swinburne's primary high-performance compute cluster, interconnected with 200 Gbps NVIDIA Quantum-2 NDR InfiniBand.

- **Login / submit nodes:** `nt.swin.edu.au` (round-robin to `tooarrana1.hpc.swin.edu.au` and `tooarrana2.hpc.swin.edu.au`).
- **Standard CPU nodes:** Dual 32-core AMD EPYC 7543 CPUs (64 cores per node) with NVMe SSD local scratch (`$JOBFS`).
- **High-memory CPU nodes:** Same 64-core AMD EPYC architecture with expanded RAM and NVMe SSD local scratch.
- **GPU nodes:** 64-core AMD EPYC nodes equipped with 4× NVIDIA A100 80 GB GPUs per node and NVMe SSD local scratch.

## OzSTAR

OzSTAR provides Intel Xeon compute capacity and NVIDIA P100 GPUs, interconnected with 100 Gbps Intel Omni-Path.

- **Login / submit nodes:** `ozstar.swin.edu.au` (round-robin to `farnarkle1.hpc.swin.edu.au` and `farnarkle2.hpc.swin.edu.au`).
- **Standard compute nodes:** Dual 18-core Intel Xeon Gold 6140 CPUs (up to 32 requestable cores per node), SSD local scratch (`$JOBFS`), and 2× NVIDIA P100 12 GB GPUs per node.
- **High-memory compute nodes:** Same CPU and GPU architecture with expanded RAM and NVMe SSD local scratch.

## Trevor

Trevor is a private cloud (virtual machine) compute cluster built for jobs with low resource requirements and tasks that require external internet access from compute nodes.

- **Login / submit node:** `trevor` — reachable only by jumping via SSH from an NT or OzSTAR login node (see [Connecting via SSH](../access/ssh-access.md)).
- **Compute nodes:** 12-core Intel (Haswell) CPUs with modest RAM, local SSD scratch, and outbound internet access.

## Data-movers

Dedicated data-mover nodes (such as `data-mover01.hpc.swin.edu.au`; inspect live nodes with `sinfo -s -p datamover`) handle file transfers to and from Swinburne HPC storage — both interactively and via batch transfer jobs — so large transfers do not slow down shared login nodes. See [Transferring Files](../storage/file-transfer.md) for recommended `rsync` commands.

## Choosing a cluster

Jobs are automatically queued to the cluster whose login node you submit from:

- Submit from `tooarrana1` or `tooarrana2` to run on **NT**.
- Submit from `farnarkle1` or `farnarkle2` to run on **OzSTAR**.
- Submit from `trevor` to run on **Trevor**.

Do not set `--partition` in your Slurm scripts; partition routing is managed automatically based on your submit node and resource requests (see [Creating and Submitting Jobs](../jobs/creating-jobs.md)).

### Checking live capacity and memory ceilings

Because installed physical RAM includes overhead reserved for the operating system, the requestable memory per node is lower than the installed total. See [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) for requestable memory ceilings, core-multiple rules, and walltime limits.

To check live cluster allocation status, backfill slots, and partition summaries from any login node, run:

```bash
qinfo -v     # detailed cluster allocation status (or qinfo -s for a compact summary)
showbf       # available backfill slots
sinfo -s     # compact Slurm partition summary
```

### Internet access on compute nodes

Compute nodes on **NT** and **OzSTAR** are isolated from external networks by design to ensure reliable, uninterrupted computation. Stage any required external data into `/fred` or `/home` before submitting jobs. If your workflow needs automated downloads from external servers, run the transfer step on **Trevor** and chain downstream NT or OzSTAR jobs using Slurm dependencies.

## Porting between clusters

Although NT, OzSTAR, Trevor, and the data-movers all run **AlmaLinux** (binary-compatible with Red Hat Enterprise Linux) and share the same `/home` and `/fred` filesystems, each cluster uses a different CPU architecture.

:::{important}
Software modules, compiled binaries, and Python or Conda environments are built specifically for the CPU architecture of each cluster. A binary or environment built on OzSTAR will not reliably run on NT or Trevor (and vice versa).
:::

### Recompiling binaries

Log in to the target cluster's login node (for example, `nt.swin.edu.au` for NT or `ozstar.swin.edu.au` for OzSTAR), load the matching compiler and library modules on that cluster, and recompile your code from source. Store cluster-specific build outputs in separate directories so they do not overwrite one another on shared `/fred` or `/home` storage.

### Recreating Python and Conda environments

Recreate virtual environments and Conda/Mamba environments directly on the cluster where your jobs will run.

::::{tab-set}

:::{tab-item} Python venv
1. On the **source cluster**, activate your existing virtual environment and export its package list:

   ```bash
   pip freeze > requirements.txt
   ```

2. Log in to the **target cluster**, load your Python module, create a fresh virtual environment, and install the exported packages:

   ```bash
   pip install -r requirements.txt
   ```
:::

:::{tab-item} Conda / Mamba
1. On the **source cluster**, activate your existing environment and export its specification:

   ```bash
   conda env export > environment.yml
   ```

2. Log in to the **target cluster**, load the `mamba` module (`conda` is an alias for `mamba`), and recreate the environment:

   ```bash
   conda env create -f environment.yml
   ```
:::

::::

See [Python and Conda](../software/python.md) for full setup instructions and home-quota tips.

### OpenMP thread count

`OMP_NUM_THREADS=1` is set by default on all nodes so single-core jobs do not accidentally spawn excess threads. If your application uses OpenMP multithreading, set `OMP_NUM_THREADS` explicitly in your batch script to match `--cpus-per-task` (see [Parallel job models](../jobs/creating-jobs.md#parallel-job-models)).

## Next steps

- [Accounts and Projects](accounts.md) — apply for an account and join or create a project.
- [Connecting via SSH](../access/ssh-access.md) — connect to NT, OzSTAR, Trevor, and the data-movers.
- [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) — check requestable RAM ceilings, GPU requests, and Slurm limits.
