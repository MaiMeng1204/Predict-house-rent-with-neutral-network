# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    location = scrapy.Field()  # 地点
    house_type = scrapy.Field()  # 房屋类型
    house_code = scrapy.Field()   # 房源编号
    price = scrapy.Field()  # 价格
    tags = scrapy.Field()   # 房源标签
    lease = scrapy.Field()  # 租赁方式
    area = scrapy.Field()   # 面积
    orientation = scrapy.Field()  # 朝向
    floor = scrapy.Field()  # 楼层
    elevator = scrapy.Field()   # 电梯
    stall = scrapy.Field()  # 车位
    water = scrapy.Field()  # 用水
    electricity = scrapy.Field()    # 用电
    fuel_gas = scrapy.Field()   # 燃气
    heating = scrapy.Field()    # 采暖
    facility = scrapy.Field()    # 配套设施
    description = scrapy.Field()    # 房源描述
    pass
