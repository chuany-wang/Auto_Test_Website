"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain: 对接三方 ,发送到三方
"""
import sys
import json
import redis
from common.lo_logger import logger
from common.read_data import read_conf
from typing import TypeVar, Optional, Dict


T = TypeVar('T')


class RedisPool:
    __Pool = None

    def __init__(self):
        envir = sys.platform.lower()
        REDIS = read_conf(value='REDIS')
        if envir == 'win32':
            self.REDIS_CONFIG = REDIS.get('TEST')
        elif envir == 'linux':
            self.REDIS_CONFIG = REDIS.get('PRO')
        self.session = self.redis_conn()

    def redis_conn(self) -> Optional[redis.StrictRedis]:
        try:
            if not RedisPool.__Pool:
                RedisPool.__Pool = redis.ConnectionPool(**self.REDIS_CONFIG)
            session = redis.StrictRedis(connection_pool=RedisPool.__Pool)
            return session
        except Exception as e:
            logger.error(f'连接错误！{e}')
            return None

    def _execute_command(self, command: str, *args, **kwargs) -> T:
        with self.session.pipeline() as pipe:
            getattr(pipe, command)(*args, **kwargs)
            ret = pipe.execute()
        if ret:
            return self._decode_result(ret[0])  # 解码结果
        else:
            logger.error('操作失败')
            return None

    @staticmethod
    def _decode_result(result):
        if isinstance(result, bytes):
            return result.decode()
        elif isinstance(result, list):
            return [item.decode() if isinstance(item, bytes) else item for item in result]
        elif isinstance(result, dict):
            return {key.decode(): value.decode() if isinstance(value, bytes) else value for key, value in
                    result.items()}
        else:
            return result

    def expire(self, key: str, seconds: int) -> Optional[bool]:
        return self._execute_command('expire', key, seconds)

    def set(self, key: str, value: str, expiration: int = None) -> Optional[bool]:
        result = self._execute_command('set', key, value)
        if expiration is not None:
            self.expire(key, expiration)
        return result

    def get(self, key: str) -> Optional[str]:
        return self._execute_command('get', key)

    def set_dict(self, key, value, expiration: int = None) -> Optional[bool]:
        result = self._execute_command('hmset', key, value)
        if expiration is not None:
            self.expire(key, expiration)
        return result

    def get_dict(self, key, value=None) -> Optional[dict]:
        if value:
            return self._execute_command('hmget', key, value)
        else:
            return self._execute_command('hgetall', key)

    def set_list(self, key: str, value: list, expiration: int = None) -> Optional[bool]:
        value_str = json.dumps(value)  # 将列表转换为字符串
        result = self._execute_command('set', key, value_str)
        if expiration is not None:
            self.expire(key, expiration)
        return result

    def get_list(self, key: str) -> Optional[list]:
        value_str = self._execute_command('get', key)
        if value_str is not None:
            value = json.loads(value_str)  # 将字符串转换回列表
            return value
        else:
            return None

    def set_multiple(self, key_value_dict: Dict[str, dict], expiration: int = None) -> Optional[bool]:
        pipe = self.session.pipeline()

        for key, value in key_value_dict.items():
            value_str = json.dumps(value)  # 将字典转换为字符串
            pipe.set(key, value_str)

            if expiration is not None:
                pipe.expire(key, expiration)

        results = pipe.execute()
        return all(results)  # 返回所有写入操作是否成功的结果

    def flush_all(self) -> Optional[bool]:
        return self._execute_command('flushall')


re_db = RedisPool()

if __name__ == '__main__':
    # session_id = re_db.get("SID_https://test.cncest.com/")
    # print(session_id)

    text = re_db.get_list("https://test.cncest.com/")
    # print(text.get("sku"))
    print(type(text))
