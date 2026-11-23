# OzSTAR User Guide

Technical user guide for Swinburne's supercomputers — **Ngarrgu Tindebeek (NT)**, **OzSTAR**, and **Trevor** — covering accounts, access, storage, software, and running jobs with Slurm.

## New to OzSTAR?

Follow these five steps to get set up and run your first job:

1. Read [Policies](1-getting_started/Policies.rst) and review [Swinburne HPC Systems](getting-started/systems.md).
2. Request an account and join or create a project in [Accounts and Projects](getting-started/accounts.md).
3. Set up [Two-Factor Authentication (2FA)](getting-started/2fa.md) in the Accounts Portal before your first SSH login.
4. Connect via [SSH](access/ssh-access.md) and check [Filesystems and Storage](storage/filesystems.md).
5. Submit your first batch job with [Creating and Submitting Jobs](jobs/creating-jobs.md).

## Jump straight to a topic

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Access & Shell
:link: access/ssh-access
:link-type: doc

Connect over SSH, reuse connections, launch X11 or VNC sessions, configure restricted keys or AI coding tools, and manage your shell environment.
:::

:::{grid-item-card} Storage & Data
:link: storage/filesystems
:link-type: doc

Check `/home`, `/fred`, `/aphid`, `$JOBFS`, and `/datasets` quotas, transfer data via data-movers, and optimise Lustre I/O.
:::

:::{grid-item-card} Software & Containers
:link: software/modules
:link-type: doc

Load Lmod modules, build Python and Conda/Mamba environments, run Jupyter notebooks, and build or run Apptainer containers.
:::

:::{grid-item-card} Running Jobs
:link: jobs/creating-jobs
:link-type: doc

Write Slurm batch scripts, request CPUs, memory, GPUs, and interactive sessions, and adapt tested job templates.
:::

:::{grid-item-card} Monitoring & Reference
:link: jobs/monitoring
:link-type: doc

Track live job utilisation in the Web Job Monitor, inspect queues from the command line, and look up Slurm directives.
:::

:::{grid-item-card} Troubleshooting & Support
:link: help/faq
:link-type: doc

Diagnose common SSH, quota, and Slurm errors or send a complete support request to Swinburne HPC staff.
:::

::::

## External portals

- [Accounts Portal](https://supercomputing.swin.edu.au/account-management/) — apply for accounts, manage projects, reset passwords, and configure 2FA.
- [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) — inspect live CPU, memory, GPU, and I/O usage for running and past jobs.
- [Swinburne Supercomputing](https://supercomputing.swin.edu.au/) — facility overview, news, and merit allocation information.

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Getting Started

1-getting_started/Policies
getting-started/systems
getting-started/accounts
getting-started/2fa
:::

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Access & Shell

access/ssh-access
access/graphical-access
access/restricted-keys
access/ai-coding-tools
access/linux-environment
:::

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Storage & Data

storage/filesystems
storage/file-transfer
storage/optimising-lustre
:::

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Software

software/modules
software/python
software/notebooks
software/apptainer
software/apptainer-examples
:::

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Running Jobs

jobs/creating-jobs
jobs/resources-and-interactive
jobs/examples
jobs/monitoring
jobs/slurm-reference
jobs/ligo-reporting
:::

:::{toctree}
:maxdepth: 1
:hidden:
:caption: Help & Support

help/faq
help/support
:::
