.. highlight:: rst

Slurm: Creating a job
==========================
A job is formed of two sections: **resource requests** and **job steps**. Resource requests involves specifying the required a number of CPUs/GPUs, expected job duration, amounts of RAM, disk space, and so on. Job steps involves describing what needs to be done (i.e. computing steps, which software to run, parameter space, etc.).

Typically, a job is created via a **submission script**: a shell script. For example, comments are prefixed with **SBATCH** at the beginning of a Bash script are understood by Slurm as parameters describing resource requests and other submissions options. A complete list of parameters can be obtained from the sbatch manual page (``man sbatch``).

.. important::

    The very first line of the submission file has to be the `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_ (e.g. ``#!/bin/bash``). Then, the next lines must be the **SBATCH** directives. Finally, you can input any other line.

The script itself is a job step. Other job steps are created with the ``srun`` command.

For instance, the following script, hypothetically named myjob.sh,

::

    #!/bin/bash
    #
    #SBATCH --job-name=test
    #SBATCH --output=res.txt
    #
    #SBATCH --ntasks=1
    #SBATCH --time=60:00
    #SBATCH --mem-per-cpu=200

    srun hostname
    srun sleep 60

would request one CPU for 60 minutes, and 200 MB of RAM, in the default queue. When started, the job would run a first job step ``srun hostname``, which will launch the UNIX command hostname on the node on which the requested CPU was allocated. Then, a second job step will start the ``sleep`` command. Note that the ``--job-name`` parameter lets give a meaningful name to the job and the ``--output`` parameter defines the file to which the output of the job must be sent.

Once the submission script is correct, you need to submit it to slurm through the ``sbatch`` command, which, upon success, responds with the ``jobid`` attributed to the job. (The ``%`` sign below is the shell prompt)

::

    % sbatch submit.sh
    sbatch: Submitted batch job 99999999

.. note::

    It is possible to submit a new job to the queue from an SBATCH script.

Job steps on the queue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once a job has been submitted to a queue with ``sbatch``, execution will follow these steps/states:

1. **PENDING**: The job then enters the queue in the PENDING state.
2. **RUNNING**: Once resources become available and the job has highest priority, an allocation is created for it and it goes to the RUNNING state.
3. If the job completes correctly, it goes to the **COMPLETED** state, otherwise, it is set to the **FAILED** state.


Querying Job State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is possible to query information about a job in near-realtime (memory consumption, etc.) with the ``sstat`` command, by introducing ``sstat -j jobid``. It is possible to select specific information to output with ``sstat`` via the ``--format`` parameter. Refer to the manpage for more information ``man sstat``.

The output file contains the result of the commands run in the script file. Following the previous example, it is possible to view its results with ``cat res.txt``. Slurm appends to the job output file while the job is running which makes it easy to see job progress.

.. note::

    The previous example illustrates a serial job running on a single CPU, and on a single node, and therefore does not take advantage of multi-processor nodes or multiple compute nodes available with a cluster.

Parallel jobs
----------------------------

Parallel job (e.g. tasks ran simultaneously) can be created via different methods:

- by running a multi-process program (`Single Process, Multiple Data (SPMD) <http://en.wikipedia.org/wiki/SPMD>`_ paradigm, e.g. with `MPI <http://en.wikipedia.org/wiki/Message_Passing_Interface>`_)
- by running a multi-threaded program (shared memory paradigm, e.g. with `OpenMP <http://en.wikipedia.org/wiki/OpenMP>`_ or `pthreads <http://en.wikipedia.org/wiki/Pthreads>`_)
- by running several instances of a single-threaded program (`Embarrassingly parallel paradigm <https://en.wikipedia.org/wiki/Embarrassingly_parallel>`__ or a *job array*)
- by running one master program controlling several slave programs (*master/slave* paradigm)

In the Slurm context, a task represents a **process**; a multi-process program is made of several tasks. By contrast, a multi-threaded program is composed of only one task, which uses several CPUs.

Tasks are requested/created with the ``--ntasks`` option, while CPUs, for the multithreaded programs, are requested with the ``--cpus-per-task`` option. Tasks cannot be split across several compute nodes, so requesting several CPUs with the ``--cpus-per-task`` option will ensure all CPUs are allocated on the same compute node. By contrast, requesting the same amount of CPUs with the --ntasks option may lead to several CPUs being allocated on several, distinct compute nodes.

When using OpenMP parallelisation, you will need to pass the number of OpenMP tasks through to the program by setting the environment variable ``OMP_NUM_THREADS``, for example

::

    export OMP_NUM_THREADS=16

This can be combined with Slurm's environment variable which provides the number of CPUs per task to automatically set the number of OpenMP tasks based on the resources requested:

::

    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

.. note::

    The default value is ``OMP_NUM_THREADS=1``

.. note::

    On OzSTAR, while a single node has 36-cores, usage is limited to 32-cores per node for a single job. This is due to the need for leaving cores free to communicate with GPUs.


For different parallel job scripts, see the :doc:`oz-slurm-examples` page.
