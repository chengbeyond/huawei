#!usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""美团火锅热门店抓取"""


class MeiTuanSpider(object):
    def __init__(self):
        self.url = "http://meishi.meituan.com/i/api/channel/deal/list"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Cookie": "_lxsdk_cuid=167ad0c4df5c8-0fe58d829fcfa1-6313363-1fa400-167ad0c4df5c8; ci=59; rvct=59; uuid=38ecf2f29b3c4009a3df.1544965376.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; IJSESSIONID=joi9baun21q6dbk5kz38evwa; iuuid=8F1EB0299DA1CB1B2284A52EA762737AF096B16249F0AD5C8968CD75832AE095; cityname=%E6%88%90%E9%83%BD; _lxsdk=8F1EB0299DA1CB1B2284A52EA762737AF096B16249F0AD5C8968CD75832AE095; __utma=74597006.1146495771.1544965403.1544965403.1544965403.1; __utmc=74597006; __utmz=74597006.1544965403.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); latlng=30.67485,104.06291,1544965403276; ci3=1; __utmb=74597006.2.9.1544965406814; i_extend=C_b1Gimthomepagecategory11H__a; client-id=bff49476-2bcc-4ed5-a551-c3b0d74510ab; _hc.v=1f57e029-308d-0b54-e4d6-6ed755d81c0b.1544965417; _lxsdk_s=167b71cd820-092-ebb-5c6%7C%7C18",
            "Referer": "http://meishi.meituan.com/i/?ci=59&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1"
        }

    # 请求地址
    def parse_url(self, num=None):
        data = dict(
            cateId=17,
            limit=15,
            offset=num,
        )

        response = requests.post(self.url, headers=self.headers, data=data, verify=False)
        json_str = response.content.decode()
        return json_str

    # 获取火锅的列表
    def get_hot_list(self, temp):
        hot = json.loads(temp)
        hot_pots = hot["data"]["poiList"]["poiInfos"]
        return hot_pots

    # 处理列表
    def save_item(self, list):
        item_list = []
        for hot in list:
            item = dict()
            item["avgPrice"] = hot["avgPrice"]
            item["avgScore"] = hot["avgScore"]
            item["cateName"] = hot["cateName"]
            item["name"] = hot["name"]
            if len(hot["preferentialInfo"]["maidan"]["entries"]) == 1:
                item["content"] = hot["preferentialInfo"]["maidan"]["entries"][0]["content"]
            elif len(hot["preferentialInfo"]["maidan"]["entries"]) == 2:
                item["content"] = hot["preferentialInfo"]["maidan"]["entries"][0]["content"]
                item["content1"] = hot["preferentialInfo"]["maidan"]["entries"][1]["content"]

            elif len(hot["preferentialInfo"]["maidan"]["entries"]) == 3:
                item["content"] = hot["preferentialInfo"]["maidan"]["entries"][0]["content"]
                item["content1"] = hot["preferentialInfo"]["maidan"]["entries"][1]["content"]
                item["content2"] = hot["preferentialInfo"]["maidan"]["entries"][2]["content"]
            item_list.append(item)
        return item_list

    def run(self):
        pot_list = []
        num = 0
        while True:
            if num == 45:
                break
            temp_list = self.parse_url(num)
            hots_list = self.get_hot_list(temp_list)
            item = self.save_item(hots_list)
            for i in item:
                pot_list.append(i)
            num += 15
        print(json.dumps(pot_list))


if __name__ == "__main__":
    ps = MeiTuanSpider()
    ps.run()
