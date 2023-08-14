.. highlight:: rst

File Transfer
======================================================

In order to transfer files to and from the supercomputer, an SSH-based file transfer utility is required. There are a variety of Options that you can use.

.. note::

    If you are using Windows Subsystem for Linux, we recommend that you follow the instructions for Linux. The Linux utilities are generally superior to the Windows equivalents, and are more widely supported.

+------------------+---------------------------------------------------------------------------------------------------+
| Operating System | Program                                                                                           |
+------------------+---------------------------------------------------------------------------------------------------+
| Mac and Linux    | * `rsync <https://linux.die.net/man/1/rsync>`_ a powerful tool for transferring multiple files,   |
|                  |   with the ability to compare the source and destination and only send changes.                   |
|                  | * `scp (secure copy) <http://www.computerhope.com/unix/scp.htm>`_, a simple file transfer tool    |
+------------------+---------------------------------------------------------------------------------------------------+
| Windows          | * `WinSCP <http://winscp.net/eng/index.php>`_ is a graphical interface for transferring files     |
+------------------+---------------------------------------------------------------------------------------------------+


Copying a file or directory via SSH
---------------------------------------

The best way to copy a file to or from the supercomputer is to use the ``rsync`` command. ``rsync`` is preferred over ``scp`` because it designed to handle multiple files, and because it preserves permissions on directories.

.. note::

    Please use the data-mover nodes (``data-mover[01-04]``) instead of the login nodes for file transfers. The login nodes are shared between all users, who may be running tests or compiling code, whereas the data-movers are dedicated to file transfers. You can access the data-mover nodes externally by their addresses: data-mover[01-04].hpc.swin.edu.au

**Copying a local file to the OzSTAR supercomputer**::

    rsync -avPxH --no-g --chmod=Dg+s <local files and dirs> username@data-mover01.hpc.swin.edu.au:/fred/<project dir>/<somewhere>/

rsync has many options, but these are the recommendations. Please refer to rsync's man page for more information::

    -a, --archive    archive mode; equals -rlptgoD (no -H,-A,-X)
    -v, --verbose               increase verbosity
    -P                          same as --partial --progress
    -x, --one-file-system       don't cross filesystem boundaries
    -H, --hard-links            preserve hard links
    -g, --group                 preserve group
    --chmod=CHMOD           affect file and/or directory permissions

You can also copy a file from the supercomputer to your local machine (i.e. **download**) by swapping the source and destination arguments::

    rsync -avPxH --no-g --chmod=Dg+s username@data-mover01.hpc.swin.edu.au:/fred/<project dir>/<somewhere>/ <local destination>

.. note::

    When transferring large files, it may be useful to use the ``-z`` option of ``rsync`` to first compress the file, send it, and then decompress it. This is especially useful if your network connection is slow.

Resuming interrupted transfers
--------------------------------

If a transfer is interrupted, you might end up with part of the files being transferred. Rather than restarting the transfer from scratch, rsync will compare the **source** and **destination** directories and only transfer what needs to be transferred (missing files, modified files, etc.). Simply run the rsync command again (with the same source and destination arguments) to resume the transfer.

Transferring code
----------------------
The best way to transfer code from one computer to another is to host the code in a *source code repository* using a *versioning system* such as `git <https://www.git-scm.com>`__ and clone the repository to the supercomputer.

Synchronising with a local directory
--------------------------------------------
If you want to keep two directories (one on your local computer, and one on the supercomputer) in sync, you can do that with rsync using its ``--delete`` option. But that is only one-way so you need to really think in what direction you do it, and it does not scale beyond two synchronized directory trees.

.. warning::
    Please note that the supercomputer is **NOT** a place to use as a backup for your laptop or workstation. Storage on the Lustre file system is expensive to maintain, and must not be used for purposes unrelated to compute jobs.
