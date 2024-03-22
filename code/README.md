How to boot 90sNet (Order of operations)

1. Flask Server `./Backend/setup_flash_app.sh` (also docker-compose up)
2. Container Network `./backend_network.sh`
3. Monitor `./Backend/DockerMon/monitor.py`
4. Manager `./Backend/DockerMan/manager.py`
5. Frontend `./frontend.py`