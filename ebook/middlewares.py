# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import USER_AGENTS
from .settings import PROXIES
import random
import base64

class EbookSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxyMiddleware(object):
    # process_request必要方法
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)

        if proxy['user_pass'] is None:
            # 代理需要写在 request 的 meta 信息中
            request.meta["proxy"] = "http://" + proxy['ip_port']
        else:
            # 对账户进行 base64 的编码转换
            base64_userpasswd = base64.b64encode(proxy["user_pass"].encode("utf-8")).decode()

            # 代理的 IP 地址
            request.meta["proxy"] = "http://" + proxy['ip_port']

            # 代理的 用户名密码
            request.headers["Proxy-Authorization"] = 'Basic ' + base64_userpasswd
