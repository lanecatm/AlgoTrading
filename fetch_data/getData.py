# -*- coding:utf-8 -*-
import urllib2
import json
import repo
def get_data():
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

    print infoArr[:-1]
    return infoArr[:-1]

if __name__=='__main__':
    infoArr = get_data()
    database = repo.repo("./test.db")
    database.insert_data(infoArr)
    exit()

