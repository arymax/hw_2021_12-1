from re import fullmatch
from typing import Union

from scrapy.http import HtmlResponse

from .models import Article
from .spider import Spider
from ..kernel import Config


class Gamer(Spider):
    name = "Gamer"
    allowed_domains = ['forum.gamer.com.tw']
    start_urls = ["https://forum.gamer.com.tw"]

    def __init__(self, config: Config):
        super().__init__(config)
        self.DOWNLOADER_MIDDLEWARES.update({
            'src.crawler.middlewares.ptt_cookies.CookiesMiddleware': 700
        })

    def capture(self, response: HtmlResponse) -> Union[Article, None]:
        query = response.xpath("/html/body/div[5]/div/div[2]/section[2]/div[2]/div[1]/h1")
        full_title = self.clear_html_tags_from_selectors(query)
        if full_title.strip() == "":
            return None
        title_data = fullmatch(r"\【(.*?)\】(.*?)", full_title)
        # Get Tag and Title
        if title_data is None:
            tag = "Unknown"
            title = full_title
        else:
            tag = title_data.group(1)
            title = title_data.group(2)
        # Get Class
        # ToDo: 抓不到版名 只顯示[]
        query = response.xpath('/html/body/div[3]/ul/li[1]/a')
        class_ = self.clear_html_tags_from_selectors(query)
        # Get Content
        query = response.xpath(
            '/html/body/div[5]/div/div[2]/section[2]/div[2]/div[2]/article/div')
        content = self.clear_html_tags_from_selectors(query)
        # Get URL
        url = response.url
        # Get Words
        words = self.explode_as_list(content)
        # Get Times
        # ToDo: 抓不到時間 只顯示 []
        query = response.xpath(
            '/html/body/div[5]/div/div[2]/section[1]/div[2]/div[1]/div[3]/a[1]/@data-mtime')
        # Return
        return Article(
            origin=self.name,
            class_=class_,
            tag=tag,
            title=title,
            content=content,
            url=url,
            words=words,
            created_time=0,
            updated_time=0
        )
