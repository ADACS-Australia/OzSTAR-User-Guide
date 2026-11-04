# OzSTAR User Guide and Documentation

## Local Preview

To build and preview the documentation locally:

```bash
python3 -m venv venv && source venv/bin/activate
pip install sphinx==9.1.1 sphinx_rtd_theme==3.1.0
sphinx-build -b html docs/source build/
```

## How to deploy:

* Change directory to the `/var/www/user-guide/` on the `web` VM
* Run a `git pull` on the `master` branch
* Execute `sudo docker-compose up --build -d`
* The container will automatically build the documentation to html format and serve it using nginx
* The container is listening on port 8002, which is behind an nginx reverse proxy on the host
