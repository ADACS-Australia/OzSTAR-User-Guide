# Linux Environment and Shell

Ngarrgu Tindebeek (NT), OzSTAR, Trevor, and the data-movers run an Enterprise Linux distribution binary-compatible with [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) (such as [AlmaLinux](https://almalinux.org/) or [Rocky Linux](https://rockylinux.org/); run `cat /etc/os-release` on any node to check the exact OS release). Use this guide to learn Linux shell basics, read manual pages, change your login shell, run persistent terminal sessions, and avoid common dotfile issues.

## Learning the Linux command line

Because all Swinburne HPC workflows run on Enterprise Linux via the command line, spend time becoming comfortable with core Linux commands before submitting production jobs. Most Red Hat Enterprise Linux documentation applies directly.

Recommended introductory resources:

- [30 Days of Linux: A Complete Guide for Beginners (GeeksforGeeks)](https://www.geeksforgeeks.org/linux-unix/30-days-of-linux/)
- [UNIX Tutorial for Beginners (University of Surrey)](https://info-ee.surrey.ac.uk/Teaching/Unix/)
- [Linux Survival (interactive browser tutorial)](https://linuxsurvival.com/)

## Reading man pages

Most Linux commands include built-in documentation accessible through the `man` (manual) command:

```bash
man <command>
```

For example, to inspect flags and options for `ls`:

```bash
man ls
```

Use the arrow keys or `Space` to scroll, `/` followed by a search term to search, and `q` to quit. Manual pages follow a consistent layout — **NAME**, **SYNOPSIS**, **DESCRIPTION**, options, and examples:

```text
LS(1)                           User Commands                          LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List information about the FILEs (the current directory by default).
       Sort entries alphabetically if none of -cftuvSUX nor --sort is
       specified.

       Mandatory arguments to long options are mandatory for short options too.

       -a, --all
              do not ignore entries starting with .

       -A, --almost-all
              do not list implied . and ..

       --author
              with -l, print the author of each file
...
```

## Changing your login shell

User accounts on Swinburne HPC are managed via LDAP, so the standard `chsh` command is not available. To change your default login shell, run `changeShell` on any login node and follow the prompts:

```bash
changeShell
```

Available login shells:

- `bash`
- `zsh`
- `csh`
- `tcsh`
- `ksh`

Changes take a few minutes to propagate across nodes; log out and log back in for your chosen shell to take effect.

## Persistent terminal sessions (tmux and screen)

To keep long-running interactive terminals alive across network drops, use `tmux` on your single `myhome`-assigned login node (see [Assigning a login node with myhome](ssh-access.md#assigning-a-login-node-with-myhome)).

:::{important}
Prefer **`tmux`** over **`screen`**. Linux strips `LD_LIBRARY_PATH` for security reasons when launching setgid executables such as `screen`, which breaks the pre-loaded `slurm` and `nvidia` modules. Interactive Slurm jobs (`srun` or `sinteractive`) started inside `screen` inherit that broken environment.
:::

If you must use `screen`, start a login shell inside each new `screen` window to restore your module paths:

```bash
# For bash users
bash -l

# For tcsh users
tcsh -l
```

## Dotfiles and shell hygiene

Dotfiles (such as `~/.bashrc`) let you customise your interactive prompt and shell aliases (see the [freeCodeCamp `.bashrc` customisation guide](https://www.freecodecamp.org/news/bashrc-customization-guide/) for general concepts).

:::{warning}
Many login, file-transfer, X11, VNC, and batch-job failures stem from `module load` commands or unexpected output in `~/.bashrc` and other dotfiles. Do **not** load software modules or set workflow-specific environment variables in your dotfiles — place them inside your Slurm batch script instead.
:::

Keep your dotfiles minimal for three reasons:

- **Reproducibility:** Modifying dotfiles later can silently break older batch scripts when you revisit them months or years later.
- **Workflow isolation:** Loading modules globally causes library version conflicts between separate projects and applications.
- **Reliable logins and file transfers:** Printing text to standard output from a non-interactive shell startup file breaks `rsync` and `scp`. Avoid sourcing shared dotfiles edited by other project members, as their changes can unexpectedly break your login.

### Fixing X11, VNC, and Emacs library conflicts

- **X11 forwarding and VNC:** Software modules that bundle X11 or GUI libraries can override system libraries and prevent graphical windows or VNC servers from starting. Remove all `module load` statements from your dotfiles and run `ml purge` before starting a VNC server (see [Graphical Access (X11 and VNC)](graphical-access.md)).
- **Emacs:** Emacs links against system shared libraries that can conflict with libraries supplied by loaded software modules. Remove `module load` statements from your dotfiles and launch Emacs from a clean shell with no modules loaded (`ml purge`), loading build or compute modules in a separate terminal window — or start Emacs first before loading modules in that shell.

## Next steps

- [Environment Modules and Installing Software](../software/modules.md) — discover and load software cleanly inside scripts and interactive sessions.
- [Graphical Access (X11 and VNC)](graphical-access.md) — run X11 windows or VNC desktops on your assigned login node.
- [Creating and Submitting Jobs](../jobs/creating-jobs.md) — put module loads and environment setup inside Slurm batch scripts.
