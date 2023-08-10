.. highlight:: rst

Accounts
========

Overview
--------

Accounts are available free of charge to Swinburne staff and students, and anyone working in the field of astronomy and space sciences and based at a publicly funded research institution within Australia. Every account must be linked to at least one project, whether that be a general access project that defines a research group or a project approved through a merit allocation scheme. International collaborators on approved projects may also apply for accounts but cannot be the lead on a research project.

Manage your account
--------------------

If you already have an account and would like to update your contact details, reset your password, etc. you can go directly to the account management portal (`supercomputing.swin.edu.au/account-management <https://supercomputing.swin.edu.au/account-management/>`_). Please note that OzSTAR accounts are completely separate to Swinburne logins.

Getting a new account
-----------------------------------

.. image:: ../_static/g2-Account.png

- Step 1:
    * Fill in the form on https://supercomputing.swin.edu.au/account-management/new_account_request with your details.
- Step 2:
    * The system will send you an email to verify your email address. Please check your spam folder.

.. note::
    In the majority of cases where the verification email has not arrived, it is because it has been caught by the spam filter, or the email address has been entered incorrectly.

- Step 3:
    * Your account request will be sent to our admin team for approval. This may take up to 48 hours. You will not be able to login to the account-management system until your account has been approved.
- Step 4:
    * If our admin team approves your account, the system will send you an email with your username.

Projects
-------------

The standard approach to utilising the facility is to apply for an account and then compete for time through the general access job queue. However, your account needs to be linked to a project. This is for management, reporting and file system quota purposes. In general, a project can be thought of as defining a research group or department. For example, the leader of a research group would setup a project for that group at the same time as applying for an account. Students and postdocs within that group, when applying for an account, would then join that project. This will be set as the default project for that person. In practice, when logging in and submitting jobs to the general access job queue, the fact that your account is linked to a project will not have any bearing on the way that you operate. However, your allocation of disk space on the Lustre file system will be considered by project, i.e. research group.

.. note::
    Students cannot be the leader of a project. If you are a student and required a new project, please ask your supervisor to create a project, which you can join.

The other type of projects are those created for proposals that are granted time on the facility through a merit allocation scheme (MAS). For MAS projects a set number of resource credits are assigned (generally in terms of CPU walltime). These credits are utilised by submitting jobs to the queue but it is important that when doing this the group id is set to that of the MAS project and the MAS project is designated in the job submission script (see the Job Queue page).

Note that an account can be linked to more than one project, e.g. a default research group project and a MAS project.

.. image:: ../_static/g2-project-3.png

Create New Project
^^^^^^^^^^^^^^^^^^^^^^
- Step 1: submit a new project request via the account-management system.
- Step 2: your project request will be sent to our admin team for approval. The apporval process may take up to 48 hours.
- Step 3: you will receive an email when your project is created. You will find a new project space created on ``/fred/your-project-id``

Join Existing Project
^^^^^^^^^^^^^^^^^^^^^^
- Step 1: submit a project join request via the account-management system.
- Step 2: your request will be sent to the project leader for approval. Please contact the project leader before submitting a project join request.
- Step 3: you will receive an email when your request is approved. The system will automatically add you to the group associated with this project. This will give you access to the project directory and quota.
