#!usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue
import threading
import requests
from lxml import etree
from pymongo import MongoClient
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""获取代理IP，拼接成代理格式，存数据库"""


class ProxySpider(object):
    def __init__(self):
        self.url = "https://www.xicidaili.com/nn/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        self.client = MongoClient('localhost', 27017)
        self.collection = self.client['all_ip']['xicidaili']
        self.html_queue = Queue()
        self.ip_queue = Queue()
        self.pack_queue = Queue()

    # 请求地址
    def parse_url(self):
        response = requests.get(self.url, headers=self.headers, verify=False)
        html_str = etree.HTML(response.content.decode())
        self.html_queue.put(html_str)

    # 获取IP
    def get_ip_list(self):
        ips = list()
        html_str = self.html_queue.get()
        html_node = html_str.xpath("//table[@id='ip_list']//tr")[1:]
        for temp in html_node:
            ip_item = dict()
            ip_item["ip"] = temp.xpath("./td[2]/text()")[0]
            ip_item["port"] = temp.xpath("./td[3]/text()")[0]
            ips.append(ip_item)
        self.ip_queue.put(ips)
        self.html_queue.task_done()

    # 处理IP
    def pack_ip(self):
        res = self.ip_queue.get()
        # with open("ip.json", 'w', encoding="utf-8") as f:
        #     f.write(json.dumps(res, ensure_ascii=False, indent=2))
        ip_pool = list()
        for i in res:
            proxy_ip = {
                "https": "http://" + i["ip"] + ":" + i["port"]
            }
            ip_pool.append(proxy_ip)
        self.pack_queue.put(ip_pool)
        self.ip_queue.task_done()

    def multiple(self):
        thread_list = list()
        t_url = threading.Thread(target=self.parse_url)
        thread_list.append(t_url)
        t_ip = threading.Thread(target=self.get_ip_list)
        thread_list.append(t_ip)
        t_pick_ip = threading.Thread(target=self.pack_ip)
        thread_list.append(t_pick_ip)
        for t in thread_list:
            # 把子线程设置为守护线程,主线程结束，子线程结束
            t.setDaemon(True)
            t.start()

        for q in [self.html_queue, self.ip_queue, self.pack_queue]:
            q.join()

    def run(self):
        self.multiple()
        ret = self.pack_queue.get()
        self.pack_queue.task_done()
        self.collection.drop()
        for i in ret:
            self.collection.insert(dict(i))
            print(i)


if __name__ == '__main__':
    ps = ProxySpider()
    ps.run()
