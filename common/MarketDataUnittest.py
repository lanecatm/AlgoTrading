
# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: MarketDataUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 12:45
# Description: marketdata 单元测试
# ==============================================================================
import datetime
from MarketData import MarketData
import sys
sys.path.append("../fetch_data/")
from repo import repo
from marketDataGetter import marketDataGetter

if __name__=='__main__':
    market = marketDataGetter()
    originArr = market.get_data(600000)
    marketData = MarketData(originArr)
    print marketData.sellPrice
    print marketData.sellAmount
    print marketData.buyPrice
    print marketData.buyAmount
    print marketData.time

    repoEngine = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = False)
    originArr = repoEngine.get_data(600000, datetime.datetime(2016, 12,23,10))
    marketData = MarketData(originArr)
    print marketData.sellPrice
    print marketData.sellAmount
    print marketData.buyPrice
    print marketData.buyAmount
    print marketData.time

