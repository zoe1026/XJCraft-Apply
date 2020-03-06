# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from sqlite3 import Cursor

from flask import Flask, session, request
from db import transactional
from util import valid_json, valid_not_blank, valid_regexp, get_ip, auth
import worker
import setting
import os
import logging
import time
from enum import Enum, unique


app = Flask(__name__)
app.secret_key = setting.HTTP_SECRET


@unique
class ApplyType(Enum):
    QQLevel = 1  # QQ 等级过太阳
    Invite = 2   # 老玩家邀请
    PYJY = 3     # OP Py 交易


@unique
class ApplyStatus(Enum):
    NEW = 1      # 待审核
    ACCEPT = 2   # 已通过
    DENY = 3     # 已拒绝


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


@app.route("/api/login/login", methods=["POST"])
@valid_json("username", [valid_not_blank, valid_regexp(r"[a-zA-Z0-9_]{3,16}")])
@valid_json("password", [valid_not_blank, valid_regexp(r"[a-zA-Z0-9]{6,50}")])
@transactional
def login(cur: Cursor = None) -> dict:
    """
    OP 登录
    """
    json_data = request.get_json()

    cur.execute("""
      SELECT
        username
      FROM apply_op
      WHERE username = ?
      AND password = ?
    """, (json_data["username"], json_data["password"]))
    username = cur.fetchone()
    if not username:
        return fail("用户名或密码错误")
    else:
        session["username"] = username[0]
        return success()


@auth
@app.route("/api/login/logout", methods=["POST"])
def logout() -> dict:
    session.pop("username", None)
    return success()


@auth
@app.route("/api/user/info", methods=["POST"])
def logout() -> dict:
    return success(session["username"])


@app.route("/api/player/req", methods=["POST"])
@valid_json("playerName", [valid_not_blank, valid_regexp(r"[a-zA-Z0-9_]{3,16}")])
@valid_json("password", [valid_not_blank, valid_regexp(r"[a-zA-Z0-9]{6,50}")])
@valid_json("type", [valid_not_blank])
@valid_json("qq", [valid_not_blank, valid_regexp(r"[0-9]{5,11}")])
@transactional
def req(cur: Cursor = None) -> dict:
    """
    玩家申请注册
    """
    json_data = request.get_json()

    # 玩家名查重
    cur.execute("""
      SELECT
        password, qq, status
      FROM apply_player
      WHERE player_name = ?
    """, (json_data["playerName"], ))
    player = cur.fetchone()
    if player:
        if player[0] == json_data["password"] and player[1] == json_data["qq"]:
            if player[2] == ApplyStatus.NEW.name:
                return success("您之前的申请仍在等待审核")
            elif player[2] == ApplyStatus.ACCEPT.name:
                return success("您之前的申请已通过")
            elif player[2] == ApplyStatus.DENY.name:
                return success("您之前的申请已被拒绝")
            else:
                raise Exception("?????")
        else:
            return fail("玩家名已存在")
    # QQ 查重
    cur.execute("""
      SELECT
        player_name
      FROM apply_player
      WHERE qq = ?
    """, (json_data["qq"], ))
    if cur.fetchone():
        return fail("QQ 号已存在")

    # 校验参数
    req_type: str = json_data['type']
    op_name = None
    if req_type == ApplyType.QQLevel.name:
        pass
    elif req_type == ApplyType.Invite.name:
        if not valid_not_blank(json_data, "oldPlayerName"):
            return fail("未填写邀请人玩家名")
    elif req_type == ApplyType.PYJY.name:
        if not valid_not_blank(json_data, "opName"):
            return fail("未填写 OP 名")
        else:
            op_name = json_data["opName"]
            if op_name.endswith("_OP"):
                op_name = op_name[:-3]

    ip = get_ip("X-Forwarded-For")
    cur.execute("""
      SELECT
        COUNT(*)
      FROM apply_player
      WHERE ip = ?
      AND status = 'NEW'
    """, (ip, ))
    ip_count = cur.fetchone()
    if ip_count[0] > 3:
        return fail("同一个 IP 最多只能有三个申请")
        pass
    cur.execute("""
      SELECT
        req_time
      FROM apply_player
      WHERE ip = ?
      AND status = 'NEW'
      ORDER BY req_time DESC
      LIMIT 1
    """, (ip, ))
    last_time = cur.fetchone()
    if last_time and (datetime.now() - datetime.strptime(last_time[0], "%Y-%m-%d %H:%M:%S.%f")).seconds < 3600:
        return fail("同一个 IP 每小时只能申请一次")
        pass

    # 插 DB
    cur.execute("""
        INSERT INTO apply_player VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        json_data["playerName"],
        json_data["password"],
        datetime.now(),
        None,
        None,
        ApplyStatus.NEW.name,
        ApplyType.__members__[req_type].name,
        ip,
        json_data["qq"],
        json_data["oldPlayerName"],
        op_name
    ))

    return success()


if __name__ == '__main__':
    # logger
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s]: %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename='logs/%s.log' % time.strftime('%y-%m-%d_%H_%M_%S'),
                        filemode='w')
    sh = logging.StreamHandler()
    sh.setFormatter(logging.getLogger().handlers[0].formatter)
    logging.getLogger().addHandler(sh)

    # worker
    worker.init()

    # Flask
    # TODO 公共异常处理？
    app.run(port=setting.HTTP_PORT)  # 注意，阻塞性操作
