# -*- coding: utf-8 -*-
# @Time    :2021/4/9 17:50
# @Author  :lzh
# @File    : run_start.py
# @Software: PyCharm
# @description :前后端启动脚本
import os
import platform
import sys
import threading


class myThread(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


# 创建新线程
start_backend = "python manage.py runserver"
if platform.system().lower() == "linux":
    start_backend = "python3 manage.py runserver"

# 前端打包后运行
# 带参数，则打包静态资源部署到compressedAML/public目录下
BASE_PATH = os.getcwd()
STATIC_PATH = os.path.join(BASE_PATH, "..", "compressedAML")
FRONTEND_PATH = os.path.join(BASE_PATH, "..", "AML_frontend")

if not os.path.exists(STATIC_PATH):
    os.system("cd .. && npm install express-generator -g && express compressedAML && cd compressedAML && npm install ")

start_fronend = "cd {} && npm run dev".format(FRONTEND_PATH)
# dist参数执行打包好后的静态文件
if len(sys.argv) > 1 and sys.argv[1] == "dist":
    start_fronend = "cd {} && npm start".format(STATIC_PATH)
# build 执行打包命令
elif len(sys.argv) > 1 and sys.argv[1] == "build":
    os.system("cd {} and npm run build".format(FRONTEND_PATH))
    # 打包后的静态文件移到到
    os.system("mv {} {}".format(os.path.join(FRONTEND_PATH, "dist", "*"), os.path.join(STATIC_PATH,"public")))
    start_fronend = "cd {} && npm start".format(STATIC_PATH)

thread_backend = myThread(start_backend)
thread_frontend = myThread(start_fronend)

# 开启新线程
thread_backend.start()
thread_frontend.start()
# pipreqs. / --encoding = utf - 8