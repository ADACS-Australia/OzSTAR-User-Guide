# OzSTAR User Guide and Documentation

## How to deploy:

* Change directory to the `/var/www/user-guide/` on the `web` VM
* Run a `git pull` on the `master` branch
* Execute `sudo docker-compose up --build -d`
* The container will automatically build the documentation to html format and serve it using nginx
* The container is listening on port 8002, which is behind an nginx reverse proxy on the host
