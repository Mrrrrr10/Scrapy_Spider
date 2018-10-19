# ⭐Scrapy_Spider
**基于scrapy的爬虫**

## 项目列表
1. 项目1：[Amazon_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
2. 项目2：[Lianjia_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
3. 项目3：[Tripadvisor_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
4. 项目4：[36kr_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)

## 项目描述：
### 项目1：[Amazon_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
* **需求**：爬取中国亚马逊的海外购所有类目热销排名的商品详情，用户评论，并对数据清洗后写入mongodb
* **用法**：```scrapy crawl amazon```
* **成果**：
![Comment](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Amazon/comment.png)
![Product](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Amazon/product.png)
* **后续工作**：可以对某一类特定的商品的评论进行数据分析、可视化

### 项目2：[Lianjia_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
* **需求**：爬取广州链家二手房成功成交的订单数据
* **用法**：```scrapy crawl lianjia```
* **成果**：
![lianjia](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Lianjia/detail.png)
* **后续工作**：可以长期抓取数据，进行房价的数据分析

### 项目3：[Tripadvisor_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
* **需求**：爬取猫头鹰tripadvisor Top25热门景点的酒店详情，对应的用户地址，并对数据清洗后写入mongodb，进行数据分析、可视化
* **用法**：```scrapy crawl tripadvisor```
* **成果**：
![tripadvisor](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Tripadvisor/world.png)
![tripadvisor](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Tripadvisor/chinese.png)
* **后续工作**：可以抓取某一特定国家的用户，进行用户信息抓取和行为分析
* **不足**：代码结构需要调整一下，还有就是用户的地址，举个例子：有些用户填写London、有些用户填写london、有些填写United Kingdom，很明显这种都属于英国，这样就会造成分析的障碍。

### 项目4：[36kr_Spider](https://github.com/Mrrrrr10/Scrapy_Spider/tree/master/Scrapy_Spider/spiders)
* **需求**：爬取36kr旗下的鲸准创投网站的创投企业详情，并对数据清洗后写入mongodb，进行数据分析、可视化
* **说明**：由于网页版的爬虫需要身份认证后才能爬取到企业信息，所以把目标转向客户端，我这里用的时创投助手这个app，需要登陆后用抓包工具charles进行分析url，发现虽然需要登陆，但是返回数据的url不需要cookie就可以访问，所以直接访问抓取就好了。
* **用法**：```scrapy crawl Jingzhun_36kr```
* **数据可视化**：
![address](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/address.png)
![企业分布](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/%E4%BC%81%E4%B8%9A%E5%88%86%E5%B8%83.png)
![投资轮数](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/%E5%B1%9E%E4%BA%8E%E4%BC%81%E4%B8%9A%E6%9C%8D%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%9A%84%E6%8A%95%E8%B5%84%E8%BD%AE%E6%95%B0.png)
![类型1](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/%E6%9C%80%E6%96%B0%E8%8E%B7%E6%8A%95%E4%BC%81%E4%B8%9A%E7%B1%BB%E5%9E%8B.png)
![类型2](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/%E6%9C%80%E6%96%B0%E9%A1%B9%E7%9B%AE%E4%BC%81%E4%B8%9A%E7%B1%BB%E5%9E%8B.png)
![类型3](https://github.com/Mrrrrr10/Scrapy_Spider/blob/master/Data_Analysis/Jingzhun_36kr/%E8%9E%8D%E8%B5%84%E4%B8%AD%E7%9A%84%E4%BC%81%E4%B8%9A%E7%B1%BB%E5%9E%8B.png)
* **后续工作**：可以根据服务类型进一步细分
