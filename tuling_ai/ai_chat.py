# -*- coding:utf-8 -*-
import sys
import json
import time
import requests


# 人机对话所用机器人为图灵机器人，每日请求总数为100，请手动去图灵官网申请自己的机器人替换配置KEY与USER_ID
Tuling_API_URL = "http://openapi.tuling123.com/openapi/api/v2"
# 替换为你的API_KEY
Tuling_API_KEY = "2ae44d01717d407daebd0d2bc3f0a7db"
# 替换为你的UserID
Tuling_USER_ID = "429262"
name = ""


class Colors:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def Ask_Tuling(msg):
    tuling_post_data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": Tuling_API_KEY,
            "userId": Tuling_USER_ID,
        },
    }
    json_data = json.dumps(tuling_post_data).encode("utf8")
    resp = requests.post(url=Tuling_API_URL, headers={"content_type": "application/json"}, data=json_data)
    if resp.status_code == 200:
        r = resp.json()
        if r:
            return r["results"][0]["values"]["text"]


def Human_AI_Mode():
    print(Colors.PINK + "艾达：Hi～我是艾达哟～" + Colors.END)
    while True:
        q = input(Colors.BLUE + name + ": " + Colors.END)
        if q == "exit":
            print("即将退出聊天...Wait a minute！")
            time.sleep(1)
            sys.exit(0)
        a = Ask_Tuling(q)
        time.sleep(1)
        word = ['Good Morning', 'Good Afternoon', 'Good Evening', 'Have a good time', 'What was dead will never die!']
        import random
        rand_num = random.randint(0, len(word)-1)
        w = word[rand_num]
        print(Colors.PINK + "艾达：{}".format(w) + Colors.END)


if __name__ == "__main__":
    print("提示：示例程序所选用的机器人每日有次数限额，可自行申请替换，具体请参考代码注释")
    time.sleep(1)
    print("提示：输入" + Colors.RED + "exit" + Colors.END + "可退出聊天")
    name = input(Colors.YELLOW + "请输入你的名字：" + Colors.END)
    if name == "":
        name = "你"
    time.sleep(1)
    print(Colors.GREEN + "正在进入呼叫傻逼..." + Colors.END)
    time.sleep(1)
    print(Colors.GREEN + "连接成功" + Colors.END)
    time.sleep(1)
    Human_AI_Mode()
