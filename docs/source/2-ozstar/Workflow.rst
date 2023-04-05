.. highlight:: rst

Dotfiles and workflows
======================

Dotfiles (e.g. ``.bashrc``) provide a way to customise your environment by defining environment variables and aliases. For a beginner's guide on customising your ``.bashrc`` file, see https://www.freecodecamp.org/news/bashrc-customization-guide/

It is often tempting to load modules or define environment variables used in your workflows. We strongly recommend against doing so for several reasons:

* **Dotfiles may silently break old workflows**: It may become impossible to reproduce old results by running an old job script because your dotfile has since changed. By the time you realise, many years may have passed, and the previous setup requirements may be long forgotten.
* **Complex dotfile setups often lead to conflicts between workflows**: Everybody eventually runs more than one type of job. Placing your setup in your dotfile prevents you from keeping your workflows separate.
* **Errors in your dotfiles may prevent you from logging in or transferring files**: For example, any output will prevent ``rsync`` from working. This is especially problematic when scripts in your dotfiles are shared between project members, as their changes may break your environment.

Always define your environment variables and setup in the batch script.

.. warning::
    Many of the issues that users commonly encounter result from problems with their dotfiles.
