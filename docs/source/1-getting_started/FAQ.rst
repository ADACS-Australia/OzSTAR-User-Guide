.. highlight:: rst

FAQ
============================

.. contents:: Table of Contents
    :depth: 2

Who is eligible for an account on the facility?
--------------------------------------------------------

All Swinburne staff and students are eligible for accounts as are researchers in the field of astronomy and space sciences based at publicly funded institutions within Australia. International collaborators may also apply for accounts but cannot be the lead on a research project.

How do I access the facility?
------------------------------------------

Access is via SSH only into the login nodes (``nt.swin.edu.au`` for NT or ``ozstar.swin.edu.au`` for OzSTAR). For more details, see the page :doc:`../1-getting_started/Access`.

What operating system is used?
------------------------------------------

All nodes of OzSTAR are running `AlmaLinux 9 <https://almalinux.org>`_ as the main operating system. As such, we advise that you get yourself familiar with the Linux operating system and the use of command line before using the supercomputer.

How do I change my login password?
------------------------------------------

- You can change your password when you are logged on via SSH, just type ``passwd`` in the terminal. You can find more details on `passwd manual page <http://man7.org/linux/man-pages/man1/passwd.1.html>`_.

- You can reset your password from `supercomputing.swin.edu.au/account-management/new_account_request <https://supercomputing.swin.edu.au/account-management/new_account_request>`__. There is a Login/Reset Password link on the left hand pane.

How can I change my login shell?
------------------------------------------

On this system, user accounts are managed via LDAP, so the standard chsh command is not available. Instead, you can change your default login shell by using the changeShell command.

To change your shell, type ``changeShell``, then follow the prompts to select your desired shell. Changes will take a few minutes to propagate, and you will need to log out and log back in for the change to take effect.

The available shells include:

* csh
* tcsh
* bash
* zsh
* ksh

How can I avoid session timeouts?
------------------------------------------

There are a few ways to do this but a simple method is to go to the .ssh directory on your laptop or desktop machine and create a file called “config” if it does not already exist. In that file, add the line:
::

    ServerAliveInterval 120

If you created that file, ensure it has the correct permissions:
::

    chmod 600 ~/.ssh/*


How can I find out more about using GPUs?
---------------------------------------------

If you would like to learn more about using graphics processing units (GPUs) in your research, a good starting point is the `GPU programming guide by ENCCS <https://enccs.github.io/gpu-programming/>`_. For NVIDIA-specific information, you can visit the `NVIDIA Developer Zone <https://developer.nvidia.com/category/zone/cuda-zone>`_.

You can also look through slides on `Getting Started <http://astronomy.swin.edu.au/supercomputing/Swin_Getting_Started_with_CUDA_static.pdf>`_ with the CUDA programming language for GPUs, an introduction to the `OpenACC <http://astronomy.swin.edu.au/supercomputing/Swin_Intro_to_OpenACC_static.pdf>`_ directives for accelerating code with GPUs and the `Thrust <http://astronomy.swin.edu.au/supercomputing/thrust.pdf>`_ acceleration library.

These were all presented at a CUDA Easy workshop at Swinburne (thanks to Michael Wang, Paul Mignone, Amr Hassan and Luke Hodkinson).

Another great starting point is to go to the `GPU Technology Conference <https://www.nvidia.com/gtc/training/>`_ website and search through past presentations using their On-Demand tool. You can search by field and/or topic, for example, and most likely someone in your field has already tackled what you are hoping to do.

Why am I getting “Disk quota exceeded” message?
-----------------------------------------------

Type the following command on any node ::

    quota

and it will highlight which of your project or home quotas you are exceeding.

Why don't some nvidia and slurm commands, or srun/sinteractive gpu jobs work from my screen session?
-------------------------------------------------------------------------------------------------------

Linux unsets ``LD_LIBRARY_PATH`` for security reasons when running setgid executables (such as ``screen``), which interferes with the pre-loaded ``slurm`` and ``nvidia`` modules. Interactive slurm jobs started from screen sessions inherit this broken environment.

The simple workaround is to run ``bash -l`` or ``tcsh -l`` in each screen window you open, or to use ``tmux`` instead.

What is the meaning behind the machine names?
---------------------------------------------

The name Ngarrgu Tindebeek was provided by Wurundjeri elders through the assistance of the Moondani Toombadool Centre at Swinburne. It translates as “Knowledge of the Void” in the local Woiwurrung language and represents the goal of harnessing the power of a supercomputer to enable researchers to explain the unknown, to push the boundaries of knowledge. Understanding black holes - how they come together within galaxies, collide and create gravitational waves - is a key use case and a prime example.

The login nodes, Tooarrana, are named after a cute and furry Australian creature, which is currently endangered.

Most of the other components of the OzSTAR cluster are named in memory of the late satirist, actor, comedian, and writer `John Clarke <https://en.wikipedia.org/wiki/John_Clarke_(satirist)>`_.

OzSTAR's login nodes are farnarkle. login node cgroups are grommet. The main filesysem is Dagg mounted at Fred. Lustre servers are arkle, warble, umlaut. The majority of compute nodes are called John, with high memory nodes being Bryan. NT's compute nodes are named Dave.

Why am I getting a "permission denied" error when logging in?
-------------------------------------------------------------

If you were previously able to log in, and assuming you are using the correct password or SSH key, then most likely your account has expired. All accounts automatically expire 2 years after the creation date. Due to a current limitation in the account management system, users are not alerted prior to account expiration. If your account has expired and you would like us to renew it, or if you would like to find out your current expiry date, please contact us at hpc-support@swin.edu.au.

Why doesn't Emacs/X11/other program work?
-----------------------------------------
*"Emacs is delicate and sensitive like a little flower, and won't work if you mess with its libs".*

See our page on `Workflows and Dotfiles <../2-ozstar/Workflow.html>`_ for more information.

Why don't the compute nodes have internet access or access to external networks?
--------------------------------------------------------------------------------

The compute nodes on our facility are dedicated exclusively to computation and data processing. By design, they are isolated from external networks to ensure reliable, uninterrupted performance. Allowing internet access would risk delays due to network issues, slow or unreliable external servers, and potentially introduce security concerns.

For workflows that require external data, we recommend transferring necessary files to your home or project directory in advance. If automated file transfers from external sources are needed, we recommend using the internet-enabled trevor nodes for these tasks. You can set up file transfers on trevor nodes as part of your workflow, then chain Slurm jobs together with dependencies to automate data movement and processing.