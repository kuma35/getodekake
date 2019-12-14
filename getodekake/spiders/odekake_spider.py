#
# -*- code:utf-8 -*-
import json
import scrapy
from scrapy_selenium import SeleniumRequest


class OdekakeSpider(scrapy.Spider):
    """
    extract trains from JR West JR-Odekake site.

    JP:JR西日本JRおでかけサイトから列車情報抽出。
    """
    name = "odekake"

    def __init__(self, urls=None, *args, **kwargs):
        """
        Parameters
        ----------
        urls : str
            url list by json array str
            example: ``'["url1", "url2", "url3"]'``
        """
        super(OdekakeSpider, self).__init__(*args, **kwargs)
        self.start_urls = json.loads(urls)

    def start_requests(self):
        """
        from spider-arg urls

        JP:スパイダー引数 urls で指定したurl群を指定
        """
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse_station)

    def parse_station(self, response):
        """
        extract train urls from station timetable and
        get train pages.

        JP:駅時刻表ページより列車時刻表URL群を抽出し、
        各列車時刻表ページ取得
        """
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        args = {}
        args['eki'] =  response.xpath(
                "//div[@class='station_time']/h1/span/text()").get()
        senku_houmen = response.xpath(
            "//div[@class='station_time']/h1/text()").get()
        (args['senku'], args['houmen']) = senku_houmen.split('\u3000')
        for link in response.xpath("//font[@class='min']/parent::a/@href"):
            train_url = response.urljoin(link.get())
            yield scrapy.Request(url=train_url,
                                 callback=self.parse_train,
                                 cb_kwargs=args)

    def parse_train(self, response, eki, senku, houmen):
        """
        extract train info from train page.

        JP:列車情報ページより列車情報抽出。
        """
        from scrapy.shell import inspect_response
        inspect_response(response, self)
