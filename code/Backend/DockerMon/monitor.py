
import subprocess
import time
import requests
import json

FLASK_IP = "127.0.0.1:5000"

def docker(command):
    return subprocess.Popen(['docker']+command.split(" "), stdout=subprocess.PIPE).stdout.read().decode()

container_info_dump = docker("ps").split("\n")
containers = {}
for ci in container_info_dump[1:-1]:
    container_id = ci[:ci.find(" ")]
    container_name = ci[ci.rfind(" ")+1:]
    containers[container_name] = {'id':container_id, 'dirs':{}, 'files':{}, 'cmds':{}, 'flags':{}}

to_check = {
    "ALL":{
        'dirs':[
            "/",
            ],
        'files':[
            '/hello_world.txt',
            ],
        'cmds':[
            'last',
        ],
        'flags':{
            'hello_world.txt':100
        }
    },
    "proxy":{
        'dirs':[
            ],
        'files':[
            ],
        'cmds':[
        ],
        'flags':{
            'hello_world2.txt':100
        }
    }
}

while True:
    # for each entry in to_check
    for c_names, checks in to_check.items():
        # get names
        if c_names == "ALL":
            c_names = list(containers.keys())
        elif type(c_names) is not list:
            c_names = [c_names]
        
        # for each container in check
        for c_name in c_names:
            cid = containers[c_name]['id']

            #check dirs
            for path in checks['dirs']:
                # get dirs
                dir_ls = docker("exec -it {} /bin/ls {}".format(cid, path))
                # check to see if this has been seen before, if not, add
                if path not in containers[c_name]['dirs']:
                    containers[c_name]['dirs'][path] = dir_ls
                # if new info, print, push, and add data
                elif containers[c_name]['dirs'][path] != dir_ls:
                    print("{} {} updated with ({})".format(c_name, path, dir_ls))
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"root_dir_mod", "machine_id":cid, "time":time.time()}).text
                    containers[c_name]['dirs'][path] = dir_ls

            #check files
            for path in checks['files']:
                # get files
                file_content = docker("exec -it {} /bin/cat {}".format(cid, path))
                # check to see if this has been seen before, if not, add
                if path not in containers[c_name]['files']:
                    containers[c_name]['files'][path] = file_content
                # if new info, print, push, and add data
                elif containers[c_name]['files'][path] != file_content:
                    print("{} {} updated with ({})".format(c_name, path, file_content))
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"file_mod", "machine_id":cid, "time":time.time()}).text
                    containers[c_name]['files'][path] = file_content

            #check cmds
            for path in checks['cmds']:
                # get cmds
                file_content = docker("exec -it {} /bin/{}".format(cid, path))
                # check to see if this has been seen before, if not, add
                if path not in containers[c_name]['cmds']:
                    containers[c_name]['cmds'][path] = file_content
                # if new info, print, push, and add data
                elif containers[c_name]['cmds'][path] != file_content:
                    print("{} {} updated with ({})".format(c_name, path, file_content))
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"cmd_changed_output", "machine_id":cid, "time":time.time()}).text
                    containers[c_name]['cmds'][path] = file_content

            #check flags
            for path,score in checks['flags'].items():
                # get flags
                file_content = docker("exec -it {} /bin/cat {}".format(cid, path))
                # check to see if this has been seen before, if not, add
                if path not in containers[c_name]['flags']:
                    containers[c_name]['flags'][path] = file_content


                # if new info, print, push, and add data
                elif containers[c_name]['flags'][path] != file_content:
                    #get list of active users
                    users = json.loads(requests.get("http://{}/users".format(FLASK_IP),headers={'Content-Type':'application/json'},json={}).text)
                    users = {user['username']:user['id'] for user in users}
                    potential_user = file_content.strip()
                    if potential_user in users:
                        print("{} scored {}".format(potential_user, score))
                        requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"score", "machine_id":cid, "time":time.time(), "description":"{},{}".format(potential_user, score)}).text
                        containers[c_name]['flags'][path] = file_content
                    
                
        

        







'''
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
'''