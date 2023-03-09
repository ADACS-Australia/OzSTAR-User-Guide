.. highlight:: rst

Swinburne HPC system
========================

OzSTAR supercomputing operates 2 supercomputers: the eponymous "OzSTAR", and the next generation machine "Ngarrgu Tindebeek". In addition to these  machines, OzSTAR also manages a cloud-based cluster "Trevor".

Ngarrgu Tindebeek
-----------------

Ngarrgu Tindebeek is OzSTAR's flagship machine, featuring 11,648 CPU cores and 88 GPUs in total.

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

Nodes are connected via NVIDIA Quantum-2 NDR InfiniBand switches with a data throughput of 200 Gbps.

OzSTAR
----------------

Installed in 2018, "OzSTAR" is the previous supercomputer, featuring 4140 CPU cores and 230 GPUS in total.

107 standard compute nodes:

* 2x 18-core Intel Gold 6140 GPUs
* 192 GB RAM
* 400 GB SSD
* 2x NVIDIA P100 12 GB GPUs

8 high-memory compute nodes:

* 384 or 768 GB RAM
* 2 TB NVMe SSD
* (other specs same as standard cmopute nodes)

Nodes are connected via Intel Omni-Path switches w ith a data throughput of 100 Gbps.

Trevor
------

The Trevor cluster is a set of cloud-based compute nodes designed for high-throughput applications (many small jobs). A key feature is internet connectivity to all compute nodes in the cluster, which enables workflows that rely on external access. This cluster provides an additional resource for small jobs, so that they don't have to compete in the queue with the two main supercomputers.

Since the cluster is based in the cloud, the number of nodes is variable and can be adjusted to meet demand.

* 12-core Intel CPUs (Haswell architecture)
* 30 GB RAM
* 10 GB SSD
