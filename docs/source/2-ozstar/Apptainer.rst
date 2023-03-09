Apptainer on OzSTAR
===================

Apptainer (formerly Singularity) enables users to have full control of their
environment. Apptainer containers can be used to package entire scientific
workflows, software and libraries, and even data. This means that you don't have
to ask your cluster admin to install anything for you - you can put it in a
Apptainer container and run.

You can use Apptainer by loading the module

`module load apptainer/latest`


Examples
--------

For documentation on how to create Apptainer containers, please visit the
official documentation: https://apptainer.org/docs/user/latest/


Binding the filesystem to a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To bind `/fred` from OzSTAR to `/fred` in your container:

::

    apptainer run -B /fred mycontainer.simg

To bind your project directory to a specific location in your container
(In this case ``/fred/oz123`` from OzSTAR to ``/oz123`` inside the container):

::

    apptainer run -B /fred/oz123:/oz123 mycontainer.simg


Using a GPU with a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are on a login node, or you have requested one or more Nvidia GPU's in
your batch job, you can access the GPU's in your container using the ``--nv``
switch. This will automatically bind the GPU's in to your container. You may
still need to have your own cuda installation in your container.

::

    apptainer run --nv mycontainer.simg


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

    cp /path/to/my/container.simg $JOBFS/container.simg

    apptainer run $JOBFS/container.simg
