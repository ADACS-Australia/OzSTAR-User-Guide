# Tracking LIGO Job Usage

Include a mandatory LIGO accounting tag (`#SBATCH --comment=...`) in every LIGO-related batch script submitted on Ngarrgu Tindebeek (NT) or OzSTAR so Swinburne and LIGO can track supercomputer contributions to LIGO research.

## Before you start

- Know how to write and submit a Slurm batch script — see [Creating and Submitting Jobs](creating-jobs.md).

## Select and add an official LIGO tag

1. Identify the tag matching your workflow using the [LDG tag generator](https://ldas-gridmon.ligo.caltech.edu/ldg_accounting/user). If you are unsure which category applies, check with members of your research group or the Chair of the relevant LIGO Working Group.
2. Add the tag as a `#SBATCH --comment` directive near the top of your batch script:

   ```bash
   #SBATCH --comment=ligo.example.tag
   ```

Always check whether your workflow fits an official LDG category before falling back to a custom tag.

## Custom gravitational-wave tags

If your job relates to gravitational-wave (GW) science but sits outside all official LDG categories, use a custom tag in the following format:

```bash
#SBATCH --comment=ligo.ozstar.sci.misc.<label>
```

Replace `<label>` with a short identifier for your job or code (for example, `compas`), using **no more than 10 alphanumeric characters**. Use a custom tag only after confirming that no official LDG tag applies to your workflow.

## Verify your tag is recorded

After submitting a job with `sbatch`, confirm that Slurm recorded your tag:

```bash
sjob <job_id> | grep Comment
```

## Next steps

- [Creating and Submitting Jobs](creating-jobs.md) — batch script structure and MAS `#SBATCH --account` settings.
- [Slurm Command Reference](slurm-reference.md) — quick reference for `#SBATCH` directives.
- [Policies](../1-getting_started/Policies.rst) — publication acknowledgement and facility reporting requirements.
