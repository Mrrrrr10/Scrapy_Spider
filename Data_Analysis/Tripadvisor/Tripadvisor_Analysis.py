import pymongo
from pyecharts import Map
from collections import Counter

class DataAnalysis(object):

    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.Spider
        self.collection = db.TripadvisorItem

    def run(self):
        self.world_analysis()
        self.china_analysis()

    def world_analysis(self):
        """分析哪些国家的人们喜欢去旅游(前100)"""
        location_key = []
        location_value = []
        area_USA = ["California", "New York", "New York", "Texas", "Illinois",
                    "Massachusetts", "Washington", "Georgia", "Colorado",
                    "Pennsylvania", "Virginia", "District of Columbia", "New Jersey",
                    "Minnesota", "North Carolina", "Ohio", "Oregon", "Michigan",
                    "USA", "CA", "Arizona", "Maryland", "Wisconsin", "Connecticut",
                    "NY", "Los Angeles", "Louisiana", "Nevada", "Hawaii", "Missouri", "Utah",
                    "Tennessee", "Indiana"]
        area_UK = ["London", "UK", "England", "london", "Manchester", "Dublin", "uk"]
        area_Australia = ["Sydney", "Melbourne", "Perth", "Brisbane"]
        area_Netherladns = ["The Netherlands", "Amsterdam"]
        area_Canada = ["Toronto", "Vancouver", "Ontario"]
        area_China = ["Taiwan", "Hong Kong", "Macau"]
        area_Turkey = ["Istanbul"]
        area_Korea = ["Korea"]
        area_Brazil = ["SP"]
        area_Italy = ["Rome"]
        area_Spain = ["Barcelona"]
        area_France = ["Paris"]
        area_United_Arab_Emirates = ["Dubai"]

        query = {"userlocation": {"$elemMatch": {"$ne": ""}}}
        cursor = self.collection.find(query)
        world_list = [item.get("userlocation") for item in cursor]

        print('*' * 20, 'Start Analysis', '*' * 20)
        print('The cardinality of user are %s' % len(world_list))
        c = Counter()
        for location in world_list:
            if ',' in location:
                country = location.split(',')[-1].strip()
                if country in area_USA:
                    c['United States'] += 1
                elif country in area_UK:
                    c['United Kingdom'] += 1
                elif country in area_Netherladns:
                    c['Netherlands'] += 1
                elif country in area_Canada:
                    c['Canada'] += 1
                elif country in area_Australia:
                    c['Australia'] += 1
                elif country in area_Korea:
                    c["Korea"] += 1
                elif country in area_Brazil:
                    c['Brazil'] += 1
                elif country in area_China:
                    c["China"] += 1
                elif country in area_France:
                    c["France"] += 1
                elif country in area_Spain:
                    c['Spain'] += 1
                elif country in area_United_Arab_Emirates:
                    c['United_Arab_Emirates'] += 1
                elif country in area_Turkey:
                    c['Turkey'] += 1
                elif country in area_Italy:
                    c['Italy'] += 1
                else:
                    c[country] += 1
            else:
                area = location[0].split(',')[0].strip()
                if area in area_USA:
                    c['United States'] += 1
                elif area in area_UK:
                    c['United Kingdom'] += 1
                elif area in area_Netherladns:
                    c['Netherlands'] += 1
                elif area in area_Canada:
                    c['Canada'] += 1
                elif area in area_Australia:
                    c['Australia'] += 1
                elif area in area_Korea:
                    c["Korea"] += 1
                elif area in area_Brazil:
                    c['Brazil'] += 1
                elif area in area_China:
                    c["China"] += 1
                elif area in area_France:
                    c["France"] += 1
                elif area in area_Spain:
                    c['Spain'] += 1
                elif area in area_United_Arab_Emirates:
                    c['United_Arab_Emirates'] += 1
                elif area in area_Turkey:
                    c['Turkey'] += 1
                elif area in area_Italy:
                    c['Italy'] += 1
                else:
                    c[area] += 1

        for k, v in c.most_common(100):
            location_key.append(k)
            location_value.append(v/10)

        world_map = Map("世界各国喜爱出行旅游的程度(前100)", width=1200, height=600)
        world_map.add("", location_key, location_value, maptype="world", is_visualmap=True, visual_text_color="#000", is_map_symbol_show=False,)
        print('Generated a world map done!')
        print('*' * 20, 'End Analysis', '*' * 20)

        world_map.render("Tripadvisor_world.html")

    def china_analysis(self):
        """分析我国的人们喜欢去Top25中的哪个国家"""
        cursor = self.collection.find({"userlocation": {"$elemMatch": {"$in": ["China", "Hong Kong", "Taiwan", "Macau"]}}}, {"hotel_location": 1, "userlocation": 1, "_id": 0})
        # cursor = self.collection.find({"userlocation": {"$elemMatch": {"$in": ["London", "london"]}}}, {"hotel_location": 1, "userlocation": 1, "_id": 0})
        country_key = []
        country_value = []
        country_list = [item.get('hotel_location').split('-')[1] for item in cursor]
        c = Counter()
        for country in country_list:
            c[country] += 1
        for k, v in c.most_common(100):
            country_key.append(k)
            country_value.append(v)

        world_map = Map("中国人们喜欢去Top25的哪个国家", width=1200, height=600)
        world_map.add("", country_key, country_value, maptype="world", is_visualmap=True, visual_text_color="#000",
                      is_map_symbol_show=False, )
        print('Generated a world map done!')
        print('*' * 20, 'End Analysis', '*' * 20)

        world_map.render("Tripadvisor_Chinese.html")

if __name__ == '__main__':
    analysis = DataAnalysis()
    analysis.run()



























