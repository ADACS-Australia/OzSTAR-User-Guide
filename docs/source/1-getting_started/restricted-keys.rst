.. highlight:: rst

Restricted SSH keys for automated jobs
======================================

Why a restricted key
--------------------

Use a dedicated, command-restricted SSH key for a job that must connect
without someone entering a 2FA code. Support must approve an exemption;
creating a key alone does not bypass 2FA. Keep your normal login separate.
For interactive reuse, see :ref:`Reusing SSH connections (multiplexing)`.

Before you start
----------------

Complete enrollment in :doc:`2fa` and check that your interactive login works.
You need access to the project's data and a known source address for the job.
Examples connect to ``nt.swin.edu.au``; ``ozstar.swin.edu.au`` is equivalent
if the job runs there.

Replace ``USER`` with your username, ``PROJECT`` with your project directory,
and ``CIDR`` with the job's externally visible source address or network in
CIDR notation. Replace ``DIR1`` through ``DIR4`` with your actual directories,
and ``DIR`` with a subdirectory of your data directory.
These are placeholders, not existing directories. Choose only the access
your job needs, and use a separate key for a different command or destination.

Step 1: Create a dedicated key
------------------------------

On the machine that will initiate the job, create a key for this job only.
The example uses ``~/.ssh/automation``; choose another name if it exists::

    ssh-keygen -t ed25519 -f ~/.ssh/automation -N '' -C unattended-job
    cat ~/.ssh/automation.pub

This creates a key without a passphrase for unattended use. Do not overwrite
an existing key. The file ending in ``.pub`` is the public key.
Never send the private key to anyone.

Step 2: Install the rsync wrapper
---------------------------------

For an rsync job, log in interactively to NT and run::

    mkdir -p ~/bin
    cp /usr/share/doc/rsync/support/rrsync ~/bin/rrsync

The examples call the copy with ``/usr/bin/python3`` explicitly, so they
do not depend on which Python your shell environment selects.
Skip this step if your job runs a fixed command rather than rsync.

Step 3: Add the key to authorized_keys
--------------------------------------

On NT, add the chosen entry to ``~/.ssh/authorized_keys`` without replacing
existing entries. Use the public key printed in Step 1 in place of
``ssh-ed25519 AAAA... comment``. The general form is::

    restrict,from="CIDR",command="..." ssh-ed25519 AAAA... comment

Each entry must be **one physical line**, even if your editor displays it
across the screen. sshd rejects an entry split by a newline, and the client
sees ``Permission denied``.
Do not paste the examples unchanged.

Pulling data with a restricted key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To let the job read only the selected data directory, use::

    restrict,from="CIDR",command="/usr/bin/python3 /home/USER/bin/rrsync -ro -absolute /fred/PROJECT/data" ssh-ed25519 AAAA... comment

Here ``-ro`` permits downloads, not uploads. ``-absolute`` allows the
absolute remote paths used in the transfer examples.

Pushing data with a restricted key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To let the job upload into the selected incoming directory, use::

    restrict,from="CIDR",command="/usr/bin/python3 /home/USER/bin/rrsync -wo -absolute -no-del /fred/PROJECT/incoming" ssh-ed25519 AAAA... comment

Here ``-wo`` permits uploads, not downloads. ``-no-del`` rejects deletion
requests, but does not prevent an upload from overwriting an existing file.

Running another command with a restricted key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a directory listing rather than a transfer, use a fixed command::

    restrict,from="CIDR",command="find /fred/PROJECT/DIR1 /fred/PROJECT/DIR2 /fred/PROJECT/DIR3 /fred/PROJECT/DIR4 -type d" ssh-ed25519 AAAA... comment

Replace the four directory placeholders before installing the entry.
Keep the command fixed: do not add client-supplied arguments or shell
evaluation. SSH ignores the command requested by the client and runs this
``find`` instead. This example lists directories; it does not transfer data.

Running a fixed script
^^^^^^^^^^^^^^^^^^^^^^

For an automated script job, use a fixed invocation::

    restrict,from="CIDR",command="/home/USER/bin/nightly-check" ssh-ed25519 AAAA... comment

