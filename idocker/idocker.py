# encoding=utf8
# author=spenly
# mail=i@spenly.com

import os
import sys
from csv import reader

DOCKER_TREE = {}
"""
### DOCKER_TREE DATA DEMO ###
DOCKER_TREE = {
    "c6ee99cde4ac":{
        "ids":["c6ee99cde4ac", "dbfc38646bc4"],
        "tags": ["web_app","python"]
    } 
}
"""
DELIMITER = ","
REP_NONE_TAG = "<none>"
REP_MISSING_TAG = "<missing>"
HISTORY_CONTAINER_IDS = []
CMDS = {
    "images": "docker images -a --format '{{.Repository}}%s{{.ID}}'" % DELIMITER,
    "history": "docker history %s -q",
    "tag": "docker tag %s %s",
    "ps": "docker ps -aq",
    "commit": "docker commit $(docker ps -lq -n1)",
}


def exec_cmd(cmd, delimiter=DELIMITER):
    result = os.popen(cmd)
    crd = reader(result, delimiter=delimiter)
    return crd


def build_tree(images):
    image_ids, image_reps = [], []
    for img in images:
        image_ids.append(img[1])
        image_reps.append(img[0])
    image_id = image_ids[0]
    res = exec_cmd(CMDS["history"] % image_id)
    his_ids = [r[0] for r in res if r[0] != REP_MISSING_TAG]
    his_tags = []
    for img in images:
        if img[1] in his_ids and img[1] not in his_tags and img[0] != REP_NONE_TAG:
            his_tags.append(img[0])
    DOCKER_TREE[image_id] = {"ids": his_ids, "tags": his_tags}
    todo_imgs = [img for img in images if img[1] not in his_ids]
    return todo_imgs


def get_his_container_ids():
    res = exec_cmd(CMDS["ps"])
    return [item[0] for item in res]


def idocker_init():
    global HISTORY_CONTAINER_IDS
    HISTORY_CONTAINER_IDS = get_his_container_ids()


def idocker_exit():
    # step 1: docker commit latest container changes
    res = exec_cmd(CMDS["commit"])
    print("idocker commit finish!")
    latest_image_id = res[0][0].split(":")[-1][:12]
    # # step 2: get all images tree
    images = exec_cmd(CMDS["images"])
    imgs = [img for img in images if img[1] == latest_image_id]
    while imgs:
        imgs = build_tree(imgs)
    print("idocker build tree finish!")
    # step 3: tag to the latest repository
    for rep in DOCKER_TREE:
        latest_tag = DOCKER_TREE[rep]["tags"][0]
        exec_cmd(CMDS["tag"] % (rep, latest_tag))
    print("idocker retag finish!")


def main():
    args = sys.argv
    if len(args) == 1:
        print("useage eg: idocker run -it your_imgae bash")
        print("idocker will help you to save your changes after exit")
        print("what you should do is just replace command 'docker' to 'idocker'")
        print("Just mail me any ideas：i@spenly.com")
        exit(0)
    args[0] = "docker"
    idocker_cmd = " ".join(args)
    docker_run_flag = args[1].lower() == "run"
    print("#: " + idocker_cmd)
    if docker_run_flag:
        idocker_init()
    res = os.system(idocker_cmd)
    if docker_run_flag and res == 0:
        idocker_exit()
    exit(res)
