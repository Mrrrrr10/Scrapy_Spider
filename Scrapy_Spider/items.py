# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import replace_escape_chars
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity, Compose


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# ---------- Item_LianJia ----------
class LianjiaItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    deal_price = scrapy.Field()
    average_price = scrapy.Field()
    listing_price = scrapy.Field()
    cost = scrapy.Field()
    adjust = scrapy.Field()
    seen = scrapy.Field()
    attention = scrapy.Field()
    view = scrapy.Field()
    type = scrapy.Field()
    floor = scrapy.Field()
    covered_area = scrapy.Field()
    structure_type = scrapy.Field()
    inner_area = scrapy.Field()
    building_type = scrapy.Field()
    orientation = scrapy.Field()
    built_at = scrapy.Field()
    decoration = scrapy.Field()
    structure = scrapy.Field()
    heating_mode = scrapy.Field()
    one_floor = scrapy.Field()
    own_years = scrapy.Field()
    is_elevator = scrapy.Field()
    lianjia_code = scrapy.Field()
    deal_type = scrapy.Field()
    listing_dt = scrapy.Field()
    house_usage = scrapy.Field()
    house_years = scrapy.Field()
    house_belongs = scrapy.Field()
    crawled_at = scrapy.Field()


# ---------- Item_JingZhun ----------
class JingZhunInFinancingItem(scrapy.Item):
    CompanyName = scrapy.Field()
    Logo = scrapy.Field()
    CompanyCcid = scrapy.Field()
    CompanyRcid = scrapy.Field()
    FinancePhase = scrapy.Field()
    IndustryType = scrapy.Field()
    CompanyBrief = scrapy.Field()
    IsExcellent = scrapy.Field()
    IsFunding = scrapy.Field()
    HasBP = scrapy.Field()
    PubDate = scrapy.Field()
    CompanyFullName = scrapy.Field()
    RelatedLink = scrapy.Field()
    WeChat = scrapy.Field()
    Member = scrapy.Field()
    Finance = scrapy.Field()
    Address1 = scrapy.Field()
    Address2 = scrapy.Field()
    InvestEntity = scrapy.Field()
    CompanyAsset = scrapy.Field()
    IndustryTags = scrapy.Field()
    ProjectInfo = scrapy.Field()


class JingZhunLastedInvestmentItem(scrapy.Item):
    CompanyName = scrapy.Field()
    Logo = scrapy.Field()
    CompanyCcid = scrapy.Field()
    CompanyRcid = scrapy.Field()
    FinancePhase = scrapy.Field()
    IndustryType = scrapy.Field()
    CompanyBrief = scrapy.Field()
    IsExcellent = scrapy.Field()
    IsFunding = scrapy.Field()
    HasBP = scrapy.Field()
    PubDate = scrapy.Field()
    CompanyFullName = scrapy.Field()
    RelatedLink = scrapy.Field()
    WeChat = scrapy.Field()
    Member = scrapy.Field()
    Finance = scrapy.Field()
    Address1 = scrapy.Field()
    Address2 = scrapy.Field()
    InvestEntity = scrapy.Field()
    CompanyAsset = scrapy.Field()
    IndustryTags = scrapy.Field()
    ProjectInfo = scrapy.Field()


class JingZhunLastedProjectItem(scrapy.Item):
    CompanyName = scrapy.Field()
    Logo = scrapy.Field()
    CompanyCcid = scrapy.Field()
    CompanyRcid = scrapy.Field()
    FinancePhase = scrapy.Field()
    IndustryType = scrapy.Field()
    CompanyBrief = scrapy.Field()
    IsExcellent = scrapy.Field()
    IsFunding = scrapy.Field()
    HasBP = scrapy.Field()
    PubDate = scrapy.Field()
    CompanyFullName = scrapy.Field()
    RelatedLink = scrapy.Field()
    WeChat = scrapy.Field()
    Member = scrapy.Field()
    Finance = scrapy.Field()
    Address1 = scrapy.Field()
    Address2 = scrapy.Field()
    InvestEntity = scrapy.Field()
    CompanyAsset = scrapy.Field()
    IndustryTags = scrapy.Field()
    ProjectInfo = scrapy.Field()


# ---------- Item_Tripadvisor ----------
class TripadvisorItem(scrapy.Item):
    hotel_url = scrapy.Field()
    hotel_cn_name = scrapy.Field()
    hotel_en_name = scrapy.Field()
    hotel_price = scrapy.Field()
    hotel_score = scrapy.Field()
    hotel_rating = scrapy.Field()
    hotel_addr = scrapy.Field()
    hotel_location = scrapy.Field()
    price_night = scrapy.Field()
    comments = scrapy.Field()
    username = scrapy.Field()
    userlocation = scrapy.Field()
    crawled_at = scrapy.Field()


# ---------- Item_Amazon ----------
class AmazonItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    brand = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    is_popular = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    comments_count = scrapy.Field()
    crawled_at = scrapy.Field()


class AmazonCommentItem(scrapy.Item):
    good_id = scrapy.Field()
    id = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
    user = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    user_url = scrapy.Field()
    crawled_at = scrapy.Field()


# ---------- Item_ITOrange ----------
class ITOrangeItem(scrapy.Item):
    investfirm = scrapy.Field()
    investfirm_wechat = scrapy.Field()
    investfirm_link = scrapy.Field()
    investfirm_desc = scrapy.Field()
    capital_scale = scrapy.Field()
    investment_scope = scrapy.Field()
    investment_round = scrapy.Field()
    project_scope = scrapy.Field()
    project_value = scrapy.Field()
    project_count = scrapy.Field()
    project_round = scrapy.Field()
    project = scrapy.Field()
    cooperator = scrapy.Field()
    cooperation_times = scrapy.Field()
    invest_info = scrapy.Field()


# ---------- Item_DianPing ----------
class DianPingItem(scrapy.Item):
    rankId = scrapy.Field()
    shopId = scrapy.Field()
    shopName = scrapy.Field()
    shopUrl = scrapy.Field()
    address = scrapy.Field()
    location = scrapy.Field()
    mainRegionName = scrapy.Field()
    mainCategoryName = scrapy.Field()
    refinedScore = scrapy.Field()
    avgPrice = scrapy.Field()
    shopPower = scrapy.Field()
    shopTags = scrapy.Field()
    shopInfo = scrapy.Field()
    crawled_at = scrapy.Field()


class DianPingCommentItem(scrapy.Item):
    shopName = scrapy.Field()
    shopId = scrapy.Field()
    shopUrl = scrapy.Field()
    shopScore = scrapy.Field()
    tags = scrapy.Field()
    reviewCount = scrapy.Field()
    reviewInfo = scrapy.Field()
    brief = scrapy.Field()
    star = scrapy.Field()
    score = scrapy.Field()
    review = scrapy.Field()
    recommend = scrapy.Field()
    crawled_at = scrapy.Field()
