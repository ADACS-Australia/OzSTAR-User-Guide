.. highlight:: rst

Guide for beta testers
======================

Thank you for offering to test OzSTAR's latest supercomputer, Ngarrgu Tindebeek.

Goals
-----
We are interested in hearing as much feedback as you can give on areas such as:

* The modules system
* Performance comparisons between the new nodes and existing OzSTAR
* Bugs and errors

Benefits
--------
Since there are very few test users on the system now, most of the system (over 10,000 CPU cores) is completely free, and jobs will start almost instantly. You are welcome to take this rare opportunity to run some large simulations that you would otherwise need to run at other larger supercomputing facilities. This helps us test the system under load.

Once the system is officially opened to all users, the queue will be much busier, and it will be harder to run large jobs with zero wait time.

Getting started
---------------
You can access the new login nodes by SSH into ``tooarrana1/2`` via ``farnarkle1/2``. These login nodes are not currently accessible externally, but will be once NT is officially opened to all users.

.. note::
    While the new system is still being set up, the login nodes may be restarted without warning at any time.

Software
--------
From the new login nodes, you can run ``module avail`` and ``module spider`` to see the new apps tree.

.. note::
    NT's module system has new features compared to OzSTAR's, and behaves slightly differently. We have included helpful hints to the output of these commands, which we encourage you to read.

A brand new set of software has been installed, and modules that you used on OzSTAR may not be available. When compiling your code, we recommend using the ``foss/2022a`` toolchain, which contains GCC 11.3.0.

Accessing project directories
-----------------------------
You will be able to access the project directories of any OzSTAR projects that you are already part of.

.. note::
    While the high-speed connection between NT's compute nodes and the Lustre storage is still being set up, read and write access to project directories may be slow. We recommend testing with jobs that only periodically write to the storage. For example, simulations that write snapshots at 10 minute intervals, rather than analysis scripts that are constantly loading files.
