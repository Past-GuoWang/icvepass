#app.py
import json
import sys
import time

import requests
from prettytable import PrettyTable

import watch


# 全局变量区
userName = ""
password = ""

'''
控制台日志输出脚本
'''


def out(text):
    print(time.strftime(f"[%Y-%m-%d %H:%M:%S]:{text}", time.localtime()))


'''
登陆并返回token
'''


def login():
    payload = {
        "userName": userName,
        "password": password,
        "type": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    token = json.loads(
        requests.request("POST", "https://sso.icve.com.cn/data/userLogin", json=payload, headers=headers).text)
    if token["msg"] == "ok":
        out("恭喜登陆成功！")
        global oktoken
        oktoken = token["data"]
    else:
        out("登陆失败！")
        sys.exit()
    out("开始尝试登陆！")
    payload = f'token={token["data"]}'
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    info = json.loads(
        requests.request("POST", "https://user.icve.com.cn/patch/zhzj/api_getUserInfo.action", headers=headers,
                         params=payload).text)
    if "成功" in info['errorMsg']:
        out("个人信息获取成功")
        table = PrettyTable(["姓名", "学号", "城市", "学校"])
        table.add_row([info['data']['displayName'], info['data']['employeeNumber'], info['data']['province'],
                       info['data']["schoolName"]])
        print(table)
    out("开始获取课程信息！")
    url = "https://user.icve.com.cn/learning/u/userDefinedSql/getBySqlCode.json"

    payload = "data=info&page.searchItem.queryId=getStuCourseInfoById&page.searchItem.keyname=&page.curPage=1&page.pageSize=500"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"token={oktoken};",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    info = json.loads(requests.request("POST", url, data=payload, headers=headers).text)

    classok = []
    k = 0
    table = PrettyTable(["编号", "课程名", "任课教师", "课程ID"])
    for i in info["page"]["items"][0]['info']:
        classok.append([i["ext1"], i["ext4"], i["ext9"]])
        table.add_row([k, i["ext1"], i["ext4"], i["ext9"]])
        k = k + 1
    print(table)
    watch.Watch(userName, password, classok[int(input("请选择您要执行的课程编号"))][2])


if __name__ == '__main__':
    login()
