import requests
from smart_airdrop_claimer import base
from core.headers import headers


def check_in(token, proxies=None):
    url = "https://major.glados.app/api/user-visits/visit/"
    try:
        response = requests.post(url=url, headers=headers(token=token), proxies=proxies, timeout=20)
        return response.json().get("is_increased")
    except:
        return None


def get_task(token, task_type, proxies=None):
    url = f"https://major.glados.app/api/tasks/?is_daily={task_type}"
    try:
        response = requests.get(url=url, headers=headers(token=token), proxies=proxies, timeout=20)
        return response.json()
    except:
        return None


def do_task(token, task_id, proxies=None):
    url = "https://major.glados.app/api/tasks/"
    payload = {"task_id": task_id}
    try:
        response = requests.post(url=url, headers=headers(token=token), json=payload, proxies=proxies, timeout=20)
        return response.json().get("is_completed")
    except:
        return None


def process_check_in(token, proxies=None):
    if check_in(token=token, proxies=proxies):
        base.log(f"{base.white}Auto Check-in: {base.green}Success")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Checked in already")


def process_do_task(token, proxies=None):
    for task_type in ["true", "false"]:
        task_list = get_task(token=token, task_type=task_type, proxies=proxies)
        for task in task_list:
            task_id = task["id"]
            task_name = task["title"].replace("\n", "")
            if do_task(token=token, task_id=task_id, proxies=proxies):
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                base.log(f"{base.white}{task_name}: {base.red}Incomplete")
