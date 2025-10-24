import redis
import os

from dotenv import load_dotenv


class Repository:
    def __init__(self):
        load_dotenv()

        self.__host = os.getenv('DB_HOST')
        self.__port = os.getenv('DB_PORT')
        self.__register_expire_seconds = os.getenv('DB_REGISTER_EXPIRE_SECONDS')
        self.__r = None

    def connect(self):
        self.__r = redis.Redis(host=self.__host, port=self.__port, db=0)

    def insert(self, key: str, value: str):
        self.__r.set(key, value)
        self.__r.expire(key, self.__register_expire_seconds)

    def insert_list(self, key: str, value: str):
        self.__r.rpush(key, value)
        self.__r.ltrim(key, -20, -1)
        self.__r.expire(key, self.__register_expire_seconds)

    def get(self, key: str) -> str:
        return self.__r.get(key)
    
    def get_list(self, key: str, limit: int = None) -> list[str]:
        if limit:
            raw_data = self.__r.lrange(key, -limit, -1)
        else:
            raw_data = self.__r.lrange(key, 0, -1)
        return [item.decode('utf-8') for item in raw_data]

    def remove(self, key: str):
        self.__r.delete(key)
        