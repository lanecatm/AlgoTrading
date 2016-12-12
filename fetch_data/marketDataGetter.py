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

    # old stock id 601006
    def get_data(self, stockId):
        #self.log.info("get_data(), input stock id" + stockId)
        url = 'http://hq.sinajs.cn/list=sh' + stockId
        #self.log.info("request url: " + url)
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        #self.log.info("request ans: " + res)
        #print res
        infoStr = res[res.find('"') + 1: -1]
        infoArr = infoStr.split(',')
        infoArr[0] = '"' + infoArr[0] + '"'
        infoArr[-3] = '"' + infoArr[-3] + '"'
        infoArr[-2] = '"' + infoArr[-2] + '"'

        self.log.info("get data from sina api:\n" + str(infoArr[:-1]))
        return infoArr[:-1]

if __name__=='__main__':

    # sys.argv 命令行参数
    if len(sys.argv) < 3:
        print "param error, marketDataGetter [db name] [stock id 1] ..."
        exit()
    dbName = sys.argv[1]
    stockIdArr = sys.argv[2:]

    getter = marketDataGetter()
    database = repo.repo("./" + dbName)

    for stockId in stockIdArr:
        infoArr = getter.get_data(stockId)
        infoArr[0] = stockId
        database.insert_data(infoArr)
    exit()

