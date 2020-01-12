#!usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
# 运行
execute(('scrapy crawl hw').split())
# execute(('scrapy view https://www.vmall.com').split())
# execute(('scrapy shell https://www.vmall.com').split())
