# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random as rd
from scrapy.http import HtmlResponse
from logging import getLogger
from template.useragent import user_agent_list
import time


class TemplateSpiderMiddleware(object):
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

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TemplateDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware:
    def __init__(self):
        self.logger = getLogger(__name__)

    def process_request(self, request, spider):
        """
        用chrome抓取页面
        :param request: Request请求对象
        :param spider: Spider对象
        :return: HtmlResponse响应
        """
        # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        usedSelenium = request.meta.get("usedSelenium", False)
        if usedSelenium:
            self.logger.debug("chrome is getting page")
            try:
                spider.browser.get(request.url)
                # filename = 'response'
                # open(filename, 'w').write(spider.browser.page_source)
            except Exception as e:
                self.logger.debug(f"chrome getting page error, Exception = {e}")
                print(f"chrome getting page error, Exception = {e}")
                return HtmlResponse(url=request.url, status=500, request=request)
            else:
                time.sleep(3)
                return HtmlResponse(
                    url=request.url,
                    body=spider.browser.page_source,
                    request=request,
                    # 最好根据网页的具体编码而定
                    encoding="utf-8",
                    status=200,
                )


class user_agent(object):
    def __init__(self):
        self.user_agent_list = user_agent_list

    def process_request(self, request, spider):
        request.headers["USER_AGENT"] = rd.choice(self.user_agent_list)
