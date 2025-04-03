import json
import time

import redis
from django.conf import settings
from django.db.models.expressions import result

from common.logger import logger


class RedisClient:
    def __init__(self):
        # self.client = redis.StrictRedis.from_url(settings.REDIS_URL)
        self.client = redis.StrictRedis.from_url('redis://127.0.0.1:6380/1')

    def add_sorted_set(self, key, member):
        """
        添加元素到有序集合
        """
        self.client.zadd(key, member)

    def get_all_sorted_set(self, key, withscores=True):
        """
        获取有序集合中的所有元素
        """
        return self.client.zrange(key, 0, -1, withscores=withscores)

    def get_range_sorted_set_by_days(self, key, days, withscores=True):
        """
        获取指定时间戳内的数据
        """
        max_score = time.time()
        min_score = max_score - (days * 24 * 60 * 60)
        return self.client.zrangebyscore(key, min_score, max_score, withscores=withscores)

    def delete_sorted_set_by_day(self, key, days=7):
        """
        删除超出日期天数的数据，默认为 7 天
        """
        try:
            delete_days = time.time() - (days * 24 * 60 * 60)
            self.client.zremrangebyscore(key, '-inf', delete_days)
            logger.info("successfully deleted {} days".format(days))
        except Exception as e:
            logger.error(e)

    def delete_key(self, key):
        """
        删除一个键下对应的所有数据
        """
        try:
            result = self.client.delete(key)
            if result == 1:
                logger.info("successfully deleted {}".format(key))
                return True, "success"
            else:
                logger.error("failed to delete {}".format(key))
                return False, "delete failed"
        except Exception as e:
            logger.error(f"Error deleting key {key}:{e}")
            return False, f"happen error {e}"

    def key_exists(self, key):
        """
        判断键是否存在
        """
        try:
            return self.client.exists(key)
        except Exception as e:
            logger.error(e)
            return False