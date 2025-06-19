.. highlight:: rst

Using Python on a supercomputer
===============================

There are 3 ways to use Python on the OzSTAR supercomputers:

#. Python module and virtual environments (recommended for beginners)
#. conda package manager (recommended if you need a precise version of Python and packages)
#. In a container using Apptainer (recommended for optimising Lustre I/O)

.. note::

    Although the operating system provides Python at ``/usr/bin/python``, we do not recommend using it. Choosing one of the three recommended methods ensures your Python environments are managed in a sensible way.

Python modules
--------------
The modules system provides several versions of Python. These can be examined by:

::

    module spider python

The ``-bare`` versions provide a minimal installation of Python, while the standard versions include commonly used packages. Calling ``module spider`` on a specific version, e.g.

::

    module spider python/3.10.4

will show all of the included packages and their version numbers.

If you need to install additional packages, you may do so using the ``pip`` package manager. To do so, you must first `create a virtual environment <https://docs.python.org/3/library/venv.html>`_, since users do not have write permissions to the central Python installation, unlike on a personal computer. A virtual environment can be created and then activated by:

::

    python -m venv /path/to/new/virtual/environment
    source /path/to/new/virtual/environment/bin/activate

Once you are in a virtual environment, you can use ``pip`` to install packages.

.. note::
    By default, users cannot install packages outside of a virtual environment (i.e. into their ``~/.local`` directory). Installations into ``~/.local`` can be enabled by setting the environment variable ``PIP_REQUIRE_VIRTUALENV=false``. This is very likely to lead to conflicts between your environments, and we do not provide support for such usage.

Example
^^^^^^^
Here is a step-by-step example on NT. In this example, we create a virtual environment called ``foo``, where we want to use the SciPy library. The SciPy library is provided by the ``python-scientific/3.10.4-foss-2022a`` toolchain (the inclusion of SciPy can be verified using ``ml spider python-scientific/3.10.4-foss-2022a``). We install an additional Python package (the fictional ``my_extra_package``).

::

    # load python modules
    ml python-scientific/3.10.4-foss-2022a

    # see what modules are loaded
    module list

    # create a new python virtual environment
    python -m venv --system-site-packages ~/foo

    # activate the venv
    . ~/foo/bin/activate

    # you now see a (foo) prompt indicating you are in a venv

    # install your extras into the venv
    pip install my_extra_package

    # start IPython (which is provided by the toolchain)
    ipython

    # you now see a In [1]: prompt indicating you are in IPython
    import scipy
    import my_extra_package

    # do your prototyping work here. ie. write python commands.

    # use ^D to exit IPython

    # you may also run your short python scripts
    python my_script.py

    # deactivate the venv with
    deactivate

When you logout from the node and login again, and want to use this venv again then you must first load all the modules above, and then just

::

    . ~/foo/bin/activate
    ipython

.. note::
    You must load all of the required modules before activating your Python virtual environment.

    Also note that we used the option ``--system-site-packages`` when creating the venv. This guarantees that any dependencies of module-loaded python packages are still accessible from inside the environment.
    If you are not using any module-loaded python packages on top of your venv, then it is safe to omit this option.


Conda
-----
`Conda <https://docs.conda.io/en/latest/>`_ is an open-source package manager typically used for (though not limited to) Python packages. It was originally developed by Anaconda Inc. to distribute their Python environment "Anaconda". It can be considered as a replacement for the pip package manager.

On the OzSTAR supercomputers, Conda can be used by loading the ``conda`` module.

.. note::
    The conda module is actually an alias for `Mamba <https://github.com/mamba-org/mamba>`_ a reimplementation of conda in C++. The interface is the same, so users will not notice any difference. ``mamba install`` benefits from considerably improved performance when installing packages, whereas ``conda install`` still uses the old (slower) solver.

    You may have also heard of Miniconda, Miniforge, Mambaforge and Micromamba. You can find a quick summary of the differences here:
    `"What’s the difference between Anaconda, conda, Miniconda, mamba, Mambaforge, micromamba?" <https://bioconda.github.io/faqs.html#what-s-the-difference-between-anaconda-conda-miniconda-mamba-mambaforge-micromamba>`_, but from a user perspective they can all be considered "the same".

See the `Conda documentation <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ for instructions on how to create and manage environments.

.. note::
    The default channel is set to `conda-forge <https://conda-forge.org/docs/user/introduction/>`_. To use the channels that would normally come with conda, use

    ::

        mamba install -c defaults <package name>

    If you require an environment with the `Anaconda <https://docs.anaconda.com/free/anaconda/>`_ distribution of packages

    ::

        mamba install -c defaults anaconda

Conda and home directory quota
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Conda places environments in the home directory in ``~/.conda``. As you create new environments, the home directory disk quota will be exhausted very quickly. To resolve this issue, we recommend changing where conda environments are created::

    conda config --env --prepend envs_dirs /path/to/my/project/on/fred/.conda/envs
    conda config --env --prepend pkgs_dirs /path/to/my/project/on/fred/.conda/pkgs

Alternatively, you can move your ``.conda`` directory into your project storage and then create a symlink from there, so that Conda still "sees" it in the home directory:

::

    mv ~/.conda /fred/oz000/username/.conda
    ln -s /fred/oz000/username/.conda ~/.conda

