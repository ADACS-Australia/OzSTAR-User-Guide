.. highlight:: rst

Two-Factor Authentication (2FA)
===============================

Set up two-factor authentication (2FA) before connecting to OzSTAR or
Ngarrgu Tindebeek (NT). When you log in, you will need a code from your
authenticator app as well as your password or SSH key.

Enrolling in 2FA
----------------

.. important::

    Enroll in the account management portal before logging in via SSH.
    If you have not enrolled, SSH returns ``Permission denied`` without
    asking for a 2FA code. This is expected and simply means you must
    complete enrollment in the portal first.

1. Log in to the `account management portal
   <https://supercomputing.swin.edu.au/account-management/>`_
   with your OzSTAR username and password.
2. Open **Two-Factor Authentication**.
3. In your authenticator app (such as Google Authenticator, Microsoft
   Authenticator, or 1Password), scan the QR code or enter the setup key.
4. Enter the app's six-digit code in the portal to finish setup.

Emergency recovery codes
------------------------

.. warning::

    Save your recovery codes now: they are displayed only once.
    Keep them in a secure password manager or a safe place on paper.
    Do not email them to yourself or store them in an unencrypted file.

Each recovery code can be used once. If you cannot use your authenticator
app, enter an unused recovery code at the ``OzSTAR 2FA code:`` prompt.

Logging in with 2FA
-------------------

Connect to NT from your local terminal::

    ssh your-username@nt.swin.edu.au

Replace ``your-username`` with your OzSTAR username. Complete any password
or SSH-key passphrase prompts, then enter your current six-digit app code
when you see ``OzSTAR 2FA code:``.

To avoid repeated code prompts, see
:ref:`Reusing SSH connections (multiplexing)`.

Automated and unattended workflows
----------------------------------

Transfers and logins you run interactively yourself do not need an exemption;
they work with standard 2FA or connection reuse.

Unattended scripts (such as automated nightly transfers or pipelines) cannot
enter 2FA codes. Email ``hpc-support@swin.edu.au`` to request assessment for a
command-restricted SSH key. Include your OzSTAR username, the source
hostname or IP address, the command to run, and the workflow's purpose.

Lost devices and troubleshooting
--------------------------------

If you lose access to your authenticator, use an unused recovery code
and reset your authenticator through the account management portal.
If you have lost both your authenticator and recovery codes, email
``hpc-support@swin.edu.au`` with your OzSTAR username for help.
Do not send passwords, setup keys, or recovery codes in email.
