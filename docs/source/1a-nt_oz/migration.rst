.. highlight:: rst

Migrating to Ngarrgu Tindebeek
==============================
**This page contains information that is very important for users of the original OzSTAR cluster. Please read it carefully.**

Current configuration
-------------------------------

The Ngarrgu Tindebeek (NT) nodes (``tooarrana, ``dave``, and ``gina``), along with the internet-connected Trevor nodes (``trevor``) run the AlmaLinux 9 operating system. These nodes also have access to a new and improved set of modules.

In contrast, the OzSTAR nodes (``farnarkle``, ``john``, and ``bryan``) currently run the CentOS 7 operating system and have access to the old set of modules.

Upcoming reboot of OzSTAR nodes
-------------------------------

On 26 September 2023, the OzSTAR nodes will be rebooted and upgraded to AlmaLinux 9. This will bring them in line with the NT nodes. The OzSTAR nodes will be unavailable for a few days during this time. This upgrade will enable them to access the new set of modules.

.. note::
    Although the set of modules will appear to be the same on the OzSTAR, NT, and Trevor nodes, the underlying software will be different because each of these clusters have a different CPU architecture. This means that you will need to recompile your code for each cluster, even if you are using the same modules/compilers.

All workflows that currently use the OzSTAR nodes will stop working if they rely on the old set of modules or libraries in the operating system (99% of workflows). To minimise disruption, we recommend that you migrate your workflows to the NT nodes as soon as possible. This will give you time to test your workflows and make sure that they work on the new cluster before the OzSTAR cluster's operating system is upgraded.

Once the OzSTAR nodes are upgraded, you will be easily able to port your NT workflows to the OzSTAR nodes because the modules and system libraries will be nearly identical, noting that a recompile is still necessary (i.e. you will not be able to run a binary that was compiled on NT on OzSTAR). We expect, however, that most users will just prefer to stay on the NT nodes because they are newer, faster, and nearly 3x as many CPU cores. The main reason for migrating back onto the upgraded OzSTAR nodes is to take advantage of the additional CPU cores.
