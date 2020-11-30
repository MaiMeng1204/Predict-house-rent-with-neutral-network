import scrapy
import time
from scrapy.http import Request
from lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):     # 必须继承scrapy.Spider

    name = "lianjia"   # 名称
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ['https://sh.lianjia.com/zufang']   # URL列表

    def parse(self, response):
        # 获取各个区的url
        regions = response.css('#filter > ul:nth-child(2) > li.filter__item--level2 > a')
        for region in regions[1:]:
            url = 'https://sh.lianjia.com' + region.attrib['href']
            yield Request(url, callback=self.parse_region)

    # 遍历所有页
    def parse_region(self, response):
        house_num = int(response.css('#content > div.content__article > p > span.content__title--hl::text').get())  # 房子数量
        page_num = min(house_num // 30 + 1, 100)    # 每页展示30条
        for i in range(1, page_num + 1):
            time.sleep(0.1)
            url = response.url + 'pg{}'.format(i)
            print(url)
            yield Request(url, callback=self.parse_overview)

    # 爬取房屋概况信息
    def parse_overview(self, response):
        item = LianjiaItem()
        infos = response.css('div.content__list--item')
        for info in infos:
            time.sleep(0.1)
            suburl = info.css('.content__list--item--aside').attrib['href']
            if 'zufang' in suburl:
                item['title'] = info.css('.content__list--item--aside').attrib['title']
                item['location'] = '-'.join(info.css('.content__list--item--des a::text').getall())
                des = info.css('.content__list--item--des::text').getall()
                item['house_type'] = [x.strip() for x in des if '室' in x][0]
                url = 'https://sh.lianjia.com' + suburl
                yield Request(url, meta={'item': item}, callback=self.parse_info)

    # 爬取房屋详细信息
    def parse_info(self, response):
        try:
            item = response.meta['item']
            item['house_code'] = response.css('i.house_code::text').get().split('：')[1]
            item['price'] = response.css('div.content__aside--title span::text').get() + \
                response.css('div.content__aside--title::text').getall()[1].strip()
            item['tags'] = ','.join(response.css('p.content__aside--tags i::text').getall())
            item['lease'] = response.css('#aside > ul > li:nth-child(1)::text').get()
            item['area'] = response.css('#info > ul:nth-child(2) > li:nth-child(2)::text').get().split('：')[1]
            item['orientation'] = response.css('#info > ul:nth-child(2) > li:nth-child(3)::text').get().split('：')[1]
            item['floor'] = response.css('#info > ul:nth-child(2) > li:nth-child(8)::text').get().split('：')[1]
            item['elevator'] = response.css('#info > ul:nth-child(2) > li:nth-child(9)::text').get().split('：')[1]
            item['stall'] = response.css('#info > ul:nth-child(2) > li:nth-child(11)::text').get().split('：')[1]
            item['water'] = response.css('#info > ul:nth-child(2) > li:nth-child(12)::text').get().split('：')[1]
            item['electricity'] = response.css('#info > ul:nth-child(2) > li:nth-child(14)::text').get().split('：')[1]
            item['fuel_gas'] = response.css('#info > ul:nth-child(2) > li:nth-child(15)::text').get().split('：')[1]
            item['heating'] = response.css('#info > ul:nth-child(2) > li:nth-child(17)::text').get().split('：')[1]
            item['stall'] = response.css('#info > ul:nth-child(2) > li:nth-child(11)::text').get().split('：')[1]
            facilities = response.css('body > div.wrapper > div:nth-child(2) > div.content.clear.w1150 > div.content__detail > div.content__article.fl > ul > li')
            facility_list = []
            for facility in facilities[1:]:
                if 'no' not in facility.attrib['class']:
                    facility_list.append(facility.css('::text').getall()[-1].strip())
            item['facility'] = ','.join(facility_list)
            item['description'] = ''.join([x.strip() for x in response.css('#desc > p:nth-child(3)::text').getall()])
            yield item   # 返回数据
        except AttributeError as e:
            time.sleep(600)
            print(e)
