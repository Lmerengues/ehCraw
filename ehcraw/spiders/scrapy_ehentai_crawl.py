# encoding: utf-8

import scrapy
import urllib3
import time
import os
import re
from ..items import EhcrawItem
import traceback

class RucNewsSpider(scrapy.Spider):
    name = "ehentaiSearch"
    start_urls = [
        #'http://info.ruc.edu.cn/academic_faculty.php',
        #'https://e-hentai.org/?f_doujinshi=0&f_manga=0&f_artistcg=0&f_gamecg=0&f_western=0&f_non-h=0&f_imageset=0&f_cosplay=0&f_asianporn=0&f_misc=0&f_search=momoya+dynasty+warrior+chinese&f_apply=Apply+Filter'
        #"https://e-hentai.org/g/1194743/dbcc0dcb47/"
        #"https://e-hentai.org/g/830143/9f31b45815/"
         #"https://e-hentai.org/g/888847/35468d953b/",
         "https://e-hentai.org/g/137236/ac57f7cfe6/",
         "https://e-hentai.org/g/437851/2817853b84/",
         "https://e-hentai.org/g/265258/bc40736834/",
         "https://e-hentai.org/g/196644/bba07b6ee7/",
         "https://e-hentai.org/g/75951/01967ebd19/",
         "https://e-hentai.org/g/54422/0cfce4505f/",
         "https://e-hentai.org/g/54342/3104cf5515/",
         "https://e-hentai.org/g/1228631/8c0f5d3c7a/"
    ]
    http = urllib3.PoolManager()

    #def parse(self, response):
    def parse0(self,response):
        for gallery in response.css(".itg tr"):
            title_hash = str(int(time.time()))
            title = "\\n".join(gallery.css(".it5 ::text").extract()[:])
            url  = gallery.css('.it5 a::attr("href")').extract_first()
            yield response.follow(url,meta={"title_hash":title_hash,"title":title},callback=self.parseGallery)

    #def parseGallery(self, response):
    def parse(self, response):
        #galleryTitle = response.meta["title"]
        #galleryTitleHash = response.meta["title_hash"]

        galleryTitle = re.sub('[\/:*?"<>|]','-',response.css("#gn::text").extract_first())
        galleryTitleHash = str(int(time.time()))
        first_img_page = response.css('#gdt .gdtm div a::attr("href")').extract_first()
        img_id = 1
        #if os.path.isdir("C:/Users/mazy/Codes/ehimgs/"+galleryTitleHash):
        #    pass
        #else:
        #    os.mkdir("C:/Users/mazy/Codes/ehimgs/"+galleryTitleHash)
        #try:
        #    os.mkdir( "C:/Users/mazy/Codes/ehimgs/"+galleryTitleHash, 777 )
            #os.mkdir( "/root/ehimgs/"+galleryTitleHash, 777 )
        #except Exception as e:
        #    traceback.print_exc()
            #或者得到堆栈字符串信息
        #    info = traceback.format_exc()
        yield response.follow(first_img_page,meta={"id":img_id,"title":galleryTitle,"title_hash":galleryTitleHash},callback=self.parseImage)
    
    def parseImage(self, response):
        galleryTitle = response.meta["title"]
        galleryTitleHash = response.meta["title_hash"]
        img_id = response.meta["id"]
        imgurl =  response.css('#img::attr("src")').extract_first()


        yield {"image_urls":[imgurl],"title":galleryTitle,"title_hash":galleryTitleHash,"id":img_id}

        #yield {"imgurl":imgurl}
        #r = self.http.request('GET', imgurl)
        t = time.time()
        #with open("/root/ehimgs/"+galleryTitle+"/"+str(img_id)+".jpg", 'wb') as f:
        #    f.write(r.data)
        next_page = response.css('#i3 a::attr("href")').extract_first()
        yield response.follow(next_page,meta={"id":img_id+1,"title":galleryTitle,"title_hash":galleryTitleHash},callback=self.parseImage)

        '''
        for teacher in response.css('div.card'):             
            #yield {
            #    'name': teacher.css('div.name a::text').extract_first(),
            #    'homepage':  teacher.css('div.name a::attr("href")').extract_first(),
            #    "research":",".join(teacher.css('div.research p::text').extract())
            #}
            homepage = teacher.css('div.name a::attr("href")').extract_first()
            yield response.follow(homepage, callback=self.parseTeacher)

        xp = response.css('div.next a::attr("href")').extract_first()
        yield response.follow(xp, callback=self.parse)
        '''


        #if xp is not None:
        #    npage = response.urljoin(xp)
        #    yield scrapy.Request(npage, self.parse)

