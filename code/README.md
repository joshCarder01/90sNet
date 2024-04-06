How to boot 90sNet (Order of operations)

1. Flask Server @ `./Backend`, run `setup_flash_app.sh` and `docker-compose up flask_app`
2. Set up Containers:
   1. Build containers @ `./Backend` run `./build_containers.sh`
   2. If needed for python files run @ `./Backend/ComposeGenerator` `python -m venv .venv` && `source .venv/bin/activate` && `pip install -r requirements.txt`
   3. Setup Compose @ `./Backend/ComposeGenerator` run `./run.sh total_conf.yaml compose.yaml` in `venv`
   4. Run Containers @ `./Backend/ComposeGenerator` run `docker compose up`
3. Monitor @ `./Backend/DockerMon/`, run `python3 monitor.py <FLASK_IP:PORT>`
4. Manager @ `./Backend/DockerMan/`, run `python3 manager.py <FLASK_IP:PORT>`
5. Automated Adversary @ `./Backend/AutoAversary`, run `python3 adversary.py <FLASK_IP:PORT>`
6. Frontend run `python3 frontend.py`