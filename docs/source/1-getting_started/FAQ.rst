.. highlight:: rst

FAQ
============================

Who is eligible for an account on the facility?
--------------------------------------------------------

All Swinburne staff and students are eligible for accounts as are researchers in the field of astronomy and space sciences based at publicly funded institutions within Australia. International collaborators may also apply for accounts but cannot be the lead on a research project.

How do I access the facility?
------------------------------------------

Access is via SSH only into the login nodes (``nt.swin.edu.au``). For more details, see the page :doc:`../1-getting_started/Access`.

What operating system is used?
------------------------------------------

All nodes of OzSTAR are running `AlmaLinux 9 <https://almalinux.org>`_ as the main operating system. As such, we advise that you get yourself familiar with the Linux operating system and the use of command line before using the supercomputer.

How do I change my login password?
------------------------------------------

- You can change your password when you are logged on via SSH, just type ``passwd`` in the terminal. You can find more details on `passwd manual page <http://man7.org/linux/man-pages/man1/passwd.1.html>`_.

- You can reset your password from `supercomputing.swin.edu.au/account-management/new_account_request <https://supercomputing.swin.edu.au/account-management/new_account_request>`__. There is a Login/Reset Password link on the left hand pane.

How can I change my login shell?
------------------------------------------

You can change your login shell, just type ``changeShell`` in your terminal. This information will take a few minutes to propagate, and you will have to login again for it to take effect.

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

If you would like to learn more about using graphics programming units (GPUs) in your research a good starting point is the `NVIDIA Developer Zone <https://developer.nvidia.com/category/zone/cuda-zone>`_ or our `HPC/GPU webinar series <https://supercomputing.swin.edu.au/hpcgpu-webinars/>`_.

You can also look through slides on `Getting Started <http://astronomy.swin.edu.au/supercomputing/Swin_Getting_Started_with_CUDA_static.pdf>`_ with the CUDA programming language for GPUs, an introduction to the `OpenACC <http://astronomy.swin.edu.au/supercomputing/Swin_Intro_to_OpenACC_static.pdf>`_ directives for accelerating code with GPUs and the `Thrust <http://astronomy.swin.edu.au/supercomputing/thrust.pdf>`_ acceleration library.

These were all presented at a CUDA Easy workshop at Swinburne (thanks to Michael Wang, Paul Mignone, Amr Hassan and Luke Hodkinson).

Another great starting point is to go to the `GPU Technology Conference <GPU Technology Conference>`_ website and search through past presentations using their On-Demand tool. You can search by field and/or topic, for example, and most likely someone in your field has already tackled what you are hoping to do.

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

"Ngarrgu Tindebeek" means "Knowledge of the Void" in the local indigeneous language, a reflection on the astrophysical simulations run on the machine to further our knowledge of space.

The login nodes, Tooarrana, are named after a cute and furry Australian creature, which is currently endangered.

Most of the other components of the OzSTAR cluster are named in memory of the late satirist, actor, comedian, and writer `John Clarke <https://en.wikipedia.org/wiki/John_Clarke_(satirist)>`_.

OzSTAR's login nodes are farnarkle. login node cgroups are grommet. The main filesysem is Dagg mounted at Fred. Lustre servers are arkle, warble, umlaut. The majority of compute nodes are called John, with high memory nodes being Bryan. NT's compute nodes are named Dave.

Why am I getting a "permission denied" error when logging in?
-------------------------------------------------------------

If you were previously able to log in, and assuming you are using the correct password or SSH key, then most likely your account has expired. All accounts automatically expire 2 years after the creation date. Due to a current limitation in the account management system, users are not alerted prior to account expiration. If your account has expired and you would like us to renew it, or if you would like to find out your current expiry date, please contact us at hpc-support@swin.edu.au.
