# -*- coding: utf-8 -*-
# @Time    :2021/4/9 17:50
# @Author  :lzh
# @File    : run_start.py
# @Software: PyCharm
# @description :前后端启动脚本
import os
import platform
import threading


class myThread(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


# 创建新线程
start_backend = "python3 manage.py runserver"
if platform.system().lower() == "linux":
    start_backend = "python manage.py runserver"
start_fronend = "cd ../AML_frontend/ && npm run dev"
thread_backend = myThread(start_backend)
thread_frontend = myThread(start_fronend)

# 开启新线程
thread_backend.start()
thread_frontend.start()
