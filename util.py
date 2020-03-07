#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
import time
from flask import request, session
import functools
import re


def start_new_daemon_thread(target, name: str):
    thread: Thread = Thread(target=target, name=name)
    thread.setDaemon(True)
    thread.start()


def timestamp() -> int:
    return int(round(time.time() * 1000))


def get_ip(header_name: str) -> str:
    """
    获取远端 IP，会优先考虑 header 中携带的 IP
    :param header_name: 用于存储远端 IP 的 header，用于在反代之后获取 IP
    :return: 获取到的 IP
    """
    header: str = request.headers.get(header_name)
    if header:
        header = header.lower()

        start_idx = 0

        while True:
            end_idx = header.find(",", start_idx)
            if end_idx < 0:
                end_idx = len(header)

            curr_ip = header[start_idx:end_idx]
            if not curr_ip.find("unknown"):
                return curr_ip
            else:
                start_idx = end_idx + 1

            if start_idx >= len(header):
                break

    return get_real_ip()


def get_real_ip() -> str:
    """获取远端的真实 IP"""
    return request.remote_addr


def fail(msg: str, code: int = -1) -> dict:
    return {
        "message": msg,
        "code": code,
        "data": None
    }


def success(data=None, code: int = 0) -> dict:
    return {
        "message": None,
        "code": code,
        "data": data
    }


def pager_data(page: int, total_count: int, data: list, page_size: int = 10) -> dict:
    return {
        "page": page,
        "totalRow": total_count,
        "list": data,
        "pageSize": page_size
    }


# ===== valid =====


class ValidException(Exception):
    pass


def valid_json(name: str, valid_list):
    """
    Flask 中，如果请求以 JSON 提交，则可以用此方法来校验参数
    :param name: 参数名
    :param valid_list: 校验方法列表
    """
    if type(valid_list) is not list:
        valid_list = [valid_list]

    def valid_json0(fn):
        @functools.wraps(fn)
        def wrap(*args, **kw):
            for valid in valid_list:
                if not valid(request.get_json(), name):
                    raise ValidException("%s valid failed." % name)
            return fn(*args, **kw)
        return wrap
    return valid_json0


def valid_not_blank(json, name: str):
    """
    校验输入不为空(空白字符会被视为空)
    :param json: 输入内容
    :param name: 参数名
    :return: 输入内容不为空
    """
    return name in json and len(str(json[name]).strip()) != 0


def valid_regexp(regexp):
    """
    用正则表达式校验输入
    :param regexp: 正则表达式
    :return: 用于校验的函数
    """
    if type(regexp) == str:
        reg = re.compile(regexp)
    else:
        reg = regexp

    def valid_regexp0(json, name: str):
        """
        用正则表达式校验输入
        :param json: 输入内容
        :param name: 参数名
        :return: 输入内容能否通过校验
        """
        return name not in json or reg.match(str(json[name]))
    return valid_regexp0


# ===== login =====


class RequireAuthException(Exception):
    pass


def auth(fn):
    """
    要求登录才可以访问的接口
    """
    def wrap(*args, **kw):
        # TODO Session 无效？
        if "username" in session:
            return fn(*args, **kw)
        else:
            raise RequireAuthException()
    return wrap
