Apptainer on OzSTAR
===================

Apptainer (formerly Singularity) enables users to have full control of their environment.
Apptainer containers can be used to package entire scientific workflows, software and libraries, and even data.
This means that you don't have to ask your cluster admin to install anything for you - you can put it in a Apptainer container and run.

You can use Apptainer by loading the module

::

    module load apptainer


Usage
--------

For comprehensive instructions on using Apptainer, please visit the official documentation: https://apptainer.org/docs/user/latest/


Building a containerised conda environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here we will show you how to containerise a conda environment. We will use a Docker image as our starting point (https://hub.docker.com/r/mambaorg/micromamba).

Apptainer images can be built from plain text, 'definition' files, analogous to a ``Dockerfile``.
Consider the following apptainer definition file, ``bilby.def``:

::

    BootStrap: docker
    From: mambaorg/micromamba:1.4.6-jammy

    %post
        micromamba install -qy -n base -c conda-forge python=3.10 bilby gwpy python-lalsimulation


.. note::
    We have chosen to bootstrap specifically from the ``micromamba:1.4.6-jammy`` image, since its glibc version most closely matches OzSTAR's system glibc (see :ref:`Fakeroot feature` below).

Then, to build the image, do

::

    apptainer build bilby.sif bilby.def


This will:

    - download the ``micromamba:1.4.6-jammy`` image from DockerHub
    - convert it to ``sif`` format
    - install Python v3.10, ``bilby``, and a few other python packages in to the base conda/mamba environment within the image
    - save the image as ``bilby.sif``

Now you can execute commands within your containerised conda environment.
For example, to run a python script:

::

    ./bilby.sif python my-script.py


If your python script is executable and has the shebang ``#!/usr/bin/env python``, then the command can be as simple as

::

    ./bilby.sif my-script.py


Or, if you need to add some bind mounts, you can do e.g.

::

    apptainer run -B /fred/oz999,/some/other/path bilby.sif python my-script.py


In all cases, whatever comes after the sif file is the command to be executed inside the container.

.. note::
    Your script needs to exist within the container in order to be executed. In this instance, since ``my-script.py`` is in the current directory, it is available to the container, but only if ``$PWD`` is successfully mounted. (See :ref:`Binding the filesystem to a container` below).

For a similar example, but instead using the official Python Docker image and ``pip``, see :ref:`Python Apptainer Example`.

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

To bind multiple paths:

::

    apptainer run -B /fred/oz123,/some/other/path mycontainer.sif

By default, Apptainer also implicitly binds several other directories:

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

.. note::
    Apptainer binds ``$PWD`` by default, which is the current working directory when you run the command. If the directory does not exist inside the container, it will be automatically created. As a result, the behaviour of the apptainer command can be different depending on where you run it from.


It is also possible to `bind in other filesystem images <https://apptainer.org/docs/user/main/bind_paths_and_mounts.html#image-mounts>`_.
For example, if you have all your data in a read-only squashfs ``data.sqfs``, you can do

::

    apptainer run -B data.sqfs:/data:image-src=/ app.sif

which will mount the ``/`` of your squashfs to ``/data`` in the container.
If the mount point ``/data`` doesn't exist, it will be created.


Using a GPU with a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have requested one or more Nvidia GPU's in your batch job, you can access the GPU's in your container using the ``--nv`` switch. This will automatically bind the GPU's in to your container. You may still need to have your own cuda installation in your container.

::

    apptainer run --nv mycontainer.sif


Increasing the speed of your container on OzSTAR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Depending on your workload, it is often better to request ``--tmp`` storage and copy your image to there before you use your container. In many cases this will provide better performance. It is important that your requested ``--tmp`` size is bigger than your apptainer image, or ``--tmp`` will run out of space and your job will crash.

For example, in your batch script:

::

    #!/bin/bash
    #SBATCH --tmp=10G

    cp /path/to/my/container.sif $JOBFS/container.sif

    apptainer run $JOBFS/container.sif


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

    apptainer run -B /fred/oz123 32bit.sif /path/to/my/32bit/binary


Fakeroot feature
----------------
.. note::
    Apptainer on OzSTAR uses the ``fakeroot`` command in addition to a root-mapped user namespace to allow an unprivileged user to run a container with the appearance of running as root. (See option 3 https://apptainer.org/docs/user/main/fakeroot.html).

    This is useful for avoiding errors when building containers; the combination of a root-mapped user namespace with the fakeroot command allows most package installations to work. However, the fakeroot command is bound in from the host, so if the host libc library is of a very different vintage than the corresponding container the fakeroot command can fail with errors about a missing GLIBC version.

    If that situation happens (and you insist on using a container with an incompatible GLIBC) the easiest solution is to first run a container with an operating system matching the target glibc version, install Apptainer unprivileged there, and do the build nested inside that container.

Sandbox mode
------------
Apptainer's `"sandbox" <https://apptainer.org/docs/user/main/quick_start.html#building-images-from-scratch>`_ mode allows you to build and run a container that is unpacked to a directory on the host system, rather than a single SIF image.
Combined with the ``--writable`` flag, it can be useful during development and testing by allowing you to iterate and make changes to your container without having to rebuild the entire container each time.

.. warning::
    However, sandbox mode **should not be used for production runs**, as it completely negates all the benefits of using Apptainer in terms of Lustre I/O.
    Once you are happy with your container, you should convert it into a SIF image and use that for your production runs.
