.. highlight:: rst

Restricted SSH keys for automated jobs
======================================

A job that runs without a person present cannot enter a 2FA code. It needs its
own key, restricted to the command it runs and approved by support. Your normal
login key stays as it is. For interactive reuse, see
:ref:`Reusing SSH connections (multiplexing)`.

What we can and cannot approve
------------------------------

We can't exempt a key that isn't restricted. An exempt key can't open a shell,
runs only its approved command, and, for ``rrsync``, is confined to the approved
directory.

We may review the restricted entries in ``authorized_keys`` at any time without
notice. If an entry no longer matches the approved restriction, we may remove
the exemption.

Before you start
----------------

Complete enrollment in :doc:`2fa` and check that your interactive login works.
You need access to the project's data and the address the job connects from.

Examples connect to ``nt.swin.edu.au``. Use ``ozstar.swin.edu.au`` if the job
runs there.

Replace ``USER`` with your username, ``PROJECT`` with your project directory,
and ``SOURCE`` with the address the job connects from, or a range such as
``203.0.113.0/24``. Replace ``DIR1`` through ``DIR4``, and ``DIR``, with your own
directories. These are placeholders, not directories that exist.

Step 1: Create a dedicated key
------------------------------

On the machine that runs the job, create a key for this job only::

    ssh-keygen -t ed25519 -f ~/.ssh/automation -N '' -C unattended-job
    cat ~/.ssh/automation.pub

The key has no passphrase, so it can run unattended. Choose a filename that
isn't already in use, and send support only the ``.pub`` file, not the private
key.

Step 2: Add the key to authorized_keys
--------------------------------------

Add the entry to ``~/.ssh/authorized_keys`` without removing the ones already
there. Use the public key from Step 1 in place of
``ssh-ed25519 AAAA... comment``. The general form is::

    restrict,from="SOURCE",command="..." ssh-ed25519 AAAA... comment

Keep each entry on one physical line, even if your editor wraps it on screen. A
line broken by a newline stops working, and the login fails with
``Permission denied``. Replace the placeholders before installing the entry.

Pulling data
^^^^^^^^^^^^

To let the job read one directory::

    restrict,from="SOURCE",command="/usr/bin/python3 /usr/share/doc/rsync/support/rrsync -ro -absolute /fred/PROJECT/data" ssh-ed25519 AAAA... comment

``-ro`` allows downloads, not uploads. ``-absolute`` lets the job use the
absolute paths in the examples.

Pushing data
^^^^^^^^^^^^

To let the job write into one directory::

    restrict,from="SOURCE",command="/usr/bin/python3 /usr/share/doc/rsync/support/rrsync -wo -absolute -no-del /fred/PROJECT/incoming" ssh-ed25519 AAAA... comment

``-wo`` allows uploads, not downloads. ``-no-del`` refuses deletions, but an
upload can still overwrite an existing file.

Running a fixed command
^^^^^^^^^^^^^^^^^^^^^^^

For a job that runs a command rather than a transfer::

    restrict,from="SOURCE",command="find /fred/PROJECT/DIR1 /fred/PROJECT/DIR2 /fred/PROJECT/DIR3 /fred/PROJECT/DIR4 -type d" ssh-ed25519 AAAA... comment

sshd ignores whatever the client sends and runs this command instead. The
arguments in the entry are the ones that run, so edit the entry when they
change. This example lists directories and transfers nothing.

Running a fixed script
^^^^^^^^^^^^^^^^^^^^^^

For a job that runs a script::

    restrict,from="SOURCE",command="/home/USER/bin/nightly-check" ssh-ed25519 AAAA... comment

Your account must be able to execute the script, and other users shouldn't be
able to modify it. This example passes no arguments. Avoid interpreting
``SSH_ORIGINAL_COMMAND`` unless the script is designed and reviewed to validate
it safely.

Passing arguments
^^^^^^^^^^^^^^^^^

``ssh host 'cmd --flag'`` doesn't pass ``--flag``. ``command=`` is the whole
invocation, so put the arguments in the entry or inside the script.

The command the client sent is still visible to the forced command as
``SSH_ORIGINAL_COMMAND``. A wrapper that reads it has to validate the command
syntax and any paths, and keep untrusted text away from a shell. That is easy to
get wrong, so we're less likely to approve a wrapper that depends on it.

.. note::

    For an automated scp job, use rsync instead. scp transfers over SFTP, and a
    forced SFTP server can set a starting directory but doesn't keep the session
    inside it, so it isn't a substitute for rrsync.

Step 3: Request the exemption
-----------------------------

Email ``hpc-support@swin.edu.au`` with:

* your username
* the address the job connects from
* the command or destination, including the restricted entry
* the public key from the ``.pub`` file

An exemption applies to the approved key, not to every login on your account.

Step 4: Test it
---------------

Run the test from the machine and network that will run the job.
``BatchMode=yes`` stops a password or code prompt from hiding a failure,
``ControlPath=none`` stops an existing connection from being reused, and
``IdentitiesOnly=yes`` selects this key.

Read-only::

    rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none' USER@nt.swin.edu.au:/fred/PROJECT/data/DIR/ dest/

Write-only::

    rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none' local/ USER@nt.swin.edu.au:/fred/PROJECT/incoming/

Fixed command::

    ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o BatchMode=yes -o ControlPath=none USER@nt.swin.edu.au

The first two list files without copying. The third prints the fixed output and
never a shell. For an rsync entry the third command should refuse with
``Not invoked via sshd``. None should ask for a code; if one does, the exemption
isn't in place yet.

Common failures
---------------

* ``post-realpath open failed``: an absolute path is used without ``-absolute``.
* ``do not use .. in arg``: the transfer path contains ``..``.
* ``sending to read-only server is not allowed``: an upload used a ``-ro`` entry.
* ``reading from write-only server is not allowed``: a download used a ``-wo`` entry.
* ``option --delete has been disabled``: the job asked for deletion through a
  ``-no-del`` entry.
* ``Permission denied``: the address, the entry or the key doesn't match what was
  approved. Check all three.

What the restriction does not do
--------------------------------

``from=`` limits where the key connects from, ``command=`` fixes what it runs,
and ``restrict`` turns off terminals and forwarding. These limit what someone
holding the key can do; they don't constrain you, since you control
``authorized_keys``. A write-only key can still overwrite files in its
destination.
