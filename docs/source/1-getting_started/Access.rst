.. highlight:: rst

Access to the supercomputer
============================

Access Ngarrgu Tindebeek
------------------------

Access to the supercomputer is available through Secure Shell (SSH) to nt.swin.edu.au for all users. i.e:
::

    ssh [your-username]@nt.swin.edu.au

.. important::

    After logging in you will be assigned to one of the two login nodes: ``tooarrana1`` or ``tooarrana2``.

From these nodes you can submit jobs to the queue nodes using `Slurm <https://slurm.schedmd.com>`__. You may also use the login nodes as interactive nodes to run short jobs directly, compile code, or test your application.

From each of ``tooarrana1/2`` you can access the other with ``ssh t1`` or ``ssh t2``. ``tooarrana1/2`` are also available for direct login via eg. ``ssh [your-username]@tooarrana1.hpc.swin.edu.au``.

From ``tooarrana1/2`` you can also SSH into ``farnarkle1/2``, the login nodes for the previous supercomputer OzSTAR.

.. note::
    Do not use these login nodes to run long jobs or jobs with big computational requirements. Running such jobs in interactive mode can be done by requesting interactive nodes from the queue.

.. tip::
    If you want to avoid having to type the rather long ``[your-username]@ozstar.swin.edu.au`` every time you want to connect to the supercomputer, you can set a shortcut in your `SSH config <https://linuxize.com/post/using-the-ssh-config-file/>`_.

    For example, you can set the following in ``~/.ssh/config``:

    ::

        Host nt
            HostName nt.swin.edu.au
            User your-username

    Once set, you can use this shortcut to SSH into the supercomputer. The following commands will produce the same outcome:

    **Connect to supercomputer**::

        ssh [your-username]@nt.swin.edu.au

        ssh nt

    **Copy a local file to supercomputer**::

        scp myfile.txt [your-username]@nt.swin.edu.au:path/to/location/

        scp myfile.txt nt:path/to/location/


Client Requirements
--------------------

Terminal
^^^^^^^^

A terminal is required to access OzSTAR via Secure Shell (SSH) and issue command line instructions.

+------------------+------------------------------------------------------------------------------------------------------------+
| Operating System | Terminal                                                                                                   |
+==================+============================================================================================================+
| Mac              | Available by default via Applications > Utilities > Terminal                                               |
+------------------+------------------------------------------------------------------------------------------------------------+
| Linux            | Available by default                                                                                       |
+------------------+------------------------------------------------------------------------------------------------------------+
| Windows          | The recommended method is to use the Windows Subsystem for Linux (WSL). More information available at the  |
|                  | `Microsoft documentation <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__. If you are using |
|                  | an older version of Windows that does not provide WSL, you will need to install                            |
|                  | `PuTTY <https://www.putty.org>`_.                                                                          |
+------------------+------------------------------------------------------------------------------------------------------------+

X11 Windows Forwarding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to use a graphical screen of your application rather than a terminal, the ability to forward a graphical screen from the application back to your home computer is available via X11 Windows Forwarding.

.. note::
    Graphical workflows are inherently unsuitable the queue-based job submission model of the supercomputer. However, having a graphical window can still be useful for examining the results of your jobs.

With Linux and MacOS this can be done by login from the command line Secure Shell with the ``-Y`` option:

::

    ssh -Y [username]@ozstar.swin.edu.au

For **MacOS** you will first need to install `XQuartz <https://www.xquartz.org/>`_.

For modern **Windows** installations, you can use the Windows Subsystem for Linux (WSL), which provides a Linux command prompt. This is the recommended method. From there, the steps are the same as for Linux. Please refer to Microsoft's documentation on how to configure your system to run Linux GUI applications: https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps

For older **Windows** installations that do not provide WSL, you will need to install an X11 Server implementation. The following options can be used:

- `VcXsrv <https://sourceforge.net/projects/vcxsrv/>`_
- `Cygwin/X <http://x.cygwin.com/>`_
- `Xming <http://sourceforge.net/projects/xming/files/Xming/>`_

If you are using PuTTY, you will also need to enable X11 forwarding before connecting, This can be done through **connection > SSH > X11** by selecting “**Enable X11 Forwarding**”.
