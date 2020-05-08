# -*- coding: utf-8 -*-
import scrapy
from template.items import TemplateItem
from template.custom_settings import TemplateSpiderSetting
from template.useragent import user_agent_list
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pydispatch import dispatcher
from scrapy import signals
import random as rd


class TemplateSpider(scrapy.Spider):
    name = "templatespider"
    allowed_domains = [""]
    custom_settings = TemplateSpiderSetting

    def __init__(self, **kwargs):
        # selenium setting
        self.page_timeout = self.custom_settings["SELENIUM_PAGE_TIMEOUT"]
        self.element_timeout = self.custom_settings["SELENIUM_ELEMENT_TIMEOUT"]
        self.field = self.custom_settings["FIELD"]
        user_agent = rd.choice(user_agent_list)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-agent={user_agent}")
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.set_page_load_timeout(self.page_timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, self.element_timeout)  # 指定元素加载超时时间

        # url from arguments
        self.key_word = kwargs["keyword"]
        self.start_pos = str((int(kwargs["page"]) - 1) * 15)
        self.search_result_url = (
                "https://search.douban.com/book/subject_search?"
                + "search_text="
                + self.key_word
                + "&start="
                + self.start_pos
        )

        dispatcher.connect(
            receiver=self.mySpiderCloseHandle, signal=signals.spider_closed
        )

    def mySpiderCloseHandle(self, spider):
        self.browser.quit()

    def start_requests(self):
        pass

    def parse_search_result(self, response):
        pass

    def parse(self, response):
        pass
