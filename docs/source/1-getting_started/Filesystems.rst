.. highlight:: rst

File systems
============

The main filesystem is 19 Petabytes of diskspace in ``/fred``. This filesystem has more than 30 GB/s of aggregate bandwidth. It is a Lustre + ZFS filesystem with high performance, reliability, and redundancy.

There are a few other smaller filesystems in the cluster. Of these, ``/home`` is cluster-wide like ``/fred`` and ``$JOBFS`` is on SSDs in each compute node. ``/home`` is a Lustre + ZFS filesystem and ``$JOBFS`` is XFS.


Local disks
-----------

Each compute node has a local SSD (fast disk) that is accessible from batch jobs. If the I/O patterns in your workflow are inefficient on the usual cluster filesystems, then you should consider using these local disks.

The ``$JOBFS`` environment variable in each job points at a per-job directory on the local SSD. Space on local disks is requested from ``slurm`` with eg. ``#SBATCH --tmp=20GB``. The ``$JOBFS`` directory is automatically created before each job starts, and deleted after the job ends.

A typical workflow that uses local disks would be to copy tar files from ``/fred`` to ``$JOBFS``, untar, do processing on many small files using many IOPS, tar up the output, copy results back to ``fred``.

Alternativley, you may use it to write a large number of small files during your job, which you then pack into a tarball and copy back to ``/fred`` at the end of your job (See :ref:`optimizing writing <Writing>`).

Lustre
------

On OzSTAR, the two main cluster-wide directories are: ::

    /home/<username>

and ::

    /fred/<project_id>

``/fred`` is vastly bigger and faster in (almost) every way than ``/home``, but it is **NOT** backed up. ``/fred`` is meant for large data files and most jobs should be reading and writing to it.

.. warning::
    Since ``/fred`` is not backed up, it is unsuitable for long term data storage. Data loss due to hardware failure is unlikely, but possible. Accidentally deleted files cannot be recovered.

    The user is responsible for backing up any data that is important to an external location.

``/home`` is backed up. ``/home`` is intended for small source files and important scripts and input.

Typically project leaders will create directories for each of their members inside ``/fred/<project_id>`` (e.g. ``/fred/<project_id>/<username>``). If a user is a member of multiple projects then they will have access to multiple areas in ``/fred``.


Quota
^^^^^

Disk quotas are enabled on OzSTAR.

``/home`` has a per-user limit of 10GB blocks and 100,000 files. This cannot be increased. These numbers are set so that backups are feasible.

``/fred`` has a default per-project limit of 10TB blocks and 1M files. If you require additional storage, please contact hpc-support@swin.edu.au

.. note::
    Because of filesystem compression (see below), it is common to store more data than this and remain under quota. This is because quotas count only actual blocks used on disk.

To check your quota on any node, type: ::

    quota


Transparent Compression
^^^^^^^^^^^^^^^^^^^^^^^

The ``/fred`` and ``/home`` filesystems have transparent compression turned on. This means that all files (regardless of type) are internally compressed by the filesystem before being stored on disk, and are automatically uncompressed by the filesystem as they are read.

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
