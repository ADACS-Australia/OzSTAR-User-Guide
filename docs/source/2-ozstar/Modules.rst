.. highlight:: rst

Environment Modules
====================

`Environment modules <http://modules.sourceforge.net/>`_ provide a way to dynamically modify the user's environment to access required software packages. Manually managing your environment can be cumbersome, so using modules is highly recommended and is standard practice on OzSTAR.

Although you may already be familiar with environment modules from using other supercomputers, we still recommend that you take a moment to read this documentation. OzSTAR uses the `Lmod <https://lmod.readthedocs.io/en/latest/>`_ module manager, which provides additional advanced features that are not part of the standard modules package.


The structure of a module command is:
::

    module <command> [arguments]

There are many available commands. To see a list:
::

    module

To get you started, you will first need to be able to see which software packages are available. To do so, run:
::

    module spider

This will display a list of all installed software packages. To load a package:
::

    module load <package name>

This will add the paths to the binaries and libraries for that module into your environment.

Lmod also provides a convenient tool called ```ml``` (taken from `<http://lmod.readthedocs.io/en/latest/010_user.html#ml-a-convenient-tool>`_)

For those of you who can’t type the *mdoule*, *moduel*, err *module* command correctly, Lmod has a tool for you. With ``ml`` you won’t have to type the module command again. The two most common commands are ``module list`` and ``module load <something>`` and ``ml`` does both:

::

    ml

means ``module list``. And:

::

    ml foo

means ``module load foo`` while:

::

    ml -bar

means ``module unload bar``. It won’t come as a surprise that you can combine them:

::

    ml foo -bar

means ``module unload bar; module load foo``. You can do all the module commands:

::

    ml spider
    ml avail
    ml show foo

If you ever have to load a module name spider you can do:

::

    ml load spider


Hierarchical Modules
---------------------------

**OzSTAR** uses *hierarchical* modules. In summary, this means that loading a module makes more modules available by updating the module path where the module manager looks for modules. This is especially useful because it helps users avoid dependency problems and has been used on OzSTAR to avoid compiler and OpenMPI conflicts and incompatibilities.

There are 3 categories (or "levels") of modules:-

* **Core**: These are modules built using the system compiler. For example, this category includes compilers (e.g. GCC), system utilities, and programs that were installed as pre-compiled binaries.
* **Compiler**: Contrary to what the name suggests, this category does *not* contain compilers. Rather, it contains modules that have been built using a specific compiler. For example, this category contains MPI libraries (e.g. OpenMPI), and other programs that were built with a compiler (from the Core category) without dependency on an MPI library.
* **MPI**: This category contains modules built using a specific compiler and MPI combination, which will include most HPC programs.

``module avail`` will only display modules available given the currently loaded parents. "Compiler" modules will only be visible once a parent "Core" module has been loaded, and likewise, "MPI" modules will only be visible once a parent "Compiler" module has been loaded.

If a user wishes to see a list of **all** modules on OzSTAR, they should use ``module spider``. This behaviour differs from many other supercomputing clusters.

For example, consider a module for the HDF5 library. The parallel version of the HDF5 library (an MPI module) is built using a compiler (a Core module) and an MPI library (a Compiler module), for example (GCC 12.2.0) and OpenMPI 4.1.4). To see the MPI module ``hdf5/1.12.0`` via module avail, the Compiler module ``openmpi/4.1.4`` must first be loaded. But to see that OpenMPI module, the Core module ``gcc/12.2.0`` must first be loaded.

So a user who wishes to explore the available modules and load the HDF5 library would run the following commands in order:

::

    ml gcc/12.2.0
    ml openmpi/4.1.4
    ml hdf5/1.12.0

This would load the HDF5 library built using GCC 12.2.0 and OpenMPI 4.1.4. If they had instead loaded a different version of GCC or OpenMPI, then the final command would load the version of HDF5 built using those versions of the compiler and MPI instead (assuming it is installed).

Loading a module always requires the use of a version identifier - there are no default modules. This is designed to prevent user workflows from unintentionally changing or breaking if the default version changes. The user should always be aware of which version they are loading. Attempting to load a module without a version identifier will instead display a list of available versions of that module.

If a particular module is only available via one combination of Compiler/MPI in the module hierarchy, then loading that module will also automatically load the parent modules if they have not already been loaded.

If a particular module has multiple parent hierarchies, then loading that module without loading a choice of parents will instead display a list of available parent modules.

Toolchains
---------------------------

A toolchain is a set of compilers, MPI libraries, and other libraries used to build software. Rather than building each individual module with individually chosen build dependencies, common toolchains are used to standardise modules and ensure compatibility.

Loading a toolchain loads all of its components. From a user's perspective, toolchains can be considered as a shortcut for loading a set of module dependencies.

OzSTAR provides some of the ``foss`` and ``intel`` toolchains as specified by the `EasyBuild build system <https://easybuild.io>`_:

Currently, the available toolchains are

* ``foss/2022b``
* ``intel/2022b``

For example, ``foss/2022b`` provides GCC 12.2.0 and OpenMPI 4.1.4. To see the full list of components in each toolchain, refer to `<https://docs.easybuild.io/common-toolchains/#common_toolchains_overview>`_.
