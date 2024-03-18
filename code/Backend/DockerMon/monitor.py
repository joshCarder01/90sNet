
import subprocess
import time

def docker(command):
    return subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()

# Get container name and ID -> container_info
container_info_dump = docker("ps").split("\n")
container_info = {}

for ci in container_info_dump[1:-1]:
    container_id = ci[:ci.find(" ")]
    container_name = ci[ci.rfind(" ")+1:]
    container_info[container_id] = {"name":container_name}

dirs_to_check = {
    "root":"/",
}

while True:
    for cid,c_info in container_info.items():
        for dir_name, dir_path in dirs_to_check.items():
            dir_ls = docker("exec -it {} /bin/ls {}".format(cid, dir_path))
            if dir_name not in container_info[cid]:
                container_info[cid][dir_name] = dir_ls
            elif dir_ls != container_info[cid][dir_name]:
                print("{} {} updated".format(cid, dir_name))
                container_info[cid][dir_name] = dir_ls
    time.sleep(1)