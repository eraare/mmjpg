# -*- coding: utf-8 -*-
import scrapy
from mmjpg import items


class MmjpgSpiderSpider(scrapy.Spider):
    name = 'mmjpg_spider'
    # allowed_domains = ['mmjpg.com']
    start_urls = ['http://mmjpg.com/']

    def parse(self, response):
        current_page = response.css('div.pic ul li span.title a')
        for gallery in current_page:
            gallery_title = gallery.css('a::text').extract_first()
            gallery_url = gallery.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=gallery_url, headers={'Referer': gallery_url}, callback=self.parse_gallery)
        # 下一页
        next_links = response.css('div.page a.ch')
        for next_link in next_links:
            next_page_name = next_link.css('a.ch::text').extract_first()
            if next_page_name == '下一页':
                next_page = next_link.css('a.ch::attr(href)').extract_first()
                if next_page is not None:
                    next_page_url = response.urljoin(next_page)
                    yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_gallery(self, response):
        image = response.css('div.article')
        item = items.MmjpgItem()
        item['image_referer'] = [response.url]  # 防盗链referer传递
        item['image_path'] = image.css('div.content img::attr(alt)').extract_first().split()[0]
        item['image_title'] = image.css('h2::text').extract_first()
        item['image_urls'] = [image.css('div.content img::attr(src)').extract_first()]
        yield item
        # 下一页
        next_page = response.css('a.ch.next::attr(href)').extract_first()
        next_page_name = response.css('a.ch.next::text').extract_first()
        if next_page is not None and next_page_name == '下一张':
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, headers={'Referer': next_page_url}, callback=self.parse_gallery)
