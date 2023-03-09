.. highlight:: rst

Slurm: script examples
==================================

Message passing example (MPI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    #!/bin/bash
    #
    #SBATCH --job-name=test_mpi
    #SBATCH --output=res_mpi.txt
    #
    #SBATCH --ntasks=4
    #SBATCH --time=10:00
    #SBATCH --mem-per-cpu=100

    module load gcc/6.4.0
    module load openmpi/3.0.0
    srun hello.mpi

Request four cores on the cluster for 10 minutes, using 100 MB of RAM per core. Assuming ``hello.mpi`` was compiled with MPI support, ``srun`` will create four instances of it, on the nodes allocated by Slurm.

You can try the above example by downloading the `example hello world program from Wikipedia <http://en.wikipedia.org/wiki/Message_Passing_Interface#Example_program>`_ (for example, you can name it wiki_mpi_example.c), and compiling it with
::

    module load gcc/6.4.0
    module load openmpi/3.0.0
    mpicc wiki_mpi_example.c -o hello.mpi

The ``res_mpi.txt`` file should look something like this:
::

    0: We have 4 processors
    0: Hello 1! Processor 1 reporting for duty
    0: Hello 2! Processor 2 reporting for duty
    0: Hello 3! Processor 3 reporting for duty

Shared memory example (OpenMP)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    #!/bin/bash
    #
    #SBATCH --job-name=test_omp
    #SBATCH --output=res_omp.txt
    #
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=4
    #SBATCH --time=10:00
    #SBATCH --mem-per-cpu=100

    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    ./hello.omp

The job will be run in an allocation where four cores have been reserved on the same compute node.

You can try it by using the `hello world program from Wikipedia <http://en.wikipedia.org/wiki/Openmp#C>`_ (for example, you can name it  ``wiki_omp_example.c``) and compiling it with
::

    gcc -fopenmp wiki_omp_example.c -o hello.omp

The ``res_omp.txt`` file should contain something like
::

    Hello World from thread 0
    Hello World from thread 3
    Hello World from thread 1
    Hello World from thread 2
    There are 4 threads

Embarrassingly parallel example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This setup is useful for problems based on random draws (e.g. Monte-Carlo simulations). In such cases, you can have four programs drawing 1000 random samples and combining their output afterwards (with another program) you get the equivalent of drawing 4000 samples.

Another typical use of this setting is **parameter sweep**. In this case the same computation is carried on several times by a given code, differing only in the initial value of some high-level parameter for each run. An example could be the optimisation of an integer-valued parameter through range scanning:

::

    #!/bin/bash
    #
    #SBATCH --job-name=test_emb_arr
    #SBATCH --output=res_emb_arr.txt
    #
    #SBATCH --ntasks=1
    #SBATCH --time=10:00
    #SBATCH --mem-per-cpu=100
    #
    #SBATCH --array=1-8

    srun ./my_program $SLURM_ARRAY_TASK_ID

In this configuration, the command ``my_program`` will be run eight times, creating eight distinct jobs, each time with a different argument passed with the environment variable defined by slurm **SLURM_ARRAY_TASK_ID** ranging from 1 to 8.

The same idea can be used to process several data files. To do so, we must pass a different input files to different instances of the program by setting the value of the ``$SLURM_*`` environment variable. For instance, assuming there are exactly eight files in ``/path/to/data`` we can create the following script:

::

    #!/bin/bash
    #
    #SBATCH --job-name=test_emb_arr
    #SBATCH --output=res_emb_arr.txt
    #
    #SBATCH --ntasks=1
    #SBATCH --time=10:00
    #SBATCH --mem-per-cpu=100
    #
    #SBATCH --array=1-8

    FILES=(/path/to/data/*)

    srun ./my_program ${FILES[$SLURM_ARRAY_TASK_ID]}

In this case, eight jobs will be submitted, each with a different filename given as an argument to ``my_program`` defined
in the array FILES[].

Note that the same recipe can be used with a numerical argument that is not simply an integer sequence, by defining an array ARGS[] containing the desired values:

::

    ARGS=(0.05 0.25 0.5 1 2 5 100)

    srun ./my_program ${ARGS[$SLURM_ARRAY_TASK_ID]}

.. Warning::

    If the running time of your program is small (i.e. ten minutes or less), creating a job array will incur a lot of overhead and you should consider *packing* your jobs.

Packed jobs example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``srun`` command has the ``--exclusive`` argument that allows scheduling independent processes inside a Slurm job allocation. As stated in the documentation:

| *This option can also be used when initiating more than one job step within an*
| *existing resource allocation, where you want separate processors to be*
| *dedicated to each job step. If sufficient processors are not available to*
| *initiate the job step, it will be deferred. This can be thought of as providing*
| *a mechanism for resource management to the job within it's allocation.*
|

As an example, the following job submission script will ask Slurm for 8 CPUs, then it will run the ``myprog`` program 1000 times with arguments passed from 1 to 1000. But with the ``-n1 --exclusive`` option, it will ensure that at any point in time, only 8 instances are effectively running, each being allocated one CPU.

::

    #! /bin/bash
    #
    #SBATCH --ntasks=8
    for i in {1..1000}
    do
       srun -n1 --exclusive ./myprog $i &
    done
    wait

It is possible to replace the ``for``-loop with GNU ``parrallel`` if available:

::

    parallel -P $SLURM_NTASKS srun  -n1 --exclusive ./myprog ::: {1..1000}

Similarly, many files can be processed with one job submission script. The following script will run ``myprog`` for every file in ``/path/to/data``, but maximum 8 at a time, and using one CPU per task.

::

    #! /bin/bash
    #
    #SBATCH --ntasks=8
    for file in /path/to/data/*
    do
       srun -n1 --exclusive ./myprog $file &
    done
    wait

Similarly as with ``parallel``, the ``for``-loop can be replaced with another command, ``xargs``:

::

    find /path/to/data -print0 | xargs -0 -n1 -P $SLURM_NTASKS srun -n1 --exclusive ./myprog

Master/slave program example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    #!/bin/bash
    #
    #SBATCH --job-name=test_ms
    #SBATCH --output=res_ms.txt
    #
    #SBATCH --ntasks=4
    #SBATCH --time=10:00
    #SBATCH --mem-per-cpu=100

    srun --multi-prog multi.conf

With file ``multi.conf`` being, for example, as follows
::

    0      echo I am the Master
    1-3    echo I am slave %t

The above instructs Slurm to create four tasks (or processes), one running ``echo 'I am the Master'``, and the other 3 running ``echo I am slave %t``. The ``%t`` placeholder will be replaced with the task id. This is typically used in a **producer/consumer** setup where one program (the master) create computing tasks for the other program (the slaves) to perform.

Upon completion of the above job, file res_ms.txt will contain
::

    I am slave 2
    I am slave 3
    I am slave 1
    I am the Master

although not necessarily in the same order.

Hybrid jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can mix multi-processing (MPI) and multi-threading (OpenMP) in the same job, simply like this:
::

    #! /bin/bash
    #
    #SBATCH --ntasks=8
    #SBATCH --cpus-per-task=4
    module load OpenMPI
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    srun ./myprog

or even a job array of hybrid jobs:
::

    #! /bin/bash
    #
    #SBATCH --array=1-10
    #SBATCH --ntasks=8
    #SBATCH --cpus-per-task=4
    module load OpenMPI
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    srun ./myprog $SLURM_ARRAY_TASK_ID

GPU jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some clusters have a GPU. To request one or more GPUs, there is need to set ``env`` directories.

To see the if the cluster have a GPU check the generic resources of the computes nodes.

::

    # sinfo  -o "%P %.10G %N"
    PARTITION       GRES NODELIST
    skylake      gpu:1 lmPp[001-003]

The slurm command shows 3 nodes with GPU in the post processing partition.

If you want to claim a GPU for your job, you need to specify the GRES (`Generic Resource Scheduling <http://slurm.schedmd.com/gres.html>`_) parameter in your job script. Please note that GPUs are only available in a specific partition whose name depends on the cluster.

::

    #SBATCH --partition=skylake
    #SBATCH --gres=gpu:1

A sample job file requesting a node with a GPU could look like this:

::

    #!/bin/bash
    #SBATCH --job-name=example
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --time=1:00:00
    #SBATCH --mem-per-cpu=1000
    #SBATCH --partition=skylake
    #SBATCH --gres=gpu:1

    module load application/version

    myprog input.fits

.. _interactive_jobs:

Interactive jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slurm jobs are normally batch jobs in the sense that they are run unattended. If you want to have a direct view on your job, for tests or debugging, you have two options.

If you need simply to have an interactive Bash session on a compute node, with the same environment set as the batch jobs, run the following command:

::

    srun --pty bash

Doing that, you are submitting a 1-CPU, default memory, default duration job that will return a Bash prompt when it starts.

If you need more flexibility, you will need to use the `salloc <https://slurm.schedmd.com/salloc.html>`_ command. The ``salloc`` command accepts the same parameters as ``sbatch`` as far as resource requirement are concerned. Once the allocation is granted, you can use ``srun`` the same way you would in a submission script.
