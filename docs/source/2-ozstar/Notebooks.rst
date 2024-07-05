.. highlight:: rst

Working with Jupyter Notebooks - Python
=======================================
.. note::
    You should only be running notebooks for development, testing or simple analysis purposes. All computationally intensive work should be submitted as a batch job to the cluster and be run on the compute nodes in a Python script.

If you wish you to view and work with Python notebooks on OzSTAR, you simply need to launch a Jupyter server from one of the login nodes, and then connect to it. We'll show you how to do this below with either JupyterLab via a web browser, or via VS Code.

Note that you'll need to connect to a specific login node e.g. ``user@tooarrana2.hpc.swin.edu.au``. You cannot rely on the generic ``ozstar`` or ``nt`` logins as a destination for remote persistent processes, since they are both round-robin addresses. You need to pick one of ``farnarkle1/2`` or ``tooarrana1/2`` and stick to it.

Launching a Jupyter Notebook Server
-----------------------------------
First, activate your `Python environment <../2-ozstar/Python.html>`_ that you wish to work in and ensure you have ``jupyter`` installed in it.

Then, navigate to the directory where you want to serve notebooks from, and launch a Jupyter Notebook server

::

    cd /path/to/your/notebooks
    jupyter notebook --no-browser

Take note of which port the server is running on -- it will be displayed in the terminal output, along with a token/password.
You can also specify a port directly with the ``--port`` flag e.g.

::

    jupyter notebook --no-browser --port=8888

Running your notebook
---------------------

Web Browser
^^^^^^^^^^^
To use JupyterLab in a web browser for running your notebooks, you'll need to forward the port from the login node to your local machine. You can do this with SSH port forwarding.

::

    ssh -L 8000:localhost:8888 user@tooarrana2.hpc.swin.edu.au

This command forwards port 8000 on your local machine to port 8888 on the login node.

This can be done either retroactively by opening another terminal and connecting to the same login node, or proactively in the same terminal by forwarding the port **before** you launch the Jupyter server.

Ensure that you launch the Jupyter server on the same port as you specified in the SSH command. e.g. port 8888 in this case.

Finally, open a web browser on your local machine and navigate to `<http://localhost:8000>`_ to access the Jupyter server. You will be prompted for the token/password that was displayed in the terminal. Alternatively, you can append the token to the end of the url: `<http://localhost:8000/?token=YOUR_TOKEN>`_, where you should replace ``YOUR_TOKEN`` with your token.

VS Code
^^^^^^^
To use your notebook in VS Code, you'll need connect to the login node using the `Remote-SSH extension <https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host>`_, and then connect your notebook's kernel to the Jupyter server running on the login node that you set up above.

Once again, ensure that you connect to the same login node as the one that you launched the Jupyter server on, and ensure that you have installed the `Jupyter extension <https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter>`_. You should not need to forward any ports.

.. note::
    Some VS Code extensions, such as Jupyter, need to be installed in the remote environment; it is not enough to have them installed in your local VS Code.

Next, open your notebook and select the **Kernel Picker** button on the top right-hand side of the notebook (or run the **Notebook: Select Notebook Kernel** command from the Command Palette).

You will then need to connect to an **'Existing Jupyter Server'** by entering the URL of the server (e.g. `<http://localhost:8888>`_) and the token/password that was displayed in the terminal when you launched the Jupyter server. You can find more detailed steps in the `VS Code documentation <https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server>`_.

At this point you can run your notebook as you would normally, and the cells will be executed on the login node inside the Python environment that the Jupyter server was launched from.

.. note::
    We have chosen to connect to an existing Jupyter server, rather than trying to launch the server directly from within VS Code. This is because it is difficult to get VS Code to correctly recognise your Python environment and modules. By following the steps above, you ensure that the server is running in the correct environment.
