.. highlight:: rst

Job Queues
==========

The preferred method for utilising the supercomputer is through submitting batch jobs to the Slurm scheduling system which governs access to the compute nodes. The nodes are not available for direct login unless your job is running on it.

The basic goal of a queue system is to maximize utilisation of the supercomputer and to do this in a way that is fair to all users. The queue system on OzSTAR is `Slurm <https://slurm.schedmd.com>`__. Slurm is a resource manager, job scheduler, and much more. Slurm was first developed at the `Livermore Computing Center <https://hpc.llnl.gov/>`__, and has grown into a complete open-source software backed by a large community, commercially supported by the original developers, and used by many of the Top500 supercomputers. It is therefore worth learning its mechanisms.

Slurm Options
-------------
Options to Slurm can be specified on the ``sbatch`` or ``srun`` command lines like

::

    sbatch --time=1:00:00 ...

or in lines at the top of the batch script as ``#SBATCH --time=1:00:00``. In the examples below, we mostly use the command line versions for brevity, but typically these options will all be written into the top of your batch script. Your batch script is then submitted to Slurm with ``sbatch my_script``.

Memory Requests
---------------
You must request the amount of memory that your job needs.  The default allocation is ``100M`` per CPU core requested which is unlikely to be enough to achieve much and is intended to encourage you to pick a good value.  The more accurate your estimate is, the more likely your job is to be scheduled quickly as Slurm will be better able to fill up available slots in its schedule with it. Note that you should only request the amount of memory that you are going to use.

For instance if your job needs 2GB per node in total, then you would ask for ``--mem=2G``. If your job needs needs around 1GB per CPU core, then you would ask for ``--mem-per-cpu=1G``.

Slurm enforces this memory request by using the Linux kernels ``cgroup`` support which will limit the memory it can use on the node. If your job exceeds that value then the kernel will kill a process which will usually lead to the failure of your job.

Memory is the most commonly overrequested because users generally don't know how much memory their job requires. Although you may be able to make a good estimate for a self-authored code, we recommend determining memory usage via trial and error. Start with a generous request of 4000M/core, and then check the actual usage on the `Job monitor <https://supercomputing.swin.edu.au/monitor/>`_. Once the true maximum usage has been determined, set the request to 125% of the maximum. This leeway will prevent your job from crashing if a change results in a slightly different memory usage.

.. note::

	Unlike some other supercomputing clusters, a single node on OzSTAR and NT may run jobs submitted by more than one user. This optimises the usage and throughput of the entire system, but it relies on everyone submitting accurate resource requests. Requesting more memory than you need will unnecessarily block other users' jobs (and your own) from running. Please be respectful of other users on the system.

Although each node has a specific amount of RAM installed physically, not all of it is available to Slurm jobs. This is primarily because the operating system itself requires memory. If you ask for more memory than this then your job will be automatically redirected one of the high-memory nodes which have more memory available. However there are only few high memory nodes so your job throughput will be low.

+-----------------------------------+----------------------------------+----------+
| Node                              | Maximum requestable memory (MiB) | (GiB)    |
+===================================+==================================+==========+
| Skylake (regular)                 | 191,000 MiB                      | 186 GiB  |
+-----------------------------------+----------------------------------+----------+
| Skylake (high-memory)             | 375,000 MiB                      | 266 GiB  |
+-----------------------------------+----------------------------------+----------+
| Skylake (very-high-memory)        | 750,000 MiB                      | 732 GiB  |
+-----------------------------------+----------------------------------+----------+
| Milan (regular)                   | 256,000 MiB                      | 250 GiB  |
+-----------------------------------+----------------------------------+----------+
| Milan (high-memory)               | 1,024,000 MiB                    | 1000 GiB |
+-----------------------------------+----------------------------------+----------+
| Milan (GPU)                       | 512,000 MiB                      | 500 GiB  |
+-----------------------------------+----------------------------------+----------+
| Milan (GPU high-memory)           | 1,024,000 MiB                    | 1000 GiB |
+-----------------------------------+----------------------------------+----------+
| Trevor (high-memory)              | 29,000 MiB                       | 28 GiB   |
+-----------------------------------+----------------------------------+----------+

.. note::

	The default units for the memory request is in MiB. If you choose to specify "G" units, e.g. ``--mem=10G``, this is in units of GiB, equivalent to 1024 MiB.


Requesting GPUs
---------------
If your application uses GPUs then you will need to request them to be able to access them.  To request a GPU you need to ask for ``generic resources`` by doing ``--gres=gpu``.  You can request 2 GPUs on a node with ``gres=gpu:2``.  This will request will ensure that for each node you are allocated you will have sole access to that number of GPUs.  Access is controlled via the Linux kernel ``cgroup`` mechanism which locks out any other processes from accessing your allocated GPU.

On OzSTAR nodes, whilst we reserve 4 CPUs per node for GPU tasks we cannot currently guarantee they have optimal locality and so you may find performance varies across jobs depending on which core and which GPU you are allocated.

Interactive Jobs - Running a program on a compute node but with output on the login node
-----------------------------------------------------------------------------------------

If you need to run a program on a compute node that will ask questions, or you would like to watch its output in real time, then you can use the ``srun`` command to achieve this, in the same way you would use it to launch an MPI program from within a Slurm batch script.  To run an MPI program interactively you could do:

::

    srun --time=4:0:0 --cpus-per-task=4 --ntasks=4 --mem-per-cpu=2G ./my-interactive-mpi-program

You would then have to wait until the job started and then be able to interact with it as if you were running it on the login node.

.. note::
	Because NT and OzSTAR have different CPU architectures, ``srun`` must be invoked from a login node with a matching architecture. ie. Use ``tooarrana1/2`` for NT and ``farnarkle1/2`` for OzSTAR.

Interactive Jobs - Getting a shell prompt on a compute node
-----------------------------------------------------------
OzStar has no dedicated interactive nodes, instead you can request them using the ``sinteractive`` command which will give you a shell on a compute node as part of a job.  It takes all the usual options that the Slurm ``srun`` command takes to allow you to specify the run time of your job, how much memory it needs and how many cores it needs on the node. Again you will need to wait until the job this generates starts before being able to do anything.

::

    sinteractive --time=1:0:0 --mem=4g --cpus-per-task=4

.. note::
	Similarly to using ``srun``, Because NT and OzSTAR have different CPU architectures, ``sinteractive`` must be invoked from a login node with a matching architecture.

Interactive Jobs - Using X11 applications
-----------------------------------------
In both the above examples you can pass the ``--x11`` option to ``srun`` or ``sinteractive`` to request X11 forwarding.

.. note::
	This will not work if you try and run this inside of ``screen`` or ``tmux``.

Requesting Local Scratch Space
------------------------------
All jobs on OzStar get allocated their own private area on local disk which is pointed to by the environment variable ``$JOBFS``. These are cleaned up at the end of every job.  By default you get a ``250M`` allocation of space, to request more you need to ask for it with the ``--tmp`` option to ``sbatch``, so for example to request 4GB of local scratch disk space you would use ``--tmp=4G``.


Partitions
----------
Slurm on splits nodes into partitions (which can overlap) in order to give prioritisation and classification of nodes. Slurm will automatically direct jobs to the correct partition based on the requested resources, and which login node the job is submitted on.

.. note::
	Users should not manually specify a partition in their job scripts. Partitions are only used internally, and their names may change.
