# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from DBUtils.PooledDB import PooledDB
import threading
import functools
import setting
import pymysql


df_pool = PooledDB(
        pymysql,
        mincached=1,
        maxcached=10,
        blocking=True,
        host=setting.MYSQL_HOST,
        port=setting.MYSQL_PORT,
        db=setting.MYSQL_DBNAME,
        user=setting.MYSQL_USER,
        passwd=setting.MYSQL_PASSWD,
        charset="utf8"
    )
thread_local_data = threading.local()


def transactional(pool=None, force_commit: bool = False):
    """
    事务装饰器，被装饰的方法会被自动注入 cur
    限制：不能用于 generator 方法，否则 generator 获取数据时 cur 已关闭，会导致出异常
    """
    def warp(f):
        @functools.wraps(f)
        def fn(*args, **kw):
            if not hasattr(thread_local_data, 'conn') or not thread_local_data.conn:
                _pool = pool
                if not _pool:
                    _pool = df_pool
                thread_local_data.conn = _pool.connection()
                thread_local_data.conn_used = 0
            thread_local_data.conn_used += 1
            conn = thread_local_data.conn
            cur = conn.cursor()
            try:
                kw['cur'] = cur
                return f(*args, **kw)
            except Exception:
                conn.rollback()
                raise
            finally:
                thread_local_data.conn_used -= 1
                cur.close()
                if force_commit or not thread_local_data.conn_used:
                    conn.commit()
                if not thread_local_data.conn_used:
                    thread_local_data.conn = None
                    conn.close()
        return fn

    if type(pool).__name__ == 'function':
        real_fn = pool
        pool = None
        return warp(real_fn)
    else:
        return warp


@transactional
def init(cur=None):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS apply_op (
          username VARCHAR(16)  NOT NULL PRIMARY KEY,
          password VARCHAR(255) NOT NULL
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS apply_player (
          player_name     VARCHAR(16)  NOT NULL PRIMARY KEY,
          password        VARCHAR(255) NOT NULL,
          req_time        DATETIME     NOT NULL,
          apply_time      DATETIME,
          apply_op        VARCHAR(16),
          status          VARCHAR(16)  NOT NULL,
          type            VARCHAR(16)  NOT NULL,
          ip              VARCHAR(15)  NOT NULL,
          qq              VARCHAR(11)  NOT NULL,
          old_player_name VARCHAR(16),
          op_name         VARCHAR(16)
        );
    """)


init()
