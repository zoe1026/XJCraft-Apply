# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


# Database
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DBNAME = "mc"
MYSQL_USER = "root"
MYSQL_PASSWD = "123456"

# 数据存放目录
DATA_FOLDER = "data"
# HTTP Port
HTTP_PORT = 5000
# HTTP 密钥
HTTP_SECRET = None  # init 中进行初始化


def init():
    """
    初始化
    """
    global DATA_FOLDER
    global HTTP_SECRET

    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)

    # 初始化 Http secret, 仅在首次运行时进行随机
    secret_file = os.path.join(DATA_FOLDER, "http.secret")
    secret = None
    if os.path.exists(secret_file):
        with open(secret_file, 'rb') as f:
            secret = f.readline()
    if not secret or len(secret.strip()) == 0:
        with open(secret_file, 'wb') as f:
            secret = os.urandom(160)
            f.write(secret)
    HTTP_SECRET = secret


init()
