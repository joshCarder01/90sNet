# Table of Contents
- [Table of Contents](#table-of-contents)
- [Backend Installation](#backend-installation)
  - [How To Run API Server](#how-to-run-api-server)
  - [Starting up Docker Containers](#starting-up-docker-containers)
    - [Configuration](#configuration)
    - [Setting up Docker Compose](#setting-up-docker-compose)
  - [How to Run Docker Manager and Monitor](#how-to-run-docker-manager-and-monitor)
  - [Running the Automated Adversary](#running-the-automated-adversary)
- [Frontend](#frontend)
  - [Recommended Setup](#recommended-setup)
  - [Running the Frontend](#running-the-frontend)

# Backend Installation
## How To Run API Server
The flask server runs on a docker container. However, the database is setup on the host machine as a volume to be persistent across running containers.

First move the source code of the `/code/Backend` into the machine you wish to run the backend on. Run the script `./setup_flask_app.sh`, this sets up the flask app in the directory and initializes the server.

```bash
$ cd code/Backup
$ ./setup_flask_app.sh 
Building flask_app
[+] Building 39.5s (13/13) FINISHED                                                                    docker:default
 => [internal] load build definition from flask_app.dockerfile                                                   0.0s
 => => transferring dockerfile: 506B                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.11.8-slim                                            0.6s
 => [internal] load .dockerignore                                                                                0.0s
 => => transferring context: 2B                                                                                  0.0s
 => [1/8] FROM docker.io/library/python:3.11.8-slim@sha256:90f8795536170fd08236d2ceb74fe7065dbf74f738d8b84bfbf2  3.7s
...
 => [7/8] COPY Flask_App /app                                                                                    0.3s 
 => [8/8] WORKDIR /app                                                                                           0.0s 
 => exporting to image                                                                                           0.4s 
 => => exporting layers                                                                                          0.3s 
 => => writing image sha256:d059edee7b8f5ddff0f26136a95cb7a6e3bf106288c74efae4fef8662aee5ae1                     0.0s 
 => => naming to docker.io/library/flask_app:local                                                               0.0s 
Creating network "backend_default" with the default driver
Creating backend_flask_app_run ... done
```

After this you can then run `docker compose up` or `docker compose up -d`, the later sets up the server in the background. This will run the server on your system with port `5000` being exposed. All other parts of the Backend and Frontend will need your IP address to coordinate and run.

## Starting up Docker Containers

### Configuration

Move into the `code/Backend/ComposeGenerator` directory. You must have your challenge images set up. You can then begin configuring everything to function in the network. With the following options:
```yaml
image: "Image which you want to run in a service"
name: "Alternative name to have as the base of each service, useful to obfuscate the exact challenges on any machine"
proxy: "Optional, true can be put here, which will expose this container on another network to be accessed by the outside world as a proxy."
count: "How many images do you want to be spun up"
location: "A list of locations for each container to be spun up in. Set up by the system to act in the correct subnets."
other_options: "A dictionary of extra options to add to the service in Docker Compose"
```

Examples of this system is in `code/Backend/ComposeGenerator/example_conf.yaml` which is a basic implementation of this system.

### Setting up Docker Compose

After setting up your configuration you can run `code/Backend/ComposeGenerator/run.sh {path_to_config} {path_to_output_compose.yaml}`. This will set up the networks and add machines to each of the networks on its own. You can then run `docker compose up` on your desired docker machine.

## How to Run Docker Manager and Monitor
These components must be run on the same machine as the isolated container network is running on, [see here](#starting-up-docker-containers). The monitor and manager can be given the ip and port of the flask server, by default the will attempt to connect to `localhost:5000`.

Both can be run, in the directory `code/Backend/DockerMan` or `code/Backend/DockerMon` respectively run `python manager.py [<ip:port>]` or `python monitor.py [<ip:port>]`.

## Running the Automated Adversary
The automated adversary may be run on any machine but must also be given the ip and port of the flask server, it will default to `localhost:5000`.

In the directory `code/Backend/AutoAdversary` run `python adversary.py [<ip:port>]`.

# Frontend

## Recommended Setup
We recommend you use python's `venv` module to install prerequisetes for the frontend, as it is important the version of python packages are exact. You can do this by running in the `code/FrontendCore` directory:
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

Which will install the prerequisites for the frontend in a virtual environment which is isolated from your systems python packages.

## Running the Frontend
After installing prerequisets, run the frontend with the ip and port of the backend flask server, [read here](#how-to-run-api-server), the frontend defaults to checking `localhost:5000`.

Front end can be run with `python frontend.py [<ip:port>]` in the `code` directory.