.. note::
    The backups for the home directory does not follow symlinks, so your ``.conda`` directory will no longer be backed up. To create a "backup" of the environment, you can export a YAML file specifying all the packages and versions in the environment:

    ::

        conda env export > environment.yml

    This YAML file can be stored in the home directory. To re-create the environment:

    ::

        conda env create -f environment.yml

Using MPI libraries
^^^^^^^^^^^^^^^^^^^
The MPI libraries provided by the module system are optimised for high performance on the OzSTAR and NT hardware. Packages from conda with MPI dependencies will install MPI binaries built by conda-forge. This may run with reduced performance, or not work at all. This can be solved by installing a "dummy" MPI library on conda so that the target package links with the system's MPI library, while dependencies are still resolved correctly:

::

    conda install "openmpi=x.y.z=external_*"

For more details, see:

- https://conda-forge.org/docs/user/tipsandtricks.html#using-external-message-passing-interface-mpi-libraries
- https://mpi4py.readthedocs.io/en/stable/install.html#using-conda


Using CUDA/GPU enabled packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some packages that are CUDA enabled (e.g. TensorFlow) will only install the CUDA/GPU enabled version if conda detects a display driver. This is controlled by the ``__cuda`` `virtual package <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html>`_, which corresponds to the maximum version of CUDA supported by the display driver.
You can list what virtual packages are detected by conda with:

::

    conda info

The NT login nodes ``tooarrana1/2``, unlike the old ``farnarkle1/2`` login nodes, do not have GPUs so there is no display driver detected. In order to install the CUDA/GPU enabled version of a package, you can either build your environment on one of the ``farnarkle`` login nodes, or you can override the virtual package manually using the ``CONDA_OVERRIDE_CUDA`` environment variable. You should set this to the maximum version of CUDA supported by the display driver, which you can determine by running ``nvidia-smi`` on a GPU node.

As of writing, the maximum version of CUDA supported by the display driver is 12.4.

::

    $ nvidia-smi
    Thu Oct 10 11:59:17 2024
    +-----------------------------------------------------------------------------------------+
    | NVIDIA-SMI 550.90.07              Driver Version: 550.90.07      CUDA Version: 12.4     |
    |-----------------------------------------+------------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
    |                                         |                        |               MIG M. |
    |=========================================+========================+======================|
    |   0  Tesla P100-PCIE-12GB           On  |   00000000:D8:00.0 Off |                    0 |
    | N/A   39C    P0             29W /  250W |     603MiB /  12288MiB |      0%      Default |
    |                                         |                        |                  N/A |
    +-----------------------------------------+------------------------+----------------------+

So, to install the CUDA/GPU enabled version of e.g. TensorFlow on ``tooarrana1/2`` you would run:

::

    CONDA_OVERRIDE_CUDA=12.4 mamba install tensorflow

Fore more information, see:

- https://conda-forge.org/docs/user/tipsandtricks/#installing-cuda-enabled-packages-like-tensorflow-and-pytorch
- https://conda-forge.org/blog/2021/11/03/tensorflow-gpu/#installation

Apptainer
---------
.. note::

    See the :doc:`Apptainer` page for getting started with Apptainer.

In the context of Python environments, Apptainer has two main benefits:

#. Ensuring reproducibility and portability across different systems
#. :doc:`../1-getting_started/Optimising-Lustre`

Large, complex Python environments on Lustre can often be slow to load/create and, at worst, may even cause a loss of filesystem performance for ALL users on the cluster. You can mitigate this by containerising your Python environment. This way, the Lustre filesystem sees only a single large file (your container, which is just a read-only `SquashFS <https://docs.kernel.org/filesystems/squashfs.html>`_), even though underneath you may be dealing with a large number of small files.


Python Apptainer Example
^^^^^^^^^^^^^^^^^^^^^^^^
A simple definition file ``my_container.def`` might look like this:

::

    BootStrap: docker
    From: python:3.12.7-bookworm

    %post
        pip install wheel tensorflow[and-cuda] tensorflow-datasets pandas

This uses the official Python 3.12.7 image from DockerHub as a base, into which it installs the TensorFlow library with CUDA support, and a few other packages, using pip.

To build the container image ``my_container.sif`` from the definition file, run:

::

    apptainer build my_container.sif my_container.def

Then you can run a TensorFlow script using the Python environment within the container:

::

    apptainer run --nv my_container.sif python my_tensorflow_script.py

Note that ``my_tensorflow_script.py`` does not exist in the container, but is assumed to be in the current directory, which is automatically mounted. We specify the ``--nv`` flag to enable GPU support in the container.

For a similar example, but instead using Micromamba in the container, see :ref:`Building a containerised conda environment`.

.. note::
    Remember, the ``.sif`` container is an immutable SquashFS (i.e. **read-only**).
    Once you have built your containerised environment, you cannot modify it -- you must rebuild it to make changes.

.. warning::
    **You may be fooled into thinking that you can write to your container**.
    For example, the following command may return without error ``apptainer run my_container.sif pip install xyz``.

    However, looking at the output carefully you will notice the following warning: *"Defaulting to user installation because normal site-packages is not writeable"*.

    In this case, the ``xyz`` package was installed into your ``~/.local``, and not into the container.
    Note that this is in **your actual home directory** on the host, since it is implictly bind mounted at runtime (but not at build time).

    **This is a trap for the unwary and will almost certainly lead to confusion and conflicts. Avoid it at all costs.**
