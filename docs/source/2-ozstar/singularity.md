Singularity on OzSTAR
=========

> Singularity enables users to have full control of their environment. Singularity containers can be used to package entire scientific workflows, software and libraries, and even data. This means that you don't have to ask your cluster admin to install anything for you - you can put it in a Singularity container and run.
>

You can use Singularity on OzSTAR by loading the singularity module

`module load singularity/latest`



Examples
---

For documentation on how to create Singularity containers, please visit the formal Singularity documentation https://sylabs.io/docs/



##### Example 1: Running a container and binding `/fred` in to your container
To bind `/fred` from OzSTAR to `/fred` in your container
`singularity run -B /fred mycontainer.simg`

To bind your project directory to a specific location in your container (In this case `/fred/oz123` from OzSTAR to `/oz123` inside the container)
`singularity run -B /fred/oz123:/oz123 mycontainer.simg`


##### Example 2: Using a GPU with a container
If you are on an OzSTAR login node, or you have requested one or more Nvidia GPU's in your batch job, you can access the GPU's in your container using the `--nv` switch. This will automatically bind the GPU's in to your container. You may still need to have your own cuda installation in your container.
`singularity run -B --nv mycontainer.simg`

### Example 3: Increasing the speed of your container on OzSTAR
In many cases frequent random IO to the `/fred` or `/home` Lustre filesystems will result in terrible performance. This is often true of frequent random IO performed in your container if the Singularity image resides on `/fred` or `/home` (Which it almost always will). Depending on your workload, it is often better to request `--tmp` storage and copy your image to there before you use your container. It is important that your requested `--tmp` size is bigger than your singularity image, or `--tmp` will run out of space and your job will crash.

Eg, in your batch script, you could do something like this:
```#!/bin/bash
#SBATCH --tmp=10G

cp /path/to/my/container.simg $JOBFS/container.simg

singularity run $JOBFS/container.simg
```