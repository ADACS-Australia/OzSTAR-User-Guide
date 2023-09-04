.. highlight:: rst

Job Monitor
============

https://supercomputing.swin.edu.au/monitor/

The Job Monitor provides a web graphical interface for monitoring your jobs on the OzSTAR supercomputers. It provides a way to view the resource usage of your jobs in real time. We recommend checking the Job Monitor regularly to ensure that your jobs are running efficiently, especially if you are running a new workflow for the first time.

.. note ::
    Please do not run the ``squeue`` command at a high frequency. This incurs a high performance penalty on the scheduler. The Job Monitor provides in realtime the same information (whether your job has started yet or finished yet) without the performance penalty.

Usage
-----

#. Select your username (abbreviated to the first 3 letters) from the list on the left.
#. A list of your jobs will appear in the center column, showing the Job ID, name, and elapsed time. Select a job to view its resource usage.
#. Detailed graphs will appear on the right column. The upper section shows the resources used exclusively by your job, whereas the lower section shows the total resources used by your job and all other jobs running on the same node.

The job monitor detects if a job is not fully utilising the resources allocated to it. This is indicated by the warnings in red. If you see this, please reduce the amount of resources being requested in your job script, or fix any efficiency issues with your code.

Performance statistics can also be viewed on the node directly by connecting via SSH and running the ``htop`` command.

Past Jobs
---------

The "Past" tab shows a timeline of the total system usage over the past 24 hours. To jump back to a snapshot of the system at a particular time, click on the timeline. This shows the state of the system at that point in time.

Future Resources
----------------

The "Future" tab displays two panels. The first is a list of the current jobs waiting in the queue. This shows how much demand there is for the system. The second panel shows the available resources via backfill. Backfill is a way of filling the gaps in the queue with jobs that can run in the time before the next job in the queue. This allows the system to be used more efficiently. Each bar on the graph is a backfill slot which may begin instantly. The horizontal axis indicates the number of cores in that slot, and the vertical axis indicates the amount of time available in that slot. For example, a 4-core slot with 30 minutes means that your job may start instantly if it requests fewer than 4 cores and fewer than 30 minutes, because there is a gap in the queue that can be filled by your job.

The same information can be viewed via the command line interface on the login nodes.

To see the current jobs in the queue::
    showq

To see the available backfill slots::
    showbf

To see the allocation status of the resources::
    qinfo -v
