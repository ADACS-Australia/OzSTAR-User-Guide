# Frequently Asked Questions

Quick fixes for common login, quota, Slurm, and shell environment errors on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor, plus the origins of Swinburne's cluster names.

## Access and accounts

### Why am I getting "Permission denied" when logging in?

Check these three causes in order:

1. **2FA not enrolled:** If you have not enrolled in two-factor authentication, SSH immediately returns `Permission denied` without asking for a code. Complete enrollment in the [Accounts Portal](https://supercomputing.swin.edu.au/account-management/) — see [Two-Factor Authentication (2FA)](../getting-started/2fa.md).
2. **Wrong credentials or SSH key:** Confirm you are using your OzSTAR username and password (or registered SSH key). OzSTAR accounts are separate from Swinburne university logins.
3. **Expired account:** Accounts expire after 2 years (see [Account expiry and renewal](../getting-started/accounts.md#account-expiry-and-renewal)). Sign in to the [Accounts Portal](https://supercomputing.swin.edu.au/account-management/) to check your expiry date or request renewal, or contact [User Support](support.md).

### How do I change or reset my login password?

While logged in via SSH, run:

```bash
passwd
```

If you cannot log in, reset your password through the [Accounts Portal password reset page](https://supercomputing.swin.edu.au/account-management/forget_password). See [Changing or resetting your password](../getting-started/accounts.md#changing-or-resetting-your-password) for more details.

### How do I avoid SSH session timeouts?

Add `ServerAliveInterval 120` to `~/.ssh/config` on your local machine and restrict permissions on the file:

```bash
chmod 600 ~/.ssh/config
```

See [Connecting via SSH](../access/ssh-access.md) for a complete `~/.ssh/config` setup including host shortcuts and connection multiplexing.

### Who is eligible for an account, and how do I connect?

See [Accounts and Projects](../getting-started/accounts.md) for eligibility, project creation, and renewal rules, and [Connecting via SSH](../access/ssh-access.md) for login hostnames and SSH client setup.

## Storage and quotas

### Why am I getting "Disk quota exceeded"?

Run `quota` on any node to see which `/home` or `/fred/<project>` capacity or file-count limit you have reached:

```bash
quota
```

Move large data, Conda environments, or build directories out of `/home` into `/fred/<project>` or `/aphid/scratch-3month`. See [Filesystems and Storage](../storage/filesystems.md) for quotas and retention rules.

## Jobs and Slurm

### Why was my `sbatch` or `sinteractive` submission rejected?

| Rejection reason | Cause | Fix |
|---|---|---|
| `--exclusive` rejected | `--exclusive` is not permitted on `sbatch`. | Remove `--exclusive` and request exact cores with `--cpus-per-task` or `--ntasks`. |
| High memory per core or `--mem=0` | Slurm enforces a per-core memory ceiling and rejects `0`. | Request more CPU cores (or less memory) to lower memory per core, and specify an explicit memory limit. |
| `--gres=tmp:...` rejected | Local scratch (`$JOBFS`) is not requested via `--gres`. | Replace `--gres=tmp:...` with `--tmp=<size>` (default is `250M`). |
| Internal partition rejected (e.g. `milan-gpu`, `milan-c`) | Partitions are routed internally based on login node and resources. | Remove `#SBATCH --partition=...` and submit from the matching login node (`tooarrana1/2` for NT, `farnarkle1/2` for OzSTAR). |
| Multi-node core count rejected | Multi-node CPU jobs must request full-node core multiples. | Request exact multiples of **64 cores** on NT or **32 cores** on OzSTAR, with `--cpus-per-task` dividing the node core count. |
| Interactive job rejected (`sinteractive` / `srun`) | Interactive allocations have a short core-time walltime limit that scales down with core count. | Reduce cores or `--time`, or submit a batch job with `sbatch`. |

See [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) for full scheduler rules and memory ceilings.

### Why do compute nodes have no internet access?

Stage external input files into `/fred/<project>` or `/home` before submitting your compute job (see [Transferring Files](../storage/file-transfer.md)). If your workflow requires automated downloads from external servers, run the download stage on the internet-enabled **Trevor** nodes and chain it to your NT or OzSTAR compute jobs with Slurm dependencies (see [Swinburne HPC Systems](../getting-started/systems.md)).

Compute nodes on NT and OzSTAR are isolated from external networks by design so network stalls or slow external servers cannot waste compute allocations or introduce security risks.

## Environment and software

### Why do NVIDIA, Slurm, or GPU commands fail inside `screen`?

Start a login shell inside each `screen` window (`bash -l` or `tcsh -l`), or use `tmux` instead:

```bash
bash -l
```

Linux clears `LD_LIBRARY_PATH` for security when launching setgid binaries such as `screen`, which breaks pre-loaded Slurm and NVIDIA modules (and interactive jobs launched inside `screen` inherit the broken environment). See [Persistent terminal sessions (tmux and screen)](../access/linux-environment.md#persistent-terminal-sessions-tmux-and-screen) for details.

### Why are Emacs, X11, VNC, or `rsync` failing?

Remove `module load` commands, library path overrides, and terminal output (such as `echo` banners) from your dotfiles (`~/.bashrc`, `~/.bash_profile`, `~/.cshrc`), then log out and log back in.

For Emacs specifically, start Emacs in a clean shell with no modules loaded and run workflow commands (with loaded modules) in a separate terminal or batch script. See [Dotfiles and shell hygiene](../access/linux-environment.md#dotfiles-and-shell-hygiene).

### How do I change my default login shell?

Run `changeShell` on any login node and follow the interactive prompts (standard `chsh` is unavailable because accounts are managed through LDAP):

```bash
changeShell
```

See [Changing your login shell](../access/linux-environment.md#changing-your-login-shell) for the list of supported shells and propagation details.

### Where can I learn GPU programming?

Explore these external GPU programming resources:

- [ENCCS GPU Programming Guide](https://enccs.github.io/gpu-programming/) — practical introduction to GPU concepts and programming models.
- [NVIDIA CUDA Developer Zone](https://developer.nvidia.com/cuda) — official CUDA toolkits, documentation, and learning guides.
- [NVIDIA GTC On-Demand Training](https://www.nvidia.com/gtc/training/) — searchable recordings of past workshops and domain-specific talks.

To submit GPU jobs on NT (A100) or OzSTAR (P100), see [Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md) and [Job Script Examples](../jobs/examples.md).

## About the clusters

### What is the meaning behind the machine names?

- **Ngarrgu Tindebeek (NT):** The name *Ngarrgu Tindebeek* was provided by Wurundjeri Elders through the assistance of the Moondani Toombadool Centre at Swinburne. It translates as *"Knowledge of the Void"* in the local Woiwurrung language and represents harnessing the power of a supercomputer to enable researchers to explain the unknown and push the boundaries of knowledge — such as understanding how black holes come together within galaxies, collide, and create gravitational waves.
- **Tooarrana:** NT's login nodes (`tooarrana1` and `tooarrana2`) are named after the *tooarrana*, an endangered native Australian animal.
- **OzSTAR and John Clarke:** Many components of the OzSTAR cluster are named in memory of the late satirist, actor, comedian, and writer [John Clarke](https://en.wikipedia.org/wiki/John_Clarke_(satirist)):
  - OzSTAR login nodes: `farnarkle`
  - Login-node cgroups: `grommet`
  - Main Lustre filesystem: `Dagg`, mounted at `/fred`
  - Lustre servers: `arkle`, `warble`, and `umlaut`
  - OzSTAR standard compute nodes: `john`; high-memory nodes: `bryan`
  - NT compute nodes: `dave`

## Next steps

- [User Support](support.md) — contact Swinburne HPC technical staff with diagnostic templates if your issue is not covered here.
- [Policies](../1-getting_started/Policies.rst) — review acceptable use, resource efficiency, and storage policies.
