# Two-Factor Authentication (2FA)

Set up two-factor authentication (2FA) before connecting via SSH to Ngarrgu Tindebeek (NT), OzSTAR, or the data-movers. Each interactive SSH login requires both your password or SSH key and a six-digit code from your authenticator app.

## Before you start

- An approved OzSTAR account and password (see [Accounts and Projects](accounts.md)).
- An authenticator app installed on your phone or password manager (such as Google Authenticator, Microsoft Authenticator, 1Password, or Apple Passwords)[^yubikey].

## Enrolling in 2FA

:::{important}
Enroll in the Accounts Portal before logging in via SSH. If you have not enrolled, SSH returns `Permission denied` without asking for a 2FA code. This is expected and simply means you must complete enrollment in the portal first.
:::

1. Sign in to the [Accounts Portal](https://supercomputing.swin.edu.au/account-management/) with your OzSTAR username and password.
2. Open **Two-Factor Authentication**.
3. In your authenticator app, scan the QR code or enter the setup key.
4. Enter the six-digit code from your app into the portal to finish setup.

## Emergency recovery codes

:::{warning}
Save your recovery codes immediately: they are displayed only once. Store them in a secure password manager or a safe place on paper. Do not email them to yourself or save them in an unencrypted file.
:::

Each recovery code can be used once. Recovery codes are accepted only by the Accounts Portal to reset or reconfigure your authenticator app if you lose access to your device; they cannot be used directly at the SSH login prompt.

## Logging in with 2FA

Connect to NT from your local terminal:

```bash
ssh <username>@nt.swin.edu.au
```

Replace `<username>` with your OzSTAR username. Complete any password or SSH-key passphrase prompts, then enter your current six-digit app code when prompted with `OzSTAR 2FA code:`.

Each 2FA code can only be used once. If you are prompted for a code again in quick succession (for example, when opening a second terminal), wait for your authenticator app to generate the next code.

To avoid entering a code for every terminal or file transfer, see [Reusing SSH connections (multiplexing)](../access/ssh-access.md#reusing-ssh-connections-multiplexing).

## Automated and unattended workflows

Logins and file transfers that you run interactively work with standard 2FA or SSH connection reuse and do not need an exemption.

Unattended scripts (such as automated nightly transfers or pipelines) cannot enter 2FA codes. They require a dedicated SSH key restricted to the job's command and exempted from 2FA by support. See [Restricted SSH Keys for Automated Jobs](../access/restricted-keys.md) to set one up and request an exemption.

## Lost devices and troubleshooting

If you lose access to your authenticator app, sign in to the [Accounts Portal](https://supercomputing.swin.edu.au/account-management/) using an unused recovery code to reset your authenticator.

If you have lost both your authenticator and your recovery codes, email `hpc-support@swin.edu.au` with your OzSTAR username (see [User Support](../help/support.md)). Never send passwords, setup keys, or recovery codes by email.

## Next steps

- [Connecting via SSH](../access/ssh-access.md) — connect to NT, OzSTAR, Trevor, and the data-movers, and configure SSH connection reuse.
- [Restricted SSH Keys for Automated Jobs](../access/restricted-keys.md) — configure command-restricted SSH keys for unattended automation.

[^yubikey]: Some hardware authenticators (such as certain YubiKey models) can store and generate standard time-based (TOTP) codes using companion software such as [Yubico Authenticator](https://support.yubico.com/s/article/Using-your-YubiKey-with-authenticator-codes). Not all hardware keys or YubiKey versions support TOTP, and compatibility is device-dependent; check your hardware documentation to confirm whether your device supports TOTP codes.