The script must be executable by your account. Keep a script you maintain in
a directory other users cannot modify. It runs with no arguments and must not
read arguments from the client.

Passing arguments
^^^^^^^^^^^^^^^^^

``ssh host 'cmd --flag'`` does not pass ``--flag`` to the restricted command:
``command=`` is the whole invocation, and sshd ignores anything the client sends.
Put arguments in the entry or inside the script. Do not pass client input
to a shell.

.. note::

    Convert an automated scp job to rsync, because scp transfers over SFTP.
    Forcing an SFTP server can set a starting directory, but it does not keep
    the session inside it, so it is not a substitute for rrsync.

Step 4: Request the exemption
-----------------------------

Email ``hpc-support@swin.edu.au`` to request assessment. Include:

* Your OzSTAR username.
* The source address from which the unattended job connects.
* The fixed command or transfer destination, including the restricted entry.
* The public key from the ``.pub`` file.

Wait for approval before testing unattended access. An exemption applies to
the approved restricted key, not to all logins to your account.

Step 5: Test it
---------------

Run the test from the machine and network that will initiate the job.
Use ``BatchMode=yes`` so a password or 2FA prompt cannot hide a failure.
``ControlPath=none`` avoids reusing an authenticated interactive connection;
``IdentitiesOnly=yes`` selects the dedicated identity.

For the read-only entry, preview a download without copying files::

    rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none' USER@nt.swin.edu.au:/fred/PROJECT/data/DIR/ dest/

For the write-only entry, preview an upload without copying files::

    rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none' local/ USER@nt.swin.edu.au:/fred/PROJECT/incoming/

Replace ``local/`` and ``dest/`` with your local source and destination.
Check that the dry run succeeds without a prompt and lists the intended
files. Remove ``--dry-run`` only when ready to transfer them.

For the fixed-command entry, run::

    ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none USER@nt.swin.edu.au

Check that it prints the fixed directory listing, not a shell prompt.
For an rsync entry, the same SSH test sends no client command and refuses
a shell with ``Not invoked via sshd``. Do not use that test for the
fixed-command entry expecting refusal: it always runs the fixed command.

Common failures
---------------

* ``post-realpath open failed (race detected): ... No such file or directory``
  can occur when an absolute transfer path is used without ``-absolute``.
  Check the installed entry against the appropriate example.
* ``do not use .. in arg (anchor the path at the root of your restricted dir)``
  means the transfer path contains ``..``. Use a path within the selected
  directory without parent-directory components.
* ``option -s has been disabled on this server.`` means the client supplied
  ``-s`` or ``--protect-args``. Remove that option for this restricted job.
* ``invalid key option string`` is recorded only in the server log, which
  users cannot read. For a malformed entry, the client sees the permission
  error below; check for a single physical line and intact option quotes.
* ``sending to read-only server is not allowed`` means an upload used
  a read-only entry. Use the key approved for uploads instead.
* ``reading from write-only server is not allowed`` means a download used
  a write-only entry. Use the key approved for downloads instead.
* ``option --delete has been disabled on this server.`` means the job requested deletion
  through a ``-no-del`` entry. Remove ``--delete``.
* ``option -L has been disabled on this server.`` means the client supplied ``-L`` or
  ``--copy-links``. Remove that option.
* ``Permission denied`` can mean a source-address mismatch, a malformed entry
  or a key that is not installed. Check the source address, the entry itself,
  the selected key and approval.

What the restriction does and does not protect
----------------------------------------------

``from=`` limits where this key can connect from. ``command=`` fixes what
it runs. ``restrict`` disables terminal allocation, port forwarding, agent
forwarding, X11 forwarding and ``~/.ssh/rc``. The rsync wrapper also checks
the requested transfer command and limits it to the selected directory.

These restrictions reduce what someone holding this job key can do.
They do not constrain the account owner, who controls
``~/.ssh/authorized_keys``. A write-only key can still overwrite files in
its permitted destination; ``-no-del`` is not a backup or overwrite guard.
A fixed command has only the limits you actually put in that command.
