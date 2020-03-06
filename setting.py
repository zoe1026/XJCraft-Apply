# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


# 数据存放目录
DATA_FOLDER = "data"
# HTTP Port
HTTP_PORT = 5000


def init():
    """
    初始化
    """
    global DATA_FOLDER

    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)


init()
