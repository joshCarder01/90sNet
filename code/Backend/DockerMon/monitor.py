
import subprocess
import time
import requests
import json
import sys

FLASK_IP = "127.0.0.1:5000"
if len(sys.argv) > 1:
    FLASK_IP = sys.argv[1]

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
            
        }
    },
    # ["challengeset1_Baldwin_0",
    #  "challengeset1_Baldwin_1",
    #  "challengeset1_TUC_0",
    #  "challengeset1_TUC_1",
    #  "challengeset1_Manti_0",
    #  "challengeset1_Manti_1",
    #  "challengeset1_OldChem_0",
    #  "challengeset1_OldChem_1",
    #  "challengeset1_Reviechel_0",
    #  "challengeset1_Reviechel_1",
    #  "challengeset1_Zimmer_0",
    #  "challengeset1_Zimmer_1",
    #  "challengeset2_Baldwin_0",
    #  "challengeset2_Baldwin_1",
    #  "challengeset2_TUC_0",
    #  "challengeset2_TUC_1",
    #  "challengeset2_Manti_0",
    #  "challengeset2_Manti_1",
    #  "challengeset2_OldChem_0",
    #  "challengeset2_OldChem_1",
    #  "challengeset2_Reviechel_0",
    #  "challengeset2_Reviechel_1",
    #  "challengeset2_Zimmer_0",
    #  "challengeset2_Zimmer_1",]:{
    #     'dirs':[
    #         ],
    #     'files':[
    #         ],
    #     'cmds':[
    #     ],
    #     'flags':{
    #         '/score.txt':100
    #     }
    # }
}

BIG_BOY = ['challengeset1_Baldwin_0', 'challengeset1_Baldwin_1', 'challengeset1_Baldwin_2', 'challengeset1_Baldwin_3', 'challengeset1_Baldwin_4', 'challengeset1_TUC_0', 'challengeset1_TUC_1', 'challengeset1_TUC_2', 'challengeset1_TUC_3', 'challengeset1_TUC_4', 'challengeset1_Manti_0', 'challengeset1_Manti_1', 'challengeset1_Manti_2', 'challengeset1_Manti_3', 'challengeset1_Manti_4', 'challengeset1_OldChem_0', 'challengeset1_OldChem_1', 'challengeset1_OldChem_2', 'challengeset1_OldChem_3', 'challengeset1_OldChem_4', 'challengeset1_Reviechel_0', 'challengeset1_Reviechel_1', 'challengeset1_Reviechel_2', 'challengeset1_Reviechel_3', 'challengeset1_Reviechel_4', 'challengeset1_Zimmer_0', 'challengeset1_Zimmer_1', 'challengeset1_Zimmer_2', 'challengeset1_Zimmer_3', 'challengeset1_Zimmer_4',
     'challengeset2_Baldwin_0', 'challengeset2_Baldwin_1', 'challengeset2_Baldwin_2', 'challengeset2_Baldwin_3', 'challengeset2_Baldwin_4', 'challengeset2_TUC_0', 'challengeset2_TUC_1', 'challengeset2_TUC_2', 'challengeset2_TUC_3', 'challengeset2_TUC_4', 'challengeset2_Manti_0', 'challengeset2_Manti_1', 'challengeset2_Manti_2', 'challengeset2_Manti_3', 'challengeset2_Manti_4', 'challengeset2_OldChem_0', 'challengeset2_OldChem_1', 'challengeset2_OldChem_2', 'challengeset2_OldChem_3', 'challengeset2_OldChem_4', 'challengeset2_Reviechel_0', 'challengeset2_Reviechel_1', 'challengeset2_Reviechel_2', 'challengeset2_Reviechel_3', 'challengeset2_Reviechel_4', 'challengeset2_Zimmer_0', 'challengeset2_Zimmer_1', 'challengeset2_Zimmer_2', 'challengeset2_Zimmer_3', 'challengeset2_Zimmer_4']
for i in BIG_BOY:
    to_check[i] = {
        'dirs':[
            "/root",
            ],
        'files':[
            ],
        'cmds':[
        ],
        'flags':{
            '/score.txt':100
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
            if c_name not in containers:
                continue
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
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"root_dir_mod", "machine_id":cid, "time":time.time(), "description":dir_ls, "machine_name":c_name}).text
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
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"file_mod", "machine_id":cid, "time":time.time(), "description":file_content, "machine_name":c_name}).text
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
                    requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"cmd_changed_output", "machine_id":cid, "time":time.time(), "description":file_content, "machine_name":c_name}).text
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
                        requests.post("http://{}/events/add".format(FLASK_IP),headers={'Content-Type':'application/json'},json={"type":"score", "machine_id":cid, "time":time.time(), "description":"{},{}".format(potential_user, score), "machine_name":c_name}).text
                        containers[c_name]['flags'][path] = file_content
    time.sleep(1)
                    
                
        

