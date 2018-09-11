# -*- coding: utf-8 -*-
from db import db
from wordCloud import WordCloudGet

import sys

def get_wechatNos():
    conn = db()
    wechatNos = conn.select_by_sql_all('select wechatNo from friendinfo')
    return set(wechatNos)

def do_cloud():

    for wechatNo in get_wechatNos():
        print(wechatNo)
        conn = db()
        contents = conn.select_by_sql_all("select contents from wechat where wechatNo = '"+wechatNo[0]+"'")
        print(len(contents))
        contentResult = ''
        for content in contents:
            print('add content')
            contentResult += content[0]
        if contentResult != '':
            print("正在生成{}的词云".format(wechatNo[0]))
            WordCloudGet(wechatNo[0]).wordcloud(contentResult)
