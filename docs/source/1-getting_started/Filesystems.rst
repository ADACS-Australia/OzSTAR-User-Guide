.. highlight:: rst

File systems
============

The main filesystem is 19 Petabytes of diskspace in ``/fred``. This filesystem has more than 30 GB/s of aggregate bandwidth. It is a Lustre + ZFS filesystem with high performance, reliability, and redundancy.

There are a few other smaller filesystems in the cluster. Of these, ``/home`` is cluster-wide like ``/fred`` and ``$JOBFS`` is on SSDs in each compute node. ``/home`` is a Lustre + ZFS filesystem and ``$JOBFS`` is XFS.

We have recently added a new cluster-wide filesystem designed for I/O-intensive workloads, available at ``/aphid/scratch-3month/<username>``. Aphid has been built using repurposed hardware from NT. We have configured the filesystem for maximum resilience, including RAIDZ3 redundancy. However, as the underlying disks are older, users should be aware that long-term reliability may be lower than for the primary production filesystems.

Local disks
-----------

Each compute node has a local SSD (fast disk) that is accessible from batch jobs. If the I/O patterns in your workflow are inefficient on the usual cluster filesystems, then you should consider using these local disks.

The ``$JOBFS`` environment variable in each job points at a per-job directory on the local SSD. Space on local disks is requested from ``slurm`` with eg. ``#SBATCH --tmp=20GB``. The ``$JOBFS`` directory is automatically created before each job starts, and deleted after the job ends.

A typical workflow that uses local disks would be to copy tar files from ``/fred`` to ``$JOBFS``, untar, do processing on many small files using many IOPS, tar up the output, copy results back to ``fred``.

Alternatively, you may use it to write a large number of small files during your job, which you then pack into a tarball and copy back to ``/fred`` at the end of your job (See :ref:`optimizing writing <Writing>`).

Lustre
------

On OzSTAR, the three main cluster-wide directories are: ::

    /home/<username>

    /aphid/scratch-3month/<username>

and ::

    /fred/<project_id>

``/fred`` is vastly bigger and faster in (almost) every way than ``/home``, but it is **NOT** backed up. ``/fred`` is meant for large data files and most jobs should be reading and writing to it.

.. warning::
    Since ``/fred`` is not backed up, it is unsuitable for long term data storage. Data loss due to hardware failure is unlikely, but possible. Accidentally deleted files cannot be recovered.

    The user is responsible for backing up any data that is important to an external location.

``/home`` is backed up. ``/home`` is intended for small source files and important scripts and input.

Typically project leaders will create directories for each of their members inside ``/fred/<project_id>`` (e.g. ``/fred/<project_id>/<username>``). If a user is a member of multiple projects then they will have access to multiple areas in ``/fred``.

``/aphid/scratch-3month`` is designed for temporary, I/O-intensive workloads. It is not backed up, and data is subject to an expiry policy (see *scratch file expiration* below). The recommended workflow on ``/aphid/scratch-3month`` is to run jobs, copy any valuable outputs to ``/home`` or ``/fred``, and then remove unnecessary intermediate data (or allow it to expire).

Quota
^^^^^

Disk quotas are enabled on OzSTAR.

``/home`` has a per-user limit of 10GB blocks and 100,000 files. This cannot be increased. These numbers are set so that backups are feasible.

``/fred`` has a default per-project limit of 10TB blocks and 1M files. If you require additional storage, please contact hpc-support@swin.edu.au

``/aphid/scratch-3month`` currently has no enforced quota. This may be revisited if storage usage becomes imbalanced, or the filesystem is not used in accordance with its intended purpose.

.. note::
    Because of filesystem compression (see below), it is common to store more data than this and remain under quota. This is because quotas count only actual blocks used on disk.

To check your quota on any node, type: ::

    quota

Scratch file expiration
^^^^^^^^^^^^^^^^^^^^^^^

Data stored under ``/aphid/scratch-3month/<username>`` is subject to a 90-day expiry policy, based on the last access time of each file. Users are responsible for ensuring that any important data is copied to long-term storage (e.g. ``/home``, which is backed up, or ``/fred`` not backed up) before expiry.

.. warning::
    Do not modify file timestamps or otherwise attempt to circumvent the three-month retention policy. Retaining unnecessary data on the older ``/aphid`` hardware increases the risk of data loss and impacts the reliability of the filesystem for all users.

A summary of files approaching expiry will be displayed on the welcome node at login. Users can also monitor expiry periods using the nightly report, available from the command line: :: 

    scratch-report

Reports are only generated for users with files on ``/aphid/scratch-3month/<username>``, and they are retained for seven days. To view those available: ::

    scratch-report list

To inspect a specific report: ::

    scratch-report show <report_file>

Transparent Compression
^^^^^^^^^^^^^^^^^^^^^^^

The ``/fred``, ``/aphid/scratch-3month`` and ``/home`` filesystems have transparent compression turned on. This means that all files (regardless of type) are internally compressed by the filesystem before being stored on disk, and are automatically uncompressed by the filesystem as they are read.

.. note::
    This means that you will not save diskspace if you gzip your files, because they are already compressed.

For example, a highly compressible file like a typical ASCII input file:
::

    % ls -ls input
    1 -rw-r--r-- 1 root root 39894 Mar  5 17:36 input

the file is ~40KB in size, but it uses less than 1KB on disk (the first column).

For a typical binary output file that is somewhat compressible:
::

    % ls -lsh output
    7.8M -rw-rw-r-- 1 root root 33M Feb 20 18:25 output

so 7.8MB of space on disk is used to store this 33MB file.

This means that although the nominal capacity of ``/fred`` is ~5 PiB (output from ``df`` is somewhat pessimistic), the amount of data that can be stored is greater. How much greater depends upon the compressibility of typical data.

.. note::
    If you are transferring files over the network to other machines then it would still make sense to have your files compressed (gzip, bzip, xz etc.) in order to minimise both network bandwidth and diskspace used at the other end. But internally to the supercomputer there is no need to compress data. Doing so is fine, but unnecessary - it will just result in the data being slightly larger because it is compressed twice by slightly different algorithms.
