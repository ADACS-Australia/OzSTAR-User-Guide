# User Support

Contact Swinburne HPC technical staff for assistance with accounts, jobs, storage, or software on Ngarrgu Tindebeek (NT), OzSTAR, and Trevor.

## Support scope and contact

:::{note}
Swinburne HPC does not operate a dedicated 24/7 support desk. Support is provided on a **best-effort basis** by a small team of HPC technical staff. We respond as soon as possible, though requests outside our capacity or scope may be politely declined.
:::

Before submitting a ticket, check the [Frequently Asked Questions](faq.md) for quick fixes to common login, quota, and Slurm issues.

Email [hpc-support@swin.edu.au](mailto:hpc-support@swin.edu.au) when you:

- Encounter an account, filesystem, or scheduler problem on NT, OzSTAR, or Trevor that you cannot resolve.
- Need advice on an efficient way to configure or launch a Slurm job.
- Have code that worked elsewhere (or previously on the cluster) and is now crashing or behaving unexpectedly.
- Need help installing software or want to request a shared system module.

:::{warning}
Never include passwords, SSH private keys, 2FA setup keys, or 2FA recovery codes in support emails.
:::

:::{note}
Support requests are tracked in JIRA. After emailing `hpc-support@swin.edu.au`, you may receive an email with a link to the JIRA web interface. The web interface is only accessible from the Swinburne network or VPN, but web access is not required — replying directly by email updates your ticket from any network.
:::

## Ticket templates

Including complete diagnostic details in your first email helps staff resolve your issue faster. Copy and fill in the template matching your request.

### General or job issue

```text
Subject: <short summary of the issue>

Username: <username>
Cluster / login node: <NT (tooarrana1/2) | OzSTAR (farnarkle1/2) | Trevor>
Job ID (if applicable): <job_id>

Summary of the issue:
<describe what went wrong>

Steps to reproduce:
1. <command or action>
2. <command or action>

Expected result:
<what you expected to happen>

Actual result:
<exact error message or observed behaviour>

Output of `module list`:
<paste output>

Output of `printenv` (redact any personal tokens or secrets if present):
<paste output>
```

### New module request

We encourage you to install single-group or fast-moving software in your own project directory — see [Installing your own software](../software/modules.md#installing-your-own-software).

If a package is stable and widely used across multiple research groups on the facility, we may consider installing it as a shared module. Include the following details in your request:

```text
Subject: Module request: <package_name> <version>

Username: <username>
Target cluster(s): <NT | OzSTAR | both>
Package name and version: <package_name> <version>
Source code or installer URL: <https://...>
Expected number of users / research groups: <estimate>
Additional details (dependencies, GPU support, compiler requirements):
<notes>
```

## Next steps

- [Frequently Asked Questions](faq.md) — check common error fixes before opening a ticket.
- [Monitoring and Managing Jobs](../jobs/monitoring.md) — gather Job IDs, `sacct` output, and Job Monitor details for job tickets.
- [Policies](../1-getting_started/Policies.rst) — review facility usage, acknowledgement, and data retention policies.
