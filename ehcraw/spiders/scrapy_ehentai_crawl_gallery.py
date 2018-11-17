# encoding: utf-8

import scrapy
import urllib3
import time
import os
import re

class gallerySpider(scrapy.Spider):
    name = "ehentaiGallery"
    start_urls = [
        #'http://info.ruc.edu.cn/academic_faculty.php',
        #'https://e-hentai.org/?f_doujinshi=0&f_manga=0&f_artistcg=0&f_gamecg=0&f_western=0&f_non-h=0&f_imageset=0&f_cosplay=0&f_asianporn=0&f_misc=0&f_search=momoya+dynasty+warrior+chinese&f_apply=Apply+Filter'
        "https://e-hentai.org/g/522692/868398b3b5/"
    ]
    http = urllib3.PoolManager()

    def parse(self, response):
        galleryTitle = re.sub('[\/:*?"<>|]','-',response.css("#gn::text").extract_first())
        first_img_page = response.css('#gdt .gdtm div a::attr("href")').extract_first()
        img_id = 1
        try:
            os.mkdir( "C:/Users/mazy/Codes/ehimgs/"+galleryTitle, 777 )
        except:
            print("no need to mkdir "+"C:/Users/mazy/Codes/ehimgs/"+galleryTitle)
        yield response.follow(first_img_page,meta={"id":img_id,"title":galleryTitle},callback=self.parseImage)
    
    def parseImage(self, response):
        galleryTitle = response.meta["title"]
        img_id = response.meta["id"]
        imgurl =  response.css('#img::attr("src")').extract_first()
        yield {"imgurl":imgurl}
        r = self.http.request('GET', imgurl)
        t = time.time()
        with open("C:/Users/mazy/Codes/ehimgs/"+galleryTitle+"/"+str(img_id)+".jpg", 'wb') as f:
            f.write(r.data)

        next_page = response.css('#i3 a::attr("href")').extract_first()
        yield response.follow(next_page,meta={"id":img_id+1,"title":galleryTitle},callback=self.parseImage)

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

