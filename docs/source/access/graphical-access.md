# Graphical Access (X11 and VNC)

Run graphical applications on Ngarrgu Tindebeek (NT) or OzSTAR login nodes using X11 forwarding for single windows or VNC for a full desktop session.

## Before you start

- Verify that standard SSH login with 2FA works ([Connecting via SSH](ssh-access.md)).
- Keep `module load` commands out of `~/.bashrc` and other dotfiles; loaded modules can conflict with X11 and VNC system libraries (see [Dotfiles and shell hygiene](linux-environment.md#dotfiles-and-shell-hygiene)).

:::{note}
Graphical sessions are intended for lightweight interactive tasks such as inspecting outputs, viewing plots, or configuring workflows. Submit computationally intensive work to compute nodes via Slurm ([Creating and Submitting Jobs](../jobs/creating-jobs.md)).
:::

## X11 forwarding

Use X11 forwarding when you need an individual graphical window over a fast, low-latency connection.

::::{tab-set}

:::{tab-item} Linux
Connect from your local terminal with `-Y` (trusted X11 forwarding):

```bash
ssh -Y <username>@nt.swin.edu.au
```

Substitute `ozstar.swin.edu.au` to connect to OzSTAR.
:::

:::{tab-item} macOS
1. Install [XQuartz](https://www.xquartz.org/) and log out and back in if prompted by the installer.
2. Connect from Terminal with `-Y`:

   ```bash
   ssh -Y <username>@nt.swin.edu.au
   ```

   Substitute `ozstar.swin.edu.au` to connect to OzSTAR.
:::

:::{tab-item} Windows (WSL — recommended)
1. Enable Linux GUI application support in WSL following the [Microsoft WSL GUI apps guide](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).
2. From your WSL terminal, connect with `-Y`:

   ```bash
   ssh -Y <username>@nt.swin.edu.au
   ```

   Substitute `ozstar.swin.edu.au` to connect to OzSTAR.
:::

:::{tab-item} Windows (legacy without WSL)
On older Windows versions without WSL:

1. Install and start a third-party Windows X11 server before connecting.
2. If you connect with [PuTTY](https://www.putty.org/), open **Connection > SSH > X11** and select **Enable X11 forwarding** before opening the session.
:::

::::

## VNC sessions

Use Virtual Network Computing (VNC) when an application requires a full desktop environment or when X11 forwarding feels sluggish over a high-latency network (for example, when rendering detailed 2D images or 3D graphics).

### Step 1: Start a VNC server on your assigned login node

Do not use the round-robin `nt.swin.edu.au` or `ozstar.swin.edu.au` addresses for VNC, because your SSH tunnel must reconnect to the exact same login node. Run `myhome` on any login node first to find your assigned login node (see [Assigning a login node with myhome](ssh-access.md#assigning-a-login-node-with-myhome)).

Connect directly to your assigned login node (the example below uses `tooarrana1.hpc.swin.edu.au`), clear any loaded modules, set a VNC password, and start the server:

```bash
ssh <username>@tooarrana1.hpc.swin.edu.au
ml purge
vncpasswd
vncserver
```

`vncserver` starts on the first available display number (such as `:1`) and prints output similar to:

```text
New 'tooarrana1:1 (<username>)' desktop is tooarrana1:1

Starting applications specified in /home/<username>/.vnc/xstartup
Log file is /home/<username>/.vnc/tooarrana1:1.log
```

You only need to run `vncpasswd` once. Running `vncserver` again starts an additional session on the next available display number (`:2`, `:3`, and so on).

### Step 2: Forward the VNC port over SSH

Open a new terminal on your **local computer** and create an SSH tunnel to the same login node. Match the port to your display number (`5901` for `:1`, `5902` for `:2`, and so on):

```bash
ssh -L 5901:localhost:5901 -N <username>@tooarrana1.hpc.swin.edu.au
```

Leave this terminal open while using VNC.

### Step 3: Connect with a VNC client

Open a VNC client on your local computer, connect to `localhost:5901` (matching your forwarded port), and enter the password you created with `vncpasswd`.

Supported VNC clients include:

- [TigerVNC](https://tigervnc.org/) (Linux, macOS, Windows)
- [RealVNC Viewer](https://www.realvnc.com/) (Linux, macOS, Windows)
- Built-in macOS **Screen Sharing** (in Finder, select **Go > Connect to Server** and enter `vnc://localhost:5901`)

Once connected, launch graphical applications from a terminal inside the VNC desktop window.

### Step 4: Stop the VNC server when finished

Always stop your VNC server when you finish so unused desktop sessions do not consume resources on shared login nodes.

On the login node where you started VNC, list running sessions and stop yours:

```bash
vncserver -list
vncserver -kill :<display_number>
```

Replace `<display_number>` with your session number (for example, `vncserver -kill :1`).

## Troubleshooting

If X11 windows fail to open or your VNC desktop closes immediately after starting, check whether your shell startup files (`~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`) load any software modules. Remove module loads from your dotfiles and run `ml purge` before launching VNC — see [Dotfiles and shell hygiene](linux-environment.md#dotfiles-and-shell-hygiene).

## Next steps

- [Dotfiles and shell hygiene](linux-environment.md#dotfiles-and-shell-hygiene) — prevent module conflicts with X11, VNC, and Emacs.
- [Jupyter Notebooks](../software/notebooks.md) — run interactive browser or VS Code notebooks via SSH port forwarding.
- [Connecting via SSH](ssh-access.md) — configure SSH shortcuts and connection reuse.
