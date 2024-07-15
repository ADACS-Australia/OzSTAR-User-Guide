.. highlight:: rst

Tracking LIGO Job Usage
==================================
All LIGO users are required to include a specific tag in the comment field of their Slurm sbatch scripts when running LIGO-related jobs. This helps both us and LIGO track the supercomputer's contributions to LIGO research. You can determine the appropriate tag for your job using the `LDG tag generator <https://ldas-gridmon.ligo.caltech.edu/ldg_accounting/user>`_.

Adding the tag
----------------------------------
When submitting a job, include the following tag in your sbatch script's directives:
::

    #SBATCH --comment="ligo.example.tag"