.. highlight:: rst

Migrating to Ngarrgu Tindebeek
==============================
**This page contains information that is very important for users of the original OzSTAR cluster. Please read it carefully.**

Current configuration
---------------------

The Ngarrgu Tindebeek (NT) nodes (the "milan" partition, with nodes ``tooarrana``, ``dave``, and ``gina``), along with the internet-connected Trevor nodes (``trevor``) run the AlmaLinux 9 operating system (functionally identical to RHEL9). These nodes also have access to a new and improved set of modules.

In contrast, the OzSTAR nodes (the "skylake" partition, with nodes ``farnarkle``, ``john``, and ``bryan``) and data-mover nodes ("datamover" partition, with nodes ``data-mover``) currently run the CentOS 7 operating system (functionally identical to RHEL7) and have access to the old set of modules.

Upcoming reboot of OzSTAR nodes
-------------------------------

On 26 September 2023, the OzSTAR nodes will be rebooted and upgraded to a RHEL9 equivalent. This will bring them in line with the NT nodes, streamlining support, maintenance, and security updates. The OzSTAR nodes will be unavailable for a few days during this time. This upgrade will enable them to access the new set of modules.

.. note::
    Although the set of modules will appear to be the same on the OzSTAR, NT, and Trevor nodes, the underlying software will be different because each of these clusters have a different CPU architecture. It also means that you will need to recompile your code for each cluster, even if you are using the same modules/compilers.

Migration
---------

All workflows that currently use the OzSTAR nodes will stop working if they rely on the old set of modules or libraries in the operating system (99% of workflows). To minimise disruption, we recommend that you migrate your workflows to the NT nodes as soon as possible. This will give you time to test your workflows and make sure that they work on the new cluster before the OzSTAR cluster's operating system is upgraded.

Once the OzSTAR nodes are upgraded, you will be easily able to port your NT workflows to the OzSTAR nodes because the modules and system libraries will be nearly identical, noting that a recompile is still necessary (i.e. you will not be able to run a binary that was compiled on NT on OzSTAR). We expect, however, that most users will just prefer to stay on the NT nodes because they are newer, faster, and nearly 3x as many CPU cores. The main reason for migrating back onto the upgraded OzSTAR nodes is to take advantage of the additional CPU cores.

Python Environments
^^^^^^^^^^^^^^^^^^^

In general, Python environments created on one cluster will not work on the other cluster. This is because packages may be built specifically for one architecture. For example, if you create a Python environment on the NT nodes, it will not work on the OzSTAR nodes. The same is true in reverse. To migrate your existing Python environments from OzSTAR to NT, you will need to recreate them on the NT nodes.

If you are using Python virtual environments, first activate the environment on the OzSTAR nodes, then run the following command to export the environment to a file:

::

    pip freeze > requirements.txt

Then, on the NT nodes, create a new virtual environment on NT and install the packages from the file:

::

    pip install -r requirements.txt

If you are using conda environments, first activate the environment on the OzSTAR nodes, then run the following command to export the environment to a file:

::

    conda env export > environment.yml

Then, on the NT nodes, create a new conda environment and install the packages from the file:

::

    conda env create -f environment.yml
