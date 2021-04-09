# -*- coding: utf-8 -*-
# @Time    :2021/4/9 14:21
# @Author  :lzh
# @File    : logutil.py
# @Software: PyCharm

import logging
import re
from logging.handlers import TimedRotatingFileHandler


def set_log(filename, log_level=logging.ERROR):
    """
    自定义日志文件位置以及打印级别
    :param filename: 日志文件存储位置
    :param log_level: 日志级别
    :return:
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 日志信息存进文件
    log_file_handler = TimedRotatingFileHandler(filename=filename, when="S", interval=1, backupCount=7)
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(log_level)

    # 控制台信息打印
    console = logging.StreamHandler()
    console.setLevel(log_level)
    # 将上述handler加入
    logger = logging.getLogger()
    logger.addHandler(console)
    logger.addHandler(log_file_handler)
    return logger


if __name__ == '__main__':
    logg = set_log("logg",logging.ERROR)

