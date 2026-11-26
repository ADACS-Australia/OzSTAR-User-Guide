# Using AI Coding Tools

You remain solely responsible for every command, file edit, data transfer, and Slurm job executed under your account by an AI coding assistant or agent on Ngarrgu Tindebeek (NT) or OzSTAR (see [Policies — AI Tools and Agents](../1-getting_started/Policies.rst#ai-tools-and-agents)). Follow these operational practices when using tools such as Claude Code, OpenAI Codex, GitHub Copilot, OpenCode, or VS Code Remote-SSH AI extensions.

## Accountability and credential boundaries

Keep authentication and agent execution strictly within environments you directly control. Permitted workflows include:

- Running an AI coding assistant on your local workstation and connecting to NT or OzSTAR over your own 2FA-authenticated SSH session.
- Running a lightweight, interactively supervised CLI coding assistant or VS Code Remote-SSH session on your single assigned login node.

:::{warning}
**Prohibited workflows:** Consistent with the prohibition on credential sharing in [Policies — AI Tools and Agents](../1-getting_started/Policies.rst#ai-tools-and-agents), never give your OzSTAR password, SSH private keys, 2FA secrets, or recovery codes to third-party hosted cloud agents or remote services outside your control. Never run MCP servers, reverse SSH tunnels, web bridges, or open network listeners on login nodes to allow third-party hosted agents to access Swinburne HPC systems.
:::

If you use [SSH connection multiplexing](ssh-access.md#reusing-ssh-connections-multiplexing), remember that any local process running under your user account — including local AI tools — can reuse an open control socket without a 2FA prompt under `ControlMaster auto`. Prefer `ControlMaster autoask` on Linux desktops and close sockets (`ssh -O exit ...`) when finished.

## Keep a human in the loop

- Require explicit human approval before your AI tool runs shell commands, deletes or overwrites files, or submits jobs with `sbatch`.
- Do not run unsupervised auto-accept or "bypass permissions" loops (for example, overnight autonomous loops that repeatedly edit code, submit jobs, and poll Slurm). A misbehaving loop can rapidly flood the scheduler, exhaust disk quotas, or destroy unbacked-up data, resulting in immediate account restriction without notice.
- Review every generated `sbatch` script and command before running it; AI models frequently invent invalid Slurm flags or nonexistent module versions.

## Stay on one login node (myhome)

Run `myhome` on any login node to find your assigned login node (see [Assigning a login node with myhome](ssh-access.md#assigning-a-login-node-with-myhome)):

```bash
myhome
```

Point VS Code Remote-SSH and any interactive AI coding session directly at your assigned node (for example, `tooarrana1.hpc.swin.edu.au`) rather than round-robin `nt.swin.edu.au` or `ozstar.swin.edu.au`. Never launch editors, language servers, or coding agents across multiple login nodes at the same time.

## Protect shared infrastructure

Login nodes, Lustre metadata servers, and the Slurm controller are shared by every researcher on the facility.

- **Keep heavy work off login nodes:** Do not allow an AI tool to run model training, benchmarks, large test suites, or multi-core parallel builds on login nodes. Submit heavy jobs with `sbatch`, or use a short `sinteractive` session for interactive testing ([Requesting Resources and Interactive Jobs](../jobs/resources-and-interactive.md)).
- **Do not scan Lustre filesystem roots:** Never point an agent, IDE workspace, file watcher, or recursive search (`find /`, `grep -r`, `du`, `ls -R`) at `/fred`, `/fred/<project>`, `/home`, or `/aphid`. Broad directory walks overload the shared Lustre metadata servers for all users. Open only your specific repository subdirectory (for example, `/fred/<project>/<username>/<repo>`), exclude large data directories via `.gitignore` or your tool's ignore settings, and bound search depth. See [Optimising Lustre I/O](../storage/optimising-lustre.md).
- **Do not poll Slurm in tight loops:** Never run `watch squeue` or let an agent poll `squeue`, `sacct`, or `sinfo` every few seconds. Use the [Web Job Monitor](https://supercomputing.swin.edu.au/monitor/) or infrequent `squeue --me` checks instead ([Monitoring and Managing Jobs](../jobs/monitoring.md)).

## Protect your data and other users' privacy

:::{warning}
Files on `/fred` and `/aphid` are **not backed up** ([Filesystems and Storage](../storage/filesystems.md)). An erroneous delete or overwrite by an AI agent can cause permanent data loss.
:::

- **Guard against accidental data loss:** Commit your work to Git before letting an agent modify files, scope write permissions strictly to your project subdirectory, and run experimental or untrusted commands inside an [Apptainer container](../software/apptainer.md).
- **Follow institutional AI and IP rules:** Swinburne HPC takes no responsibility for code, datasets, or intellectual property transmitted to third-party AI providers. Confirm your usage complies with the [Swinburne Artificial Intelligence Usage Procedures](https://www.swinburne.edu.au/about/policies-regulations/artificial-intelligence-usage-procedures/) (where applicable) and the AI, privacy, data security, and IP policies of your host institution.
- **Keep secrets and other users out of AI context:** Never allow an AI tool to inspect `~/.ssh/`, credentials, API keys, or restricted datasets. When checking jobs or processes during an AI-assisted session, scope commands strictly to your own account so other users' usernames, job names, and command lines are not sent to external AI services:

  ```bash
  squeue --me
  ps -u "$USER"
  ```

## Starter AGENTS.md / CLAUDE.md for OzSTAR and NT

Many AI coding assistants automatically read an instruction file (`AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`) at the root of your repository. Copy this starter template into your repository and replace `<project>` and `<username>` so your assistant follows Swinburne HPC's verified rules from the start:

```markdown
# Swinburne HPC (Ngarrgu Tindebeek & OzSTAR) Operational Rules

## Login nodes and compute
- Run `myhome` to stay on my single assigned login node (`tooarrana1/2` on NT; `farnarkle1/2` on OzSTAR).
- Never run heavy compute, benchmarks, large test suites, or multi-core builds on login nodes; submit with `sbatch` or run brief interactive tests with `sinteractive` (interactive walltime decreases as core count increases).
- Do not open servers, tunnels, or bridges on login nodes for external services.

## Filesystems and Lustre safety
- `/home` has a small fixed quota (check usage and limits with `quota`); place project files under `/fred/<project>/<username>/` (not backed up) or temporary scratch under `/aphid/scratch-3month/` (not backed up, automatically purged after inactivity).
- Never run broad recursive `find`, `grep -r`, `du`, `ls -R`, or file watchers at `/fred`, `/fred/<project>`, `/home`, or `/aphid` roots. Stay inside this repository directory and exclude large data directories.
- Never read `~/.ssh/`, credentials, tokens, or restricted datasets.

## Software modules and shell hygiene
- Do not guess module names or versions; discover them with `module spider <package>` and `module avail`.
- Keep `~/.bashrc` free of `module load` statements; load required modules inside batch scripts.
- Remember NT, OzSTAR, and Trevor have different CPU architectures: recompile binaries and recreate Python/Conda environments per cluster.

## Slurm batch script rules
- Never specify `--exclusive` on `sbatch` (rejected; request cores with `--cpus-per-task` / `--ntasks`).
- Use `--tmp=<size>` for `$JOBFS` local scratch (omitting it allocates only a minimal default); never use `--gres=tmp:...` (rejected).
- Keep memory-per-core requests modest and never set `--mem=0` or `--mem-per-cpu=0` (rejected); if Slurm rejects a high memory-per-core request, ask for additional CPU cores or less memory.
- Explicitly set `OMP_NUM_THREADS` for multithreaded jobs (default is `1`).
- Multi-node CPU jobs must request full-node core multiples for the target cluster (check node core counts with `sinfo -o "%P %c %m %G"`).
- Do not attempt `scontrol update` on queued jobs (disabled for non-root users; `scancel` and resubmit).

## Monitoring, privacy, and approval
- Never run `watch squeue` or tight polling loops against Slurm.
- Scope inspection commands to my account only (`squeue --me`, `ps -u "$USER"`).
- Ask for explicit confirmation before deleting files, running destructive Git commands, or running `sbatch`.
```

## Next steps

- [Policies — AI Tools and Agents](../1-getting_started/Policies.rst#ai-tools-and-agents) — read the formal facility policy governing AI tools and agents.
- [Connecting via SSH](ssh-access.md) — set up `myhome` login-node shortcuts and safe SSH multiplexing.
- [Creating and Submitting Jobs](../jobs/creating-jobs.md) — review Slurm script requirements before submitting AI-assisted code.
