# Restricted SSH Keys for Automated Jobs

A job that runs without a person present cannot enter a two-factor authentication (2FA) code. Configure a dedicated, command-restricted SSH key and request a 2FA exemption from support so unattended scripts can connect to Ngarrgu Tindebeek (NT), OzSTAR, or the data-movers without modifying your normal interactive login key.

For interactive sessions and manual transfers, use [Reusing SSH connections (multiplexing)](ssh-access.md#reusing-ssh-connections-multiplexing) instead.

## What we can and cannot approve

We cannot exempt an unrestricted SSH key from 2FA. An exempt key cannot open an interactive shell, runs only its approved command, and — for `rrsync` — is confined strictly to its approved directory.

HPC staff may review restricted entries in `~/.ssh/authorized_keys` at any time without notice. If an entry no longer matches the approved restriction, the exemption may be removed.

## Before you start

- Complete [Two-Factor Authentication (2FA)](../getting-started/2fa.md) enrollment and confirm that your normal interactive SSH login works.
- Know the project directory you need to access and the source IP address (or CIDR range) from which the automated job connects.
- Send and receive data through a data-mover rather than a login node. The examples below connect to `data-mover03.hpc.swin.edu.au`; see [Transferring Files](../storage/file-transfer.md) for the full list of data-movers.
- In every example below, replace `<username>` with your OzSTAR username, `<project>` with your project directory, `<source>` with the IP address or CIDR range the job connects from (for example, `203.0.113.0/24`), and `<dir>` / `<dir1>`–`<dir4>` with your actual directory names.

## Step 1: Create a dedicated key

On the machine that runs the automated job, generate a dedicated SSH key for this job only:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/automation -N '' -C unattended-job
cat ~/.ssh/automation.pub
```

The key has no passphrase so the unattended job can use it without prompting. Choose a filename that is not already in use, and send support only the `.pub` file — never share the private key.

## Step 2: Add the key to authorized_keys

Add the restricted entry to `~/.ssh/authorized_keys` on Swinburne HPC without removing your existing keys. Replace `ssh-ed25519 AAAA... <comment>` with the contents of `~/.ssh/automation.pub` from Step 1.

The general form is:

```text
restrict,from="<source>",command="..." ssh-ed25519 AAAA... <comment>
```

Keep each entry on a single physical line, even if your editor wraps it on screen. A line broken by a newline stops working and causes logins to fail with `Permission denied`. Replace all angle-bracket placeholders before saving.

### Pulling data (read-only)

To let the job download from one directory:

```text
restrict,from="<source>",command="/usr/bin/python3 /usr/share/doc/rsync/support/rrsync -ro -absolute /fred/<project>/data" ssh-ed25519 AAAA... <comment>
```

`-ro` allows downloads and refuses uploads. `-absolute` allows the job to reference the absolute paths used in the test commands below.

### Pushing data (write-only)

To let the job upload into one directory:

```text
restrict,from="<source>",command="/usr/bin/python3 /usr/share/doc/rsync/support/rrsync -wo -absolute -no-del /fred/<project>/incoming" ssh-ed25519 AAAA... <comment>
```

`-wo` allows uploads and refuses downloads. `-no-del` refuses deletions, though an upload can still overwrite an existing file of the same name.

### Running a fixed command

For a job that runs a single fixed command rather than a file transfer:

```text
restrict,from="<source>",command="find /fred/<project>/<dir1> /fred/<project>/<dir2> /fred/<project>/<dir3> /fred/<project>/<dir4> -type d" ssh-ed25519 AAAA... <comment>
```

`sshd` ignores whatever command the client sends and runs this exact command instead. Because the arguments are fixed in `authorized_keys`, update the entry (and notify support) if they need to change.

### Running a fixed script

For a job that executes a script on the cluster:

```text
restrict,from="<source>",command="/home/<username>/bin/nightly-check" ssh-ed25519 AAAA... <comment>
```

Ensure your account can execute the script and that other users cannot modify it. This form passes no arguments. Avoid reading `SSH_ORIGINAL_COMMAND` unless the script is explicitly designed and reviewed to validate untrusted input safely.

### Passing arguments

Running `ssh <host> 'cmd --flag'` does not pass `--flag` to a forced command. The `command="..."` string is the entire invocation, so place fixed arguments in the `authorized_keys` entry or inside the script itself.

The client's requested command is exposed to the forced command via the `SSH_ORIGINAL_COMMAND` environment variable. A wrapper that inspects `SSH_ORIGINAL_COMMAND` must strictly validate command syntax and paths and never pass untrusted text to a shell; because this is easy to get wrong, support is less likely to approve wrappers that rely on it.

:::{note}
For automated `scp` jobs, switch to `rsync` with `rrsync`. Modern `scp` transfers over SFTP, and a forced SFTP server can set a starting directory without confining the session inside it, so it is not a safe substitute for `rrsync`.
:::

## Step 3: Request the exemption

Email `hpc-support@swin.edu.au` with:

- Your OzSTAR username
- The IP address (or CIDR range) the job connects from
- The command or destination directory, including the full restricted `authorized_keys` entry
- The public key from the `.pub` file

An approved exemption applies only to that specific restricted key, never to all logins on your account.

## Step 4: Test the key

Run all tests from the machine and network that will execute the automated job.

### Before the exemption is approved

The key works before the exemption is approved, but 2FA still prompts. Verify that the key is installed by connecting to the host the job uses (for an `rsync` job, a data-mover):

```bash
ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o ControlPath=none <username>@data-mover03.hpc.swin.edu.au
```

Enter your 2FA code when prompted. Reaching the 2FA prompt confirms that your restricted key was accepted. After entering the code, an `rrsync` entry exits with `Not invoked via sshd` and a fixed-command entry prints its output. Either result confirms the key is configured correctly and is only waiting on the 2FA exemption.

### After the exemption is confirmed

Once support confirms the exemption, the same connection runs without prompting for a 2FA code. Test the full command with `--dry-run` first:

```bash
# Test pulling data (lists files without copying)
rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o ControlPath=none' <username>@data-mover03.hpc.swin.edu.au:/fred/<project>/data/<dir>/ dest/

# Test pushing data (lists files without copying)
rsync -av --dry-run -e 'ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o ControlPath=none' local/ <username>@data-mover03.hpc.swin.edu.au:/fred/<project>/incoming/
```

For a fixed command or fixed script running on a login node:

```bash
ssh -i ~/.ssh/automation -o IdentitiesOnly=yes -o ControlPath=none <username>@ozstar.swin.edu.au
```

The first two commands list matching files without copying; the last prints the fixed command output and never opens an interactive shell.

:::{warning}
Do **not** add `BatchMode=yes` to your automated `ssh` options. `BatchMode=yes` disables the `keyboard-interactive` authentication method used by the 2FA subsystem, causing even an exempted key to be refused.
:::

If any test still prompts for a 2FA code, the exemption is not yet active on that host.

## What the restriction does not do

`from=` restricts the source address, `command=` fixes what executes, and `restrict` disables interactive terminals and port forwarding. These controls limit what a party holding the automation key can do — they do not restrict you, because you control `~/.ssh/authorized_keys`. A write-only key (`-wo -no-del`) can still overwrite existing files inside its allowed destination directory.

## Next steps

- [Transferring Files](../storage/file-transfer.md) — recommended `rsync` flags and data-mover addresses.
- [Connecting via SSH](ssh-access.md) — set up interactive connection reuse with multiplexing.
- [User Support](../help/support.md) — contact `hpc-support@swin.edu.au` with exemption requests or troubleshooting questions.
