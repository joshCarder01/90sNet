How to boot 90sNet (Order of operations)

1. Flask Server @ `./Backend`, run `setup_flash_app.sh` and `docker-compose up`
X 2. Container Network `./backend_network.sh`
3. Monitor @ `./Backend/DockerMon/`, run `python3 monitor.py <FLASK_IP:PORT>`
4. Manager @ `./Backend/DockerMan/`, run `python3 manager.py <FLASK_IP:PORT>`
5. Automated Adversary @ `./Backend/AutoAversary`, run `python3 adversary.py <FLASK_IP:PORT>`
6. Frontend run `python3 frontend.py`