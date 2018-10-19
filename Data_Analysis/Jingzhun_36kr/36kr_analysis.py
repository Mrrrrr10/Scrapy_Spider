import re
import pymongo
from collections import Counter
from pyecharts import WordCloud, Map, Geo, Bar, Pie

class DataAnalysis(object):

    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.Spider
        self.collection = [db.JingZhunInFinancingItem, db.JingZhunLastedInvestmentItem, db.JingZhunLastedProjectItem]
        self.collection_infinancing = db.JingZhunInFinancingItem
        self.collection_lastedinvestment = db.JingZhunLastedInvestmentItem
        self.collection_lastedproject = db.JingZhunLastedProjectItem

    def run(self):
        self.analysis_industry_type()
        self.analysis_address()
        self.analysis_location()
        self.analysis_corporate_services()

    def analysis_industry_type(self):
        """三种投资类型的数据可视化"""
        filed = []
        attr = []
        counter = Counter()
        for collection in self.collection:
            cursor = collection.find({}, {"IndustryType": 1, "_id": 0})
            IndustryType = [item.get('IndustryType') for item in cursor]
            for type in IndustryType:
                counter[type] += 1

            for k, v in counter.most_common(50):
                filed.append(k)
                attr.append(v)
            wordcloud = WordCloud(width=1300, height=620)
            wordcloud.add("36kr创投企业类型", filed, attr, word_size_range=[30, 100], shape='diamond')
            wordcloud.render("%s_IndustryType.html" % collection.name)

    def analysis_address(self):
        """所有类型企业的位置可视化"""
        address = []
        filed = []
        attr = []
        counter = Counter()
        for collection in self.collection:
            cursor = collection.find({}, {"Address1": 1, "_id": 0})
            for item in cursor:
                address.append(item.get('Address1')[1].replace("市", '').replace("省", ''))
        for Address in address:
            counter[Address] += 1

        for k, v in counter.most_common(100):
            filed.append(k)
            attr.append(v)

        map = Map("36kr创投企业省级分布图", width=1200, height=600)
        map.add("", filed, attr, maptype="china", is_visualmap=True, visual_text_color="#000", is_map_symbol_show=False, )

        map.render("Address.html")

    def analysis_location(self):
        """所有类型企业的详细位置可视化"""
        geo = []
        filed = []
        attr = []
        counter = Counter()
        for collection in self.collection:
            cursor = collection.find({}, {"Address2": 1, "_id": 0})
            for item in cursor:
                if item.get('Address2')[1]:
                    if "省" in item.get('Address2')[1]:
                        location = re.search('省(.*)', item.get('Address2')[1]).group(1).replace("市", "")
                    else:
                        location = re.search('(.*?)市', item.get('Address2')[1])
                        location = location.group(1) if location else None
                    if location:
                        geo.append(location)

        for Address in geo:
            counter[Address] += 1

        for k, v in counter.most_common(25):
            filed.append(k)
            attr.append(v)

        data = list(zip(filed, attr))
        geo = Geo(
            "36kr前25创投企业市级分布图",
            "data from 36kr",
            title_color="#fff",
            title_pos="center",
            width=1200,
            height=600,
            background_color="#404a59",
        )
        key, value = geo.cast(data)
        geo.add(
            "",
            key,
            value,
            visual_range=[0, 200],
            visual_text_color="#fff",
            symbol_size=15,
            is_visualmap=True,
        )
        geo.render("Location.html")

    def analysis_corporate_services(self):
        """企业服务类型的公司数据可视化"""
        phase_list =[]
        phase_filed = []
        phase_attr = []
        phase_counter = Counter()
        for collection in self.collection:
            cursor = collection.find({"IndustryType": "企业服务"}, {"FinancePhase": 1, "IndustryTags": 1, "_id": 0})
            for item in cursor:
                phase_list.append(item.get('FinancePhase'))

        for phase in phase_list:
            phase_counter[phase] += 1

        for k, v in phase_counter.most_common(50):
            phase_filed.append(k)
            phase_attr.append(v)

        bar = Bar('企业服务类型的公司投资轮数柱状图')
        bar.add('', phase_filed, phase_attr, mark_line=["min", "max"])
        bar.render("Phase.html")

if __name__ == '__main__':
    analysis = DataAnalysis()
    analysis.run()






