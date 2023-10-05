.. highlight:: rst

What's new?
===========

Access
------

There is a new direct entry point to NT via ``nt.swin.edu.au``. The existing login to the OzSTAR machine at ``ozstar.swin.edu.au`` remains accessible.

Hardware
--------

Ngarrgu Tindebeek has 11,648 CPU cores and 88 GPUs in total.

160 standard compute nodes:

* 2x 32-core AMD EPYC 7543 CPUs
* 256 GB RAM
* 2 TB NVMe SSD

10 high-memory compute nodes:

* 1024 GB RAM
* (other specs same as standard compute nodes)

22 GPU compute nodes:

* 512 or 1024 GB RAM
* 4x NVIDIA A100 80 GB GPUs
* (other specs same as standard compute nodes)

Nodes are connected via NVIDIA Quantum-2 NDR InfiniBand switches with a data
throughput of 200 Gbps.

Projects and filesystem
-----------------------

Ngarrgu Tindebeek and the existing OzSTAR cluster shares the same project management system and filesystem. The existing Lustre file system (/fred) will be upgraded to 19 PB, which is accessible on OzSTAR and Ngarrgu Tindebeek.

Limitations
-----------

- Maximum wall time **for a job** is 7 days.
- Maximum CPUs **per project** is 2500.
- Maximum GPUs **per project** is 100.

Queues
------

As with with the OzSTAR cluster, you do not need to specify a Slurm queue. This is determined automatically by the node you are submitting from. Jobs submitted via ``tooarrana1/2`` will be sent to the new nodes.

Modules
-------

Ngarrgu Tindebeek continues to use software modules, but contains a new software hierarchy and a fresh installation of the latest applications. See :doc:`../2-ozstar/Modules` for more information.

Environment
-----------
* The default number of OpenMP threads is now set to 1 using the environment variable ``OMP_NUM_THREADS=1`` (previously not defined by default). Users must explicitly change this value if they wish to use more than 1 thread.
