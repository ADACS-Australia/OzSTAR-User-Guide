.. highlight:: rst

Tracking LIGO Job Usage
==================================
All LIGO users are required to include a specific tag in the comment field of their Slurm sbatch scripts when running LIGO-related jobs. This helps both us and LIGO track the supercomputer's contributions to LIGO research.

Adding the tag
----------------------------------
You can determine the appropriate tag for your job using the `LDG tag generator <https://ldas-gridmon.ligo.caltech.edu/ldg_accounting/user>`_. If you are unsure of which tag to choose you should consult with members of your research group and/or the Chair of the relevant LIGO Working Group. It is important that you make every effort to determine if your workflow falls within one of the available categories and then use the corresponding tag.

When submitting a job, include the tag in your sbatch script's directives:
::

    #SBATCH --comment=ligo.example.tag

Custom tags
----------------------------------
If your job is related to GW science but sits outside of the tag categories please include a custom tag in the following format:
::

    ligo.ozstar.sci.misc.xxxx

where ``xxxx`` is a label appropriate to your job, e.g. ``compas``. This label should consist of no more than 10 alphanumeric characters. However, please only use this option after taking the time to determine if your workflow does have an appropriate official tag.