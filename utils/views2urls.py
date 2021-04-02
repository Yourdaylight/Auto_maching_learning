# -*- coding: utf-8 -*-
# @Time    :2021/4/2 17:35
# @Author  :lzh
# @File    : views2urls.py
# @Software: PyCharm


import inspect
import types
from django.urls import path
from django.conf.urls import url

def views2urls(module_name):
    """
    将views中的接口加入到urls
    :param module_name:
    :return:
    """
    modules = module_name
    view = __import__(modules, fromlist=["cc"])
    url_patterns = []

    for name, value in inspect.getmembers(view):
        if name not in ["save_clean_data", "check_clean_condition"]:
            continue
        print(name,value)
        if isinstance(value, types.FunctionType):
            url_patterns.append(path(name, value))
    return url_patterns

if __name__ == '__main__':
    print(views2urls("Engines.engine_view"))
