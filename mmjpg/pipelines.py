# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines import images
from scrapy.exceptions import DropItem
import os


# class MmjpgPipeline(object):
#     def process_item(self, item, spider):
#         return item
class MmjpgPipeline(images.ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            image_referer = item['image_referer'] + '/'
            yield scrapy.Request(image_url, headers=self.headers(item['image_referer'][i]), meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        if hasattr(item, 'image_paths'):
            item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_path = item.get('image_path')
        image_title = item.get('image_title') + '.jpg'
        the_path = os.path.join(image_path, image_title)
        return the_path

    def headers(self, referer, ):
        """处理下载防盗链"""
        headers = {
            # 'Host': 'img.mmjpg.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            # 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': referer,
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Upgrade-Insecure-Request': 1
        }
        return headers
