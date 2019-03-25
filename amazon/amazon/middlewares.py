# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from amazon.user_agents import user_agents
import logging


class RandomUserAgentMiddleware():
    def __init__(self):
        self.user_agents = user_agents
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        user_agents = random.choice(self.user_agents)
        self.logger.debug('使用user_agents：' + user_agents)
        request.headers['User-Agent'] = user_agents
