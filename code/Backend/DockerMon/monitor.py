
import subprocess
import time
import requests
import json

FLASK_IP = "127.0.0.1:5000"

def docker(command):
    return subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()

# Get container name and ID -> container_info
container_info_dump = docker("ps").split("\n")
container_info = {}

for ci in container_info_dump[1:-1]:
    container_id = ci[:ci.find(" ")]
    container_name = ci[ci.rfind(" ")+1:]
    container_info[container_id] = {"name":container_name}
    #requests.post("http://{}/machines/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"machine_id":container_id, "name":container_name, "location":"None"}).text

dirs_to_check = {
    "root":"/",
}

files_to_check = {
    "welcome_file":"/hello_world.txt",
}

cmd_to_check = {
    "login_last":"last"
}

user_flag_locations = { #make sure all files here are also in files_to_check dict
    "/hello_world.txt":"100"
}



while True:
    for cid,c_info in container_info.items():
        # check each path for new files
        for dir_name, dir_path in dirs_to_check.items():
            # list of files
            dir_ls = docker("exec -it {} /bin/ls {}".format(cid, dir_path)).split()

            # if there are no prexisting files, update. elif there are new files, update and call out with new files
            if dir_name not in container_info[cid]:
                container_info[cid][dir_name] = dir_ls
            elif dir_ls != container_info[cid][dir_name]:
                dif_file = [f for f in dir_ls if f not in set(container_info[cid][dir_name])]
                print("{} {} updated with file ({})".format(cid, dir_name, ",".join(dif_file)))
                requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"root_dir_mod", "machine_id":cid, "time":time.time()}).text
                container_info[cid][dir_name] = dir_ls

        # check each file for new content
        for file_name, file_path in files_to_check.items():
            # list of files
            file_content = docker("exec -it {} /bin/cat {}".format(cid, file_path)).split("\n")

            # if there are no prexisting content, update. elif there are new content, update and call out with new content
            if file_name not in container_info[cid]:
                container_info[cid][file_name] = file_content
            elif file_content != container_info[cid][file_name]:
                dif_file = [f for f in file_content if f not in set(container_info[cid][file_name])]
                print("{} {} updated with file ({})".format(cid, file_name, ",".join(dif_file)))
                requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"file_mod", "machine_id":cid, "time":time.time()}).text

                if file_path in user_flag_locations:
                    users = json.loads(requests.get("http://{}/users".format(FLASK_IP),headers={'Content-Type':'application/json'},json={}).text)
                    users = {user['username']:user['id'] for user in users}
                    if dif_file[0].strip() in users:
                        print("User '{}' scored".format(dif_file[0].strip()))
                        t = requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"score", "machine_id":cid, "time":time.time(), "user_id":users[dif_file[0].strip()], 'description':'{},100'.format(dif_file[0].strip())}).text
                container_info[cid][file_name] = file_content

        # check each cmd for new content
        for cmd_name, cmd_path in cmd_to_check.items():
            # list of cmds
            cmd_content = docker("exec -it {} /bin/{}".format(cid, cmd_path)).split("\n")

            # if there are no prexisting content, update. elif there are new content, update and call out with new content
            if cmd_name not in container_info[cid]:
                container_info[cid][cmd_name] = cmd_content
            elif cmd_content != container_info[cid][cmd_name]:
                dif_cmd = [f for f in cmd_content if f not in set(container_info[cid][cmd_name])]
                print("{} {} updated with cmd ({})".format(cid, cmd_name, ",".join(dif_cmd)))
                requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"cmd_changed_output", "machine_id":cid, "time":time.time()}).text
                container_info[cid][cmd_name] = cmd_content

    time.sleep(1)