.. highlight:: rst

Job Monitor
============

https://supercomputing.swin.edu.au/monitor/

The Job Monitor provides a web graphical interface to view the resource usage of your jobs in real time. We recommend checking the Job Monitor regularly to ensure that your jobs are running efficiently, especially if you are running a new workflow for the first time.

.. warning ::
    Please do not run the ``squeue`` command at a high frequency (e.g. using the ``watch`` command. This incurs a high performance penalty on the scheduler. The Job Monitor provides in realtime the same information (whether your job has started yet or finished yet) without the performance penalty.

Usage
-----

#. Select your username (abbreviated to the first 3 letters) from the list on the left.
#. A list of your jobs will appear in the center column, showing the Job ID, name, and elapsed time. Select a job to view its resource usage.
#. Detailed graphs will appear on the right column. The upper section shows the resources used exclusively by your job, whereas the lower section shows the total resources used by your job and all other jobs running on the same node.

The job monitor detects if a job is not fully utilising the resources allocated to it. This is indicated by the warnings in red. If you see this, please reduce the amount of resources being requested in your job script, or fix any efficiency issues with your code. If in doubt, please contact us for assistance.

Performance statistics can also be viewed on the node directly by connecting via SSH and running the ``htop`` command. You will only be able to SSH into a node if you have a job running on that node.

Past Jobs
---------

The "Past" tab shows a timeline of the total system usage over the past 24 hours. To jump back to a snapshot of the system at a particular time, click on the timeline. This shows the state of the system at that point in time. Entering your username in the filter box will show how many of your jobs were running at any given time. This can be useful for finding jobs that have already finished in the last 24 hours.

Future Resources
----------------

The "Future" tab shows the available resources via backfill. Backfill is a way of filling the gaps in the queue with jobs that can run in the time before the next job in the queue. This allows the system to be used more efficiently. Each bar on the graph is a backfill slot which may begin instantly. The horizontal axis indicates the number of cores in that slot, and the vertical axis indicates the amount of time available in that slot. For example, a 4-core slot with 30 minutes means that your job may start instantly if it requests fewer than 4 cores and fewer than 30 minutes, because there is a gap in the queue that can be filled by your job.

The same information can be viewed via the command line interface on the login nodes.

To see the current jobs in the queue

::

    showq

To see the available backfill slots

::

    showbf

To see the allocation status of the resources

::

    qinfo -v
