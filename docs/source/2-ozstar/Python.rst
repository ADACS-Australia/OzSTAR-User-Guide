.. highlight:: rst

Using Python on a supercomputer
===============================

There are 2 ways to use Python on the OzSTAR supercomputers:

#. Python module and virtual environments (recommended for beginners)
#. conda package manager (recommended if you need a precise version of Python and packages)

.. note::

    You may also use Apptainer to manage your Python environment as part of a more complex workflow. This approach, however, is not recommended for the typical user.

.. note::

    Although the operating system provides Python at ``/usr/bin/python``, we do not recommend using it. Choosing one of the two recommended methods ensures your Python environments are managed in a sensible way.

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
    ml load python-scientific/3.10.4-foss-2022a

    # create a new python virtual environment
    python -m venv ~/foo

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


Conda
-----
`Conda <https://docs.conda.io/en/latest/>`_ is an open-source package manager typically used for (though not limited to) Python packages. It was originally developed by Anaconda Inc. to distribute their Python environment "Anaconda". It can be considered as a replacement for the pip package manager.

On the OzSTAR supercomputers, Conda can be used by loading the ``conda`` module.

.. note::
    The conda module is actually an alias for `Mamba <https://github.com/mamba-org/mamba>`_ a reimplementation of conda in C++. The interface is the same, so users will not notice any difference. ``mamba install`` benefits from considerably improved performance when installing packages, whereas ``conda install`` still uses the old (slower) solver.

You may be familiar with the Anaconda distribution of Python, which contains a specific version of Python bundled with a large set of datascience packages. In contrast, the Conda module provides only the package manager, giving you the freedom to create your own environment with the exact versions of Python and packages that you need.

See the `Conda documentation <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ for instructions on how to create and manage environments.

.. note::
    The default channel is set to ``conda-forge``. To use the channels that would normally come with conda, use

    ::

        mamba install -c defaults <package name>

    If you require an environment with the Anaconda distribution of packages (https://docs.anaconda.com/free/anaconda/)

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

For more details, see: https://conda-forge.org/docs/user/tipsandtricks.html#using-external-message-passing-interface-mpi-libraries
