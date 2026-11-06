.. highlight:: rst

Two-Factor Authentication (2FA)
===============================

Set up two-factor authentication (2FA) before connecting to OzSTAR or
Ngarrgu Tindebeek (NT). When you log in, you will need a code from your
authenticator app as well as your password or SSH key.

Enrolling in 2FA
----------------

.. important::

    Enroll in the accounts portal before logging in via SSH.
    If you have not enrolled, SSH returns ``Permission denied`` without
    asking for a 2FA code. This is expected and simply means you must
    complete enrollment in the portal first.

1. Log in to the `accounts portal
   <https://supercomputing.swin.edu.au/account-management/>`_
   with your OzSTAR username and password.
2. Open **Two-Factor Authentication**.
3. In your authenticator app (such as Google Authenticator, Microsoft
   Authenticator, or 1Password) [#]_, scan the QR code or enter the setup key.
4. Enter the app's six-digit code in the portal to finish setup.

Emergency recovery codes
------------------------

.. warning::

    Save your recovery codes now: they are displayed only once.
    Keep them in a secure password manager or a safe place on paper.
    Do not email them to yourself or store them in an unencrypted file.

Each recovery code can be used once. Recovery codes are only accepted
by the accounts portal to reset or reconfigure your authenticator app
if you lose access to your device. Recovery codes cannot be used directly
at the SSH login prompt.

Logging in with 2FA
-------------------

Connect to NT from your local terminal::

    ssh your-username@nt.swin.edu.au

Replace ``your-username`` with your OzSTAR username. Complete any password
or SSH-key passphrase prompts, then enter your current six-digit app code
when you see ``OzSTAR 2FA code:``.

Each 2FA code can only be used once. If you are prompted for a code again
in quick succession (for example, when opening another connection), wait
for your authenticator app to generate the next code.

To avoid repeated code prompts, see
:ref:`Reusing SSH connections (multiplexing)`.

Automated and unattended workflows
----------------------------------

Transfers and logins you run interactively yourself do not need an exemption;
they work with standard 2FA or connection reuse.

Unattended scripts (such as automated nightly transfers or pipelines) cannot
enter 2FA codes. They need a key restricted to the job's command and exempted
from 2FA. See :doc:`restricted-keys` to set one up and request the exemption.

Lost devices and troubleshooting
--------------------------------

If you lose access to your authenticator app, sign in to the accounts
portal using an unused recovery code to reset your authenticator.
If you have lost both your authenticator and recovery codes, email
``hpc-support@swin.edu.au`` with your OzSTAR username for help.
Do not send passwords, setup keys, or recovery codes in email.

.. rubric:: Footnotes

.. [#] Some hardware authenticators (such as certain YubiKey models) can store and generate standard time-based (TOTP) codes using companion software like the `Yubico Authenticator <https://support.yubico.com/s/article/Using-your-YubiKey-with-authenticator-codes>`_. Not all hardware keys or YubiKey versions support TOTP, and compatibility is entirely device-dependent; it is up to the user to identify whether their hardware device supports generating TOTP codes.
