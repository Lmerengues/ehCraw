# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):
    os_my = "linux"
    mulu_dirs = {"windows":"C:/Users/mazy/Codes/ehimgs/mulu.txt","linux":"/root/ehimgs/mulu.txt"}
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            #print("++++++++++++++++++++++++++++++++--------------------------------------------")
            #print(item)
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        #image_paths = ["C:/Users/mazy/Codes/ehimgs/"+item["title_hash"]+"/"+str(item["id"])+".jpg" for ok, x in results if ok]
        #print("images_paths:--------------------------------------------")
        #print(image_paths)
        try:
            for p in image_paths:
                f = open(self.mulu_dirs[self.os_my],"a+")
                f.write(p + "\t" + str(item["id"]) + "\t" + item["title"] + "\t" + item["title_hash"] + "\n")
                f.close()
        except:
            print("some error!")
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
