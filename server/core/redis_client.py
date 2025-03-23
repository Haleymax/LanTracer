import time

import redis
from django.conf import settings

from common.logger import logger


class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis.from_url(settings.REDIS_URL)

    def add_sorted_set(self, key, data):
        """
        添加元素到有序集合
        """
        self.client.zadd(key, data)

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