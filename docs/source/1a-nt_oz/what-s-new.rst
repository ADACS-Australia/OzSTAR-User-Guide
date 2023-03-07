.. highlight:: rst

What's new on OzSTAR?
==========================

Access
-------

Entry point is now ``ozstar.swin.edu.au``.

Hardware
----------

160 standard compute nodes:

* 64-core AMD EPYC 7543 Processor
* XXX GB RAM
* XXX GB NVMe SSD

10 high-memory compute nodes:

* 64-core AMD EPYC 7543 Processor
* XXX GB RAM
* XXX GB NVMe SSD

22 GPU compute nodes:

* 64-core AMD EPYC 7543 Processor
* XXX GB RAM
* XXX GB NVMe SSD
* 4 Nvidia A100 GPUs

Projects and filesystem
------------

Ngarguu Tindebeek and the existing OzSTAR cluster shares the same project
management system and filesystem. You will be able to access your existing
project directories on both systems.

Limitations
-----------

- Maximum wall time **for a job** is 7 days.
- Maximum CPUs **per project** is 2500.
- Maximum GPUs **per project** is 100.

Queues
-------

As with with the OzSTAR cluster, you do not need to specify a Slurm queue. This
is determined automatically by the node you are submitting from. Jobs
submitted via ``tooarrana1/2`` will be sent to the new nodes.

Modules
-----------

Ngarguu Tindebeek continues to use software modules, but contains a new
software hierarchy and a fresh installation of the latest applications. See
:doc:`../2-ozstar/Modules` for more information.
