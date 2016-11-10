# -*- coding:utf-8 -*-
import urllib2
import json
import repo
import sys
sys.path.append("../tool")
from Log import Log
class marketDataGetter:
    def __init__(self):
        self.log = Log()
        return

    def get_data(self):
        url = 'http://hq.sinajs.cn/list=sh601006'
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #print res
        infoStr = res[res.find('"') + 1: -1]
        infoArr = infoStr.split(',')
        infoArr[0] = '"' + infoArr[0] + '"'
        infoArr[-3] = '"' + infoArr[-3] + '"'
        infoArr[-2] = '"' + infoArr[-2] + '"'

        self.log.info("get data from sina api:\n" + str(infoArr[:-1]))
        return infoArr[:-1]

if __name__=='__main__':
    getter = marketDataGetter()
    infoArr = getter.get_data()
    database = repo.repo("./again.db")
    database.insert_data(infoArr)
    exit()

