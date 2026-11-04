.. highlight:: rst

Access to the supercomputer
============================

Access Ngarrgu Tindebeek
------------------------

Before connecting, set up :doc:`2fa` in the accounts portal.

Access to the :ref:`supercomputer<Ngarrgu Tindebeek>` is available through Secure Shell (SSH) to nt.swin.edu.au for all users. i.e:
::

    ssh [your-username]@nt.swin.edu.au

.. important::

    After logging in you will be assigned to one of the two login nodes: ``tooarrana1`` or ``tooarrana2``.

From these nodes you can submit jobs to the queue nodes using `Slurm <https://slurm.schedmd.com>`__. You may also use the login nodes as interactive nodes to run short jobs directly, compile code, or test your application.

.. note::
    Do not use these login nodes to run long jobs or jobs with big computational requirements. Running such jobs in interactive mode can be done by requesting interactive nodes from the queue.

Each login node is also available directly

::

    ssh [your-username]@tooarrana1.hpc.swin.edu.au
    ssh [your-username]@tooarrana2.hpc.swin.edu.au

Access OzSTAR
-------------
The login nodes for the :ref:`previous, older, supercomputer OzSTAR<OzSTAR>` (``farnarkle1/2``) are also still available via the round-robin address
::

    ssh [your-username]@ozstar.swin.edu.au

or directly
::

    ssh [your-username]@farnarkle1.hpc.swin.edu.au
    ssh [your-username]@farnarkle2.hpc.swin.edu.au

It is also possible to jump from any login node to any other login node using the hostnames ``t1``, ``t2``, ``f1``, and ``f2``.
For example,

::

    # From tooarrana1 to tooarrana2
    [tooarrana1]$ ssh t2
    [tooarrana2]$

    # From tooarrana2 to farnarkle1
    [tooarrana2]$ ssh f1
    [farnarkle1]$


Access Trevor
-------------
The login node for the cloud-based :ref:`trevor cluster<Trevor>` is only accessible by jumping from one of the other login nodes.
e.g.

::

    # From tooarrana1 to trevor
    [tooarrana1]$ ssh trevor
    [trevor]$


.. note::
    Jobs submitted on ``tooarrana1/2`` will run on the new AMD Milan nodes, whereas jobs submitted on ``farnarkle1/2`` will run on the older Intel Skylake nodes. Jobs submitted on ``trevor`` will run on the cloud-based trevor nodes.


Access data-mover nodes
-----------------------
The :ref:`data-mover nodes<Data-movers>` can be accessed directly or via the login nodes. e.g.

::

    # From local machine to data-mover01
    ssh [your-username]@data-mover01.hpc.swin.edu.au

    # From tooarrana1 to data-mover02
    [tooarrana1]$ ssh data-mover02
    [data-mover02]$

    # From farnarkle1 to data-mover03
    [farnarkle1]$ ssh dm3
    [data-mover03]$


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


Reusing SSH connections (multiplexing)
--------------------------------------

Enter your 2FA code once, then reuse that connection for other terminals
and transfers to the same destination without entering another code.

Linux, macOS, and Windows with WSL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Windows, run these steps inside the Windows Subsystem for Linux (WSL).
Native Windows OpenSSH and PuTTY do not support connection multiplexing.

Run these commands on your computer (inside WSL if you use Windows)::

    mkdir -p ~/.ssh/sockets
    chmod 700 ~/.ssh/sockets

Add this block to ``~/.ssh/config``::

    Host nt ozstar nt.swin.edu.au ozstar.swin.edu.au *.hpc.swin.edu.au
        ControlMaster auto
        ControlPath ~/.ssh/sockets/%C
        ControlPersist 300

Connect using your usual SSH command and enter your 2FA code. Subsequent
connections using the same SSH client, destination, username, and port
will reuse the connection instantly. Different login nodes and data-movers
each establish their own connection.

The connection remains available for 300 seconds (5 minutes) after the
last session closes. If you connect again within 5 minutes, you will not
be asked for a 2FA code.

.. tip::

    You can increase ``ControlPersist`` to ``10m`` (10 minutes) or ``1h``
    (1 hour) if you want the connection to stay open longer between tasks.

.. warning::

    While a shared connection is active, any process running under your
    local user account can connect through it without a 2FA code. Lock
    your computer when leaving it unattended.

Checking and closing a shared connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check if a connection is currently active::

    ssh -O check nt

To close the shared connection (note: this will close all active sessions
sharing that connection)::

    ssh -O exit nt

Here ``nt`` is the shortcut host name configured above. If you connected using
a full hostname instead, specify the full destination (e.g.
``ssh -O exit your-username@nt.swin.edu.au``). If a connection stops responding
after a network change, close it and reconnect.


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

VNC Sessions
^^^^^^^^^^^^

In some instances, you may need to run a graphical application that requires a full desktop environment.
In these cases, you can use a Virtual Network Computing (VNC) session.

VNC is also more efficient than X11 forwarding, so it can be useful for X11 applications that are slow to forward, especially over high-latency network connections -- any applications that show detailed 2D images or 3D graphics will benefit from it.

**1. Setup and launch a VNC server on OzSTAR**

Choose a login node to run the VNC server on.
You cannot rely on the generic ``ozstar`` or ``nt`` logins as a destination for remote persistent processes, since they are both round-robin addresses.
You need to pick one of ``tooarrana1/2`` or ``farnarkle1/2`` and stick to it.

::

    # Connect via ssh to a login node
    ssh [username]@tooarrana1.hpc.swin.edu.au

    # Ensure you have no modules loaded
    ml purge

    # Select up a vnc password
    vncpasswd

    # Start a vnc server
    vncserver

The VNC server will start on the first available port, e.g. ``:1``. It should say something like:

::

    New 'tooarrana1:1 (username)' desktop is tooarrana1:1

    Starting applications specified in /home/username/.vnc/xstartup
    Log file is /home/username/.vnc/tooarrana1:1.log

You only need to do this once. Running ``vncserver`` again will start a new session on the next available port, e.g. ``:2``.

**2. Use SSH tunneling to forward a port from your local machine to your VNC server**

From your local machine, setup up an SSH tunnel:

::

    ssh -L 5901:localhost:5901 -N [username]@tooarrana1.hpc.swin.edu.au

This will forward port 5901 on your local machine to port 5901 on the login node.
If you started the VNC server on a different port, adjust the port number accordingly, e.g. for port ``:2`` use ``5902``.

**3. Connect to your VNC server from your local machine with a VNC client**

You can use any VNC client to connect to the VNC server on the login node. Some popular clients include:

    - `TigerVNC <https://tigervnc.org>`_
    - `RealVNC <https://www.realvnc.com>`_
    - The inbuilt VNC client in MacOS. (You can make use of it via the "Screen Sharing" app, or via Finder -> Go -> Connect to Server, and enter ``vnc://localhost:5901``)

In each client, you just simply connect to ``localhost:5901`` (or whichever port you forwarded) and enter the password you set up with ``vncpasswd``.

You should then have a desktop window from the login node on your local machine.
You can run graphical applications from the terminal in this window.


**4. Tidying up**

When you are finished, remember to stop the VNC server on the login node

::

    vncserver -kill :X

where ``X`` is the number of the VNC server you started, e.g. ``1`` or ``2``.
You can see what servers are running with:

::

    vncserver -list
