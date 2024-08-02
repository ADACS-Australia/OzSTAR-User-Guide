.. highlight:: rst

Optimising Lustre I/O
=====================

The best way to get good performance to any filesystem (not just Lustre) is to do reads and writes in large chunks and to use large files rather than many small files. Performing many IOPS (input/output operations per second) should be avoided.

What is **“large”**?
For Lustre, reads and writes of >4MB are ideal. 10 MB and above is best. Small (eg. < 100 kB) reads and writes and especially 4k random writes should be avoided. These cause seeking and obtain low I/O performance from the underlying raids and disks. Small sequential reads are often optimised by read-ahead in block devices or Lustre or ZFS so may perform acceptably, but it's unlikely.

The best way to get high I/O performance from large parallel codes (eg. a checkpoint) is generally to read or write one large O(GB) file per process, or if the number of processes is very large, then one large file per node. This will send I/O to all or many of the Object Storage Targets (OSTs) that make up the ``/fred`` filesystem and can run at over 30 GB/s (not including speed-ups from transparent filesystem compression).

Each of the individual OSTs in the ``/fred`` filesystem is composed of 4 large raidz3's in a ZFS pool and is capable of several GB/s. Because each OST is large and fast there is no advantage in using Lustre striping.

What are IOPS?
--------------

IOPS are Input/Output Operations per Second. I/O operations are things like open, close, seek, read, write, stat, etc.. IOPS is the rate at which these occur.

High IOPS and small files tend to go hand in hand. Optimal cluster file sizes are usually between 10 MB and 100 GB. Using anything smaller than 10 MB files risks having its I/O time dominated by open()/close() operations (IOPS), of which there are a limited amount available to the entire file system.

A pathologically bad file usage pattern would be a code that accesses 100,000 files in a row, each of <8k in size. This will perform extremely badly on anything except a local disk. It is not an efficient usage model for a large shared supercomputer file system (see the :ref:`Local disks` section). Similarly, writing a code that has open()/close() in a tight inner loop will be dominated by the metadata operations to the Lustre MDSs (MetaData Servers), will perform badly, and will also impact the use of the cluster for all users because the MDS is a shared resource and can only do a finite number of operations per second (approx 100k).

Other things to avoid
---------------------

File lock bouncing is also an issue that can affect POSIX parallel file systems. This typically occurs when multiple nodes are appending to the same shared “log” file. By its very nature the order of the contents of such a file are undefined - it is really a “junk” file. However Lustre will valiantly attempt to interlace I/O from each appending node at the exact moment it writes, leading to a vast amount of “write lock bouncing” between all the appending nodes. This kills the performance of all the processes appending, and from the nodes doing the appending, and increases the load on the MDS greatly. Do not append to any shared files from multiple nodes.

In general a good rule of thumb is to not write at all to the same file from multiple nodes unless it is via a library like MPI IO.


Reading
-------

If you cannot avoid the **reading** of many small files, then you can reduce the number of IOPS and inodes by containerising your code and/or data.
This way the Lustre filesystem sees only a single large file (your container, which is just a read-only `SquashFS <https://docs.kernel.org/filesystems/squashfs.html>`_), even though underneath you're dealing with a large number of files.
See the section :ref:`Apptainer on OzSTAR` for more information on how to create and run a container.

If you only need to containerise your data, and not your code, then it's possible to manually create and mount a squashfs that holds just your data.
This is faster, albeit slightly more complicated, than simply unpacking a tarball to ``$JOBFS`` (see :ref:`Local disks`).

For example, to create a squashfs from a large number of small files in a directory, you can do

::

    $ ls training-data/
    file1 file2 file3 ... file9999

    $ mksquashfs training-data/ data.sqfs

Then, using `Linux namespaces <https://www.redhat.com/sysadmin/7-linux-namespaces>`_ and ``squashfuse`` you can mount the squashfs. The following is an example batch script that does this

::

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=1
    #SBATCH --job-name=example
    #SBATCH --time=0-00:00:30

    # load some modules...

    unshare --user --pid --map-root-user --fork --mount-proc <<EOF
        squashfuse inputs.squashfs /my/preferred/mountpoint/
        ls /my/preferred/mountpoint/
        # you can now access all the files, read-only: file1 file2 file3 ... file9999

        # run your code here...
    EOF

(You can shorten the unshare command to ``unshare -Uprf --mount-proc``).

Alternatively, if your code is containerised, you can **bind mount the squashfs directly into the container**.
(See :ref:`Binding the filesystem to a container`).

Writing
-------

If you cannot avoid the **writing** of a large number of small files, we recommend using ``$JOBFS`` (:ref:`local disks`).

Ensure that you request space on the local disk for your job with e.g. ``#SBATCH --tmp=20GB``. Then direct your code to write files to the path defined by ``$JOBFS``. At the end of your job, tar up the files and copy them back to ``/fred``.

The following is an example batch script that does this

::

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=1
    #SBATCH --job-name=example
    #SBATCH --time=0-00:00:30
    #SBATCH --tmp=20GB

    # load some modules...

    # create a directory on the local disk
    mkdir $JOBFS/data

    # run your code, directing output to $JOBFS
    ./mycode --output_dir=$JOBFS/data

    # tar up the files and copy it back to /fred
    cd $JOBFS
    tar -czf data.tar.gz ./data
    mv $JOBFS/data.tar.gz /fred/my/project/
