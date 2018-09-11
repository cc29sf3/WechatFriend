# -*- coding: utf-8 -*-
from program import do_cloud
from scrapy import Moments

## 启动爬虫
try:
    moments = Moments()
    moments.main()
except Exception as e:
    print(e)
    pass
finally:
    ## 启动制作云图
    do_cloud()
