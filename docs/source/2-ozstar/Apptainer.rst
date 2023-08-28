Apptainer on OzSTAR
===================

Apptainer (formerly Singularity) enables users to have full control of their
environment. Apptainer containers can be used to package entire scientific
workflows, software and libraries, and even data. This means that you don't have
to ask your cluster admin to install anything for you - you can put it in a
Apptainer container and run.

You can use Apptainer by loading the module

::

    module load apptainer


Examples
--------

For comprehensive instructions on using Apptainer, please visit the official documentation: https://apptainer.org/docs/user/latest/


Binding the filesystem to a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When you run a container, the host file system becomes inaccessible. However, you may want to read and write files on the host system from within the container. To enable this functionality, you can 'bind' specific directories in to the container.

To bind ``/fred`` from OzSTAR to ``/fred`` in your container:

::

    apptainer run -B /fred mycontainer.sif

To bind your project directory to a specific location in your container
(In this case ``/fred/oz123`` from OzSTAR to ``/oz123`` inside the container):

::

    apptainer run -B /fred/oz123:/oz123 mycontainer.sif

By default, Apptainer also binds several other directories:
    - ``$HOME``
    - ``$PWD``
    - ``/sys``
    - ``/proc``
    - ``/dev``
    - ``/tmp``
    - ``/var/tmp``
    - ``/etc/resolv.conf``
    - ``/etc/passwd``
    - ``/etc/localtime``
    - ``/etc/hosts``

(See https://apptainer.org/docs/user/latest/bind_paths_and_mounts.html)

Using a GPU with a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are on a login node, or you have requested one or more Nvidia GPU's in
your batch job, you can access the GPU's in your container using the ``--nv``
switch. This will automatically bind the GPU's in to your container. You may
still need to have your own cuda installation in your container.

::

    apptainer run --nv mycontainer.sif


Increasing the speed of your container on OzSTAR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Depending on your workload, it is often better to request ``--tmp`` storage and
copy your image to there before you use your container. In many cases this will
provide better performance. It is important that your requested ``--tmp`` size is
bigger than your apptainer image, or ``--tmp`` will run out of space and your job
will crash.

For example, in your batch script:

::

    #!/bin/bash
    #SBATCH --tmp=10G

    cp /path/to/my/container.sif $JOBFS/container.sif

    apptainer run $JOBFS/container.sif


Building a containerised conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here we will show you how to containerise a conda environment. We will use a Docker image as our starting point (https://hub.docker.com/r/mambaorg/micromamba).

Apptainer images can be be built from plain text, 'definition' files, analogous to a ``Dockerfile``.
Consider the following apptainer definition file, ``bilby.def``:

::

    BootStrap: docker
    From: mambaorg/micromamba:1.4.6-jammy

    %post
        micromamba install -qy -n base -c conda-forge python=3.10 bilby gwpy python-lalsimulation


.. note::
    We have chosen to bootstrap specifically from the ``micromamba:1.4.6-jammy`` image, since its glibc version most closely matches OzSTAR's system glibc (see :ref:`Fakeroot feature` below).

To build the image, simply do

::

    apptainer build bibly.sif bilby.def


This will:

    - download the ``micromamba:1.4.6-jammy`` image from DockerHub
    - convert it to ``sif`` format
    - install Python v3.10, ``bilby``, and a few other python packages in to the base conda/mamba environment within the image
    - save the image to ``bilby.sif``

Now you can execute commands within your containerised conda environment. For example, if you have a python script:

::

    ./bilby.sif python my-script.py


If your python script is executable and has the shebang ``#!/usr/bin/env python``, then the command can be as simple as

::

    ./bilby.sif my-script.py


Or, if you need to add some bind mounts, you can do e.g.

::

    apptainer run -B /fred bilby.sif python my-script.py


Whatever comes after ``bilby.sif`` is the command that is executed within the container.


Running 32-bit applications inside a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OzSTAR does not provide 32-bit libraries, so if you are stuck needing to run/build a 32-bit application, using Apptainer is the best way forward.

Our suggested strategy is to start with an existing image that has a GLIBC version similar to OzSTAR, within which you then install the necessary 32-bit libraries and run/compile your 32-bit application.

For example, consider the following definition file ``32bit.def``

::

    BootStrap: docker
    From: almalinux:9

    %post
    yum update -y
    yum install -y csh gcc make flex libXmu-devel libX11-devel glibc.i686 zlib-devel.i686 libcurl-devel.i686 expat-devel.i686 readline-devel.i686
    yum clean all


Building this in to an image with ``apptainer build 32bit.sif 32bit.def`` then allows you to run/compile 32-bit applications, e.g.

::

    apptainer run -B /home,/fred 32bit.sif /path/to/my/32bit/binary


Fakeroot feature
----------------
.. note::
    Apptainer on OzSTAR uses the ``fakeroot`` command in addition to a root-mapped user namespace to allow an unprivileged user to run a container with the appearance of running as root. (See option 3 https://apptainer.org/docs/user/main/fakeroot.html).

    This is useful for avoiding errors when building containers; the combination of a root-mapped user namespace with the fakeroot command allows most package installations to work. However, the fakeroot command is bound in from the host, so if the host libc library is of a very different vintage than the corresponding container the fakeroot command can fail with errors about a missing GLIBC version.

    If that situation happens (and you insist on using a container with an incompatible GLIBC) the easiest solution is to first run a container with an operating system matching the target glibc version, install Apptainer unprivileged there, and do the build nested inside that container.
