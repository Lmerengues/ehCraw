# encoding: utf-8

import scrapy

class RucNewsSpider(scrapy.Spider):
    name = "InfoTeacher"
    start_urls = [
        #'http://info.ruc.edu.cn/academic_faculty.php',
        'http://info.ruc.edu.cn/academic_faculty.php?teacher_dept=0&teacher_type=0'
    ]

    def parseTeacher(self, response):
        name = "\\n".join(response.css(".navigation ::text").extract())
        info = ",".join(response.css(".intro p::text").extract())
        contact =",".join(response.css(".contact p::text").extract())
        extra = ",".join(response.css(".block p::text").extract())
        #获取所有介绍block
        blocks = response.css(".block")
        allBlocks=""
        for block in blocks:
            #title:当前介绍小节标题
            title = block.css(".title::text").extract_first()
            #desc:当前小节内容
            desc =  "\\n".join(block.css("p::text").extract()[1:])
            #拼接
            allBlocks = allBlocks + ("["+title+"] "+desc+"###")

        yield{"教师姓名":name, "简介":info, "联系方式":contact,"其他内容":extra ,"其他内容(带格式)":allBlocks }


    def parse(self, response):
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



        #if xp is not None:
        #    npage = response.urljoin(xp)
        #    yield scrapy.Request(npage, self.parse)

