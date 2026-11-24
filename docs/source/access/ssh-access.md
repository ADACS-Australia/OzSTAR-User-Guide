# Connecting via SSH

Connect via Secure Shell (SSH) to Ngarrgu Tindebeek (NT), OzSTAR, Trevor, and the data-mover nodes, configure optional shortcuts and session keep-alives, and reuse SSH connections to avoid repeated two-factor authentication (2FA) prompts.

## Before you start

1. Ensure you have an approved OzSTAR account ([Accounts and Projects](../getting-started/accounts.md)) and have completed [Two-Factor Authentication (2FA)](../getting-started/2fa.md) enrollment in the Accounts Portal.
2. Open a terminal with an SSH client on your local computer:

   ::::{tab-set}

   :::{tab-item} Linux
   Open your system terminal application. The OpenSSH client (`ssh`) is available by default.
   :::

   :::{tab-item} macOS
   Open **Applications > Utilities > Terminal**. The OpenSSH client (`ssh`) is available by default.
   :::

   :::{tab-item} Windows
   Install the Windows Subsystem for Linux (WSL) using the [Microsoft WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install) (recommended). WSL provides a standard Linux terminal with OpenSSH and full support for SSH connection multiplexing.

   If you use an older version of Windows without WSL, install [PuTTY](https://www.putty.org/). Note that PuTTY and native Windows OpenSSH do not support SSH connection multiplexing.
   :::

   ::::

## Connecting to login nodes and data-movers

:::{warning}
Login nodes are shared by all users for short interactive tasks such as editing files, compiling code, and submitting Slurm jobs. Do not run long jobs or compute-intensive workloads on login nodes — submit them to compute nodes via Slurm (see [Policies](../1-getting_started/Policies.rst) and [Creating and Submitting Jobs](../jobs/creating-jobs.md)).
:::

### Ngarrgu Tindebeek (NT)

Connect via the round-robin address, which assigns you to either `tooarrana1` or `tooarrana2`:

```bash
ssh <username>@nt.swin.edu.au
```

Or connect directly to a specific NT login node:

```bash
ssh <username>@tooarrana1.hpc.swin.edu.au
ssh <username>@tooarrana2.hpc.swin.edu.au
```

Jobs submitted from `tooarrana1` or `tooarrana2` run on NT AMD Milan compute nodes.

### OzSTAR

Connect via the round-robin address, which assigns you to either `farnarkle1` or `farnarkle2`:

```bash
ssh <username>@ozstar.swin.edu.au
```

Or connect directly to a specific OzSTAR login node:

```bash
ssh <username>@farnarkle1.hpc.swin.edu.au
ssh <username>@farnarkle2.hpc.swin.edu.au
```

Jobs submitted from `farnarkle1` or `farnarkle2` run on OzSTAR Intel Skylake compute nodes.

### Trevor

The Trevor login node is reachable only by jumping from an NT or OzSTAR login node. Once logged in to `tooarrana1/2` or `farnarkle1/2`, run:

```bash
ssh trevor
```

Jobs submitted from `trevor` run on the private-cloud, internet-enabled Trevor compute nodes.

### Data-movers

Use the dedicated data-mover nodes (`data-mover01` through `data-mover04`) for transferring files to and from Swinburne HPC storage so transfers do not contend with shared login nodes (see [Transferring Files](../storage/file-transfer.md)):

```bash
ssh <username>@data-mover01.hpc.swin.edu.au
```

### Jumping between nodes

From any Swinburne HPC login node, you can jump to another login node, Trevor, or a data-mover using short internal hostnames:

- **NT login nodes:** `t1`, `t2`
- **OzSTAR login nodes:** `f1`, `f2`
- **Trevor:** `trevor`
- **Data-movers:** `dm1`–`dm4` (or `data-mover01`–`data-mover04`)

For example, from any login node:

```bash
ssh t2
ssh f1
ssh trevor
ssh dm3
```

### Assigning a login node with myhome

Because `nt.swin.edu.au` and `ozstar.swin.edu.au` are round-robin addresses, consecutive logins can land on different login nodes. For persistent sessions that must stay on a single login node — such as `tmux`, Jupyter notebooks, VNC desktops, VS Code Remote-SSH, or AI coding tools — run `myhome` on any login node to find your assigned node:

```bash
myhome
```

`myhome` deterministically assigns you to login node `1` or `2` (`tooarrana1` or `tooarrana2` on NT; `farnarkle1` or `farnarkle2` on OzSTAR) based on your username so persistent workloads stay balanced across login nodes. Connect directly to that assigned hostname (for example, `tooarrana1.hpc.swin.edu.au`) whenever you run persistent tools.

## Optional: SSH shortcuts and keep-alive

To avoid typing your full username and hostname on every connection — and to stop idle terminals from timing out — add shortcut entries to `~/.ssh/config` on your local computer (inside WSL on Windows):

```ini
Host nt
    HostName nt.swin.edu.au
    User <username>
    ServerAliveInterval 120

Host ozstar
    HostName ozstar.swin.edu.au
    User <username>
    ServerAliveInterval 120
```

`ServerAliveInterval 120` sends a keep-alive message every 120 seconds so idle SSH sessions are not dropped by intermediate firewalls. If you regularly use persistent tools on your `myhome`-assigned node, you can add a dedicated shortcut for it too (for example, `Host t1` pointing to `tooarrana1.hpc.swin.edu.au`).

Set restrictive file permissions on `~/.ssh/config` as required by OpenSSH:

```bash
chmod 600 ~/.ssh/config
```

Once configured, you can connect with the short alias instead of the full address:

```bash
ssh nt
ssh ozstar
```

## Reusing SSH connections (multiplexing)

Enter your 2FA code once, then reuse that authenticated connection for additional terminals and file transfers to the same destination without entering another code.

This works on Linux, macOS, and Windows inside WSL. On Windows, run every command below inside WSL; native Windows OpenSSH and PuTTY do not support connection multiplexing.

### Set up multiplexing

1. On your local computer, create a private directory for shared control sockets:

   ```bash
   mkdir -p ~/.ssh/sockets
   chmod 700 ~/.ssh/sockets
   ```

2. Add the appropriate block for your operating system to `~/.ssh/config` (and run `chmod 600 ~/.ssh/config` if you created the file).

   OpenSSH merges settings from every matching `Host` block in `~/.ssh/config`, matching each `Host` pattern against the alias you type rather than the expanded `HostName`. This block works standalone with real hostnames (`nt.swin.edu.au`, `ozstar.swin.edu.au`, and `*.hpc.swin.edu.au`) even if you skipped the optional shortcuts above, and also matches the `nt`, `ozstar`, `t1`/`t2`, and `f1`/`f2` shortcuts. If you define any other custom shortcut alias (such as `dm1`), append that alias name to this `Host` line as well.

   ::::{tab-set}

   :::{tab-item} Linux (graphical desktop — recommended)
   With `ControlMaster autoask`, OpenSSH prompts you with a pop-up window before allowing another terminal or program to reuse your connection.

   First install the pop-up helper (on Ubuntu or Debian):

   ```bash
   sudo apt install ssh-askpass
   ```

   Then add this block to `~/.ssh/config`:

   ```ini
   Host nt ozstar t1 t2 f1 f2 nt.swin.edu.au ozstar.swin.edu.au *.hpc.swin.edu.au
       ControlMaster autoask
       ControlPath ~/.ssh/sockets/%C
       ControlPersist 300
   ```
   :::

   :::{tab-item} macOS, Windows (WSL), or headless Linux
   Add this block to `~/.ssh/config` (inside WSL on Windows):

   ```ini
   Host nt ozstar t1 t2 f1 f2 nt.swin.edu.au ozstar.swin.edu.au *.hpc.swin.edu.au
       ControlMaster auto
       ControlPath ~/.ssh/sockets/%C
       ControlPersist 300
   ```
   :::

   ::::

### Using a shared connection

:::{warning}
While a shared connection is open, any program running under your local user account can reuse it without a 2FA code, including scripts and AI coding assistants. With `ControlMaster auto`, this happens without any prompt. Lock your computer whenever you leave it unattended.
:::

Connect with your usual SSH command and enter your 2FA code. Later connections using the same SSH client, destination, username, and port reuse that session immediately. Different login nodes and data-movers each establish their own connection.

With `ControlMaster autoask`, a small pop-up asks whether to allow the shared connection each time a process uses it (including your first login):

- Click **OK** if you just started that connection yourself.
- Click **Cancel** if you did not; that program must then authenticate from scratch with a new 2FA code.

The shared connection stays open for 300 seconds (5 minutes) after the last terminal closes. Reconnecting within 5 minutes does not require a new 2FA code.

:::{tip}
You can increase `ControlPersist` to `10m` (10 minutes) or `1h` (1 hour) if you want shared connections to remain open longer between tasks.
:::

If login fails with `Failed to connect to new control master`, the `ssh-askpass` pop-up could not be displayed. Change `ControlMaster autoask` to `ControlMaster auto` in `~/.ssh/config` and connect again.

### Checking and closing a shared connection

To check whether a shared connection is active or close it immediately (closing all sessions sharing that connection), run:

```bash
# Check status
ssh -O check <username>@nt.swin.edu.au

# Close the shared connection
ssh -O exit <username>@nt.swin.edu.au
```

If you configured the optional `Host nt` shortcut above, you can run `ssh -O check nt` and `ssh -O exit nt` instead. With `autoask`, you are prompted to confirm before closing. If a shared connection hangs after switching Wi-Fi networks or resuming from sleep, close it with `-O exit` and reconnect.

## Next steps

- [Graphical Access (X11 and VNC)](graphical-access.md) — forward GUI windows or launch a VNC desktop on your assigned login node.
- [Restricted SSH Keys for Automated Jobs](restricted-keys.md) — set up command-restricted keys for unattended automated workflows.
- [Using AI Coding Tools](ai-coding-tools.md) — run AI coding assistants and VS Code Remote-SSH responsibly on NT and OzSTAR.
