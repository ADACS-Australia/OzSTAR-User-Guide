# Jupyter Notebooks

Launch a Jupyter Notebook or JupyterLab server on your assigned Ngarrgu Tindebeek (NT) or OzSTAR login node and connect to it from a local web browser or VS Code.

:::{warning}
Run Jupyter notebooks on login nodes **only** for development, testing, and lightweight exploratory analysis. Submit computationally intensive or long-running work as batch jobs on compute nodes (see [Creating and Submitting Jobs](../jobs/creating-jobs.md) and [Policies](../1-getting_started/Policies.rst)).
:::

## Before you start

- Create a [Python environment](python.md) (`venv` or Conda/Mamba) with `jupyter` (and optionally `jupyterlab`) installed.
- **Connect directly to your assigned login node, not a round-robin address.** Do not use `nt.swin.edu.au` or `ozstar.swin.edu.au` for Jupyter sessions, because your SSH tunnel or VS Code session must connect to the same login node. Run `myhome` on any login node to find your assigned hostname (`<login_node>.hpc.swin.edu.au` — see [Assigning a login node with myhome](../access/ssh-access.md#assigning-a-login-node-with-myhome)):

  ```bash
  myhome
  ```

## Launch a Jupyter server

1. Connect via SSH to your assigned login node (for example, `tooarrana2.hpc.swin.edu.au`) and activate your Python environment.
2. Change to the directory containing your notebooks and start the server without opening a remote browser:

   ```bash
   cd /fred/<project>/<username>/notebooks
   jupyter notebook --no-browser
   ```

   To launch JupyterLab instead of the classic notebook interface (requires `jupyterlab` in your environment):

   ```bash
   jupyter lab --no-browser
   ```

3. Note the **port number** (default `8888`, or a higher port if `8888` is already in use) and the **authentication token** printed in your terminal. To request a specific port explicitly, pass `--port`:

   ```bash
   jupyter notebook --no-browser --port=8888
   ```

## Connect to your notebook

Choose either a local web browser (using SSH port forwarding) or VS Code (using Remote-SSH).

:::::{tab-set}

::::{tab-item} Web browser (SSH tunnel)

1. From a terminal on your local machine, forward a local port (for example, `8000`) to the port Jupyter is listening on (for example, `8888`) on your **same assigned login node**:

   ```bash
   ssh -L 8000:localhost:8888 <username>@tooarrana2.hpc.swin.edu.au
   ```

   Replace `tooarrana2.hpc.swin.edu.au` with your assigned login node from `myhome`, and replace `8888` if Jupyter started on a different port. You can run this in a second local terminal after starting Jupyter, or include `-L 8000:localhost:8888` in your initial SSH connection before launching Jupyter.

2. Open a web browser on your local machine and navigate to `http://localhost:8000` (or `http://localhost:8000/lab` for JupyterLab).
3. Enter the authentication token displayed in the Jupyter terminal output when prompted — or open `http://localhost:8000/?token=<token>` directly.

::::

::::{tab-item} VS Code (Remote-SSH)

1. Connect VS Code to the **same assigned login node** where your Jupyter server is running using the [VS Code Remote-SSH extension](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host). Manual port forwarding is not required.
2. Install the [Jupyter extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) in the **remote** SSH environment (installing it only in your local VS Code is not sufficient).
3. Open your notebook in VS Code and select the **Kernel Picker** button at the top right of the editor (or run **Notebook: Select Notebook Kernel** from the Command Palette).
4. Choose **Existing Jupyter Server**, enter the server URL shown in your terminal (for example, `http://localhost:8888`), and paste the authentication token when prompted. See the [VS Code remote Jupyter server documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server) for detailed steps.
5. Run notebook cells as usual — cells execute on your assigned login node inside the Python environment where you started the Jupyter server.

:::{note}
Some VS Code extensions, including the Jupyter extension, must be installed in the remote SSH environment rather than locally. Connecting to an **Existing Jupyter Server** (instead of launching Jupyter directly from VS Code) ensures Jupyter inherits the exact environment modules and virtual environment you loaded.
:::

::::

:::::

## Using R and Julia kernels

You can run languages other than Python in Jupyter by making additional [Jupyter kernels](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels) available to your Jupyter server.

Pre-installed modules are available for R ([`IRkernel`](https://irkernel.github.io/)) and Julia ([`IJulia`](https://github.com/JuliaLang/IJulia.jl)). Loading them configures the environment variables Jupyter needs to detect the kernels automatically.

Discover the exact module versions on your cluster before starting Jupyter:

```bash
module spider irkernel
module spider ijulia
```

Load the kernel module alongside your Python/Jupyter environment, launch the Jupyter server as above, and select the R or Julia kernel from the browser kernel selector or VS Code **Kernel Picker**.

## Next steps

- [Python and Conda](python.md) — set up `venv` or Conda/Mamba environments for notebooks.
- [Connecting via SSH](../access/ssh-access.md) — configure SSH shortcuts and connection multiplexing for your assigned login node.
- [Creating and Submitting Jobs](../jobs/creating-jobs.md) — move heavy notebook workflows to Slurm batch jobs.
