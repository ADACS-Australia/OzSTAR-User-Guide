# Transferring Files

Copy research data between your local computer and Swinburne HPC storage (`/home`, `/fred`, or `/aphid/scratch-3month`) using the dedicated data-mover nodes.

## Before you start

- Enroll in [Two-Factor Authentication (2FA)](../getting-started/2fa.md) and confirm you can connect via SSH ([Connecting via SSH](../access/ssh-access.md)).
- **Always use a data-mover node** (such as `data-mover01.hpc.swin.edu.au`; inspect live hosts with `sinfo -s -p datamover`) rather than a login node (`tooarrana1`/`tooarrana2` or `farnarkle1`/`farnarkle2`). Login nodes are shared for editing, compiling, and job submission; data-mover nodes are dedicated to file transfers (both interactive `rsync` and Slurm data-transfer jobs) and mount the same cluster filesystems.

:::{tip}
To avoid repeated 2FA prompts during interactive transfers, set up [Reusing SSH connections (multiplexing)](../access/ssh-access.md#reusing-ssh-connections-multiplexing) for the data-mover node you use. For automated or unattended transfers, see [Restricted SSH Keys for Automated Jobs](../access/restricted-keys.md).
:::

:::{warning}
Do **not** use Swinburne HPC storage as a backup for your laptop or workstation. Lustre storage is reserved for active compute workflows (see [Policies](../1-getting_started/Policies.rst)), and `/fred` and `/aphid/scratch-3month` are not backed up (see [Filesystems and Storage](filesystems.md)).
:::

## Copying files and directories

Choose the tab matching your local operating system. If you use Windows Subsystem for Linux (WSL), follow the Linux tab — native `rsync` is faster and easier to resume than graphical Windows clients.

:::::{tab-set}

::::{tab-item} Linux / macOS / Windows (WSL)

Use [`rsync`](https://download.samba.org/pub/rsync/rsync.1) (also available locally via `man rsync`) to transfer files and directories. `rsync` is preferred over `scp` because it handles directory trees reliably, preserves permissions cleanly, sends only changed data, and resumes interrupted transfers.

To upload files to Swinburne HPC, replace `<username>`, `<project>`, and the source/destination paths:

```bash
rsync -avPxH --no-g --chmod=Dg+s <path/to/local/files> <username>@data-mover01.hpc.swin.edu.au:/fred/<project>/<destination>/
```

To download files to your local machine, swap the source and destination arguments (omit `--no-g --chmod=Dg+s`, which are only needed when uploading into `/fred/<project>`):

```bash
rsync -avPxH <username>@data-mover01.hpc.swin.edu.au:/fred/<project>/<source>/ <path/to/local/destination>/
```

A trailing `/` on a source directory copies its *contents* into the destination directory; omitting the trailing `/` copies the directory itself inside the destination.

Recommended `rsync` options:

| Option | Purpose |
|---|---|
| `-a` (`--archive`) | Archive mode (recursive; preserves symlinks, permissions, timestamps, owner, group, and devices; equals `-rlptgoD`) |
| `-v` (`--verbose`) | Print transferred filenames and summary output |
| `-P` | Show per-file progress and keep partially transferred files (`--partial --progress`) |
| `-x` (`--one-file-system`) | Do not cross filesystem boundaries |
| `-H` (`--hard-links`) | Preserve hard links |
| `--no-g` | *(Uploads)* Do not preserve your local group ownership so files inherit the `/fred/<project>` project group |
| `--chmod=Dg+s` | *(Uploads)* Set the setgid bit on directories so new files inside inherit the project group |

:::{tip}
On slow network connections, add `-z` (`rsync -avzPxH ...`) to compress files in transit and decompress them at the destination. Omit `-z` when transferring already-compressed archives (such as `.gz`, `.bz2`, `.xz`, or `.sif` files) to save CPU overhead.
:::

For simple single-file copies, `scp` also works (run `man scp` locally), though `rsync` handles both single files and directory trees safely.

::::

::::{tab-item} Windows (WinSCP)

If you prefer a graphical client on Windows (outside WSL), install [WinSCP](https://winscp.net/eng/index.php).

1. Open WinSCP and create a **New Site** with:
   - **File protocol:** SFTP
   - **Host name:** `data-mover01.hpc.swin.edu.au` (or another live data-mover node listed by `sinfo -s -p datamover`)
   - **Port number:** `22`
   - **User name:** `<username>`
2. Click **Login**, enter your password or SSH key passphrase, and enter your 2FA code when prompted.
3. Navigate to `/fred/<project>/` or `/home/<username>/` in the remote pane and drag files between local and remote panels.

:::{note}
For large transfers or directories with many files, running `rsync` inside Windows Subsystem for Linux (see the Linux / macOS / Windows (WSL) tab) is faster and easier to resume cleanly.
:::

::::

:::::

## Resuming interrupted transfers

If an `rsync` transfer drops partway through, rerun the exact same `rsync` command with the same source and destination paths. Because `-P` retains partial files and `rsync` compares source against destination, only missing or modified files are transferred rather than restarting from scratch.

## Transferring code with Git

For source code and job scripts, host your code in a version-control repository using [Git](https://git-scm.com/) (for example on GitHub or GitLab) and clone or pull the repository directly on Ngarrgu Tindebeek (NT) or OzSTAR instead of manually copying files back and forth.

## Synchronising a local directory

You can mirror a local directory onto Swinburne HPC (or vice versa) with `rsync --delete`.

:::{warning}
`rsync --delete` performs a **one-way** mirror: any file in the destination that does not exist in the source is **permanently deleted**. Always preview changes with `--dry-run` (`-n`) first, double-check the source-to-destination direction, and note that one-way `--delete` does not scale beyond two synchronised trees.
:::

Preview what would be copied or deleted without modifying any files:

```bash
rsync -avPxH --no-g --chmod=Dg+s --delete --dry-run <path/to/source>/ <username>@data-mover01.hpc.swin.edu.au:/fred/<project>/<destination>/
```

Once the dry-run output looks right, rerun the command without `--dry-run`.

## Next steps

- [Filesystems and Storage](filesystems.md) — understand quotas, backups, and where to place transferred data.
- [Reusing SSH connections (multiplexing)](../access/ssh-access.md#reusing-ssh-connections-multiplexing) — avoid repeated 2FA prompts across interactive transfers.
- [Restricted SSH Keys for Automated Jobs](../access/restricted-keys.md) — set up 2FA-exempt keys for automated, unattended transfers.
- [Optimising Lustre I/O](optimising-lustre.md) — pack small files before reading or writing on Lustre.
