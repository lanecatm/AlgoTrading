# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: algoTradingItegrationTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-26 21:38
# Description: algotrading 集成测试
# ==============================================================================
import sys
import datetime
import random

from algoTrading import algoTrading
from repoForAT import repoForAT

sys.path.append("../tool")
from Log import Log

sys.path.append("../common/")
from clientOrder import clientOrder
from tradingUnit import tradingUnit

sys.path.append("../quant_analysis")
from TWAPQuantAnalysis import TWAPQuantAnalysis
from VWAPQuantAnalysis import VWAPQuantAnalysis
from LinearVWAPQuantAnalysis import LinearVWAPQuantAnalysis

sys.path.append("../pool")
from poolFromSinaApi import poolFromSinaApi
from tradingRecordSaver import tradingRecordSaver

sys.path.append("../fetch_data")
from marketDataGetter import marketDataGetter
from repo import repo


log = Log()
def test_history_pool():

    # 初始化algotrading的repo
    rat = repoForAT("algotrading", "12345678", None, isOpenLog = False)

    # 初始化pool
    poolDataMarketGetter = marketDataGetter(isOpenLog = False)
    poolDataRepoGetter = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = False)
    poolRecordSaver = tradingRecordSaver("algotrading", "12345678", None, isOpenLog = False)
    poolRealTime = poolFromSinaApi(poolDataMarketGetter, True, poolRecordSaver, isOpenLog = False)
    poolHistory = poolFromSinaApi(poolDataRepoGetter, False, poolRecordSaver, isOpenLog = False)
    
    # 初始化quantAnalysisDict
    repoForQuantAnalysis = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = False)
    quantAnalysisDict = {}
    quantAnalysisDict[clientOrder.TWAP] = TWAPQuantAnalysis(isOpenLog = False)
    quantAnalysisDict[clientOrder.VWAP] = VWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = False)
    quantAnalysisDict[clientOrder.LINEARVWAP] = LinearVWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = False)
 

    findLastDays = 7
    algoTradingEngine = algoTrading( rat, poolHistory, quantAnalysisDict, findLastDays, isOpenLog = False)

    log.info("init succ")

    order1 = clientOrder()
    stockId = 601377
    startTime = datetime.datetime(2016, 12, 23, 10, 00)
    endTime = datetime.datetime(2016, 12, 23, 14, 00)
    stockAmount = 10000
    buysell = 0
    algChoice = 1
    processId = 1
    tradingType = 1
    order1.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
    rat.insert_order(order1)

    order2 = clientOrder()
    buysell = 1
    algChoice = 2
    stockAmount = 1000
    startTime = datetime.datetime(2016, 12, 22, 8, 00)
    endTime = datetime.datetime(2016, 12, 23, 19, 00)
    order2.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
    rat.insert_order(order2)

    order3 = clientOrder()
    buysell = 0
    algChoice = 0
    stockAmount = 1000000
    startTime = datetime.datetime(2016, 12, 22, 10, 00)
    endTime = datetime.datetime(2016, 12, 22, 10, 10)
    order3.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
    rat.insert_order(order3)


    startTime = datetime.datetime(2016,12, 22, 8,00 )
    index = 0
    while(startTime < datetime.datetime(2016, 12,23, 22)):
        algoTradingEngine.set_time(startTime)
        startTime = startTime + datetime.timedelta(minutes = 1)
        algoTradingEngine.init_orders()
        algoTradingEngine.refresh()
        algoTradingEngine.trade_request()
        algoTradingEngine.complete_orders()
        index = index + 1
        if index%60 == 0:
            log.info("now time:" + str(startTime))

if __name__ == "__main__":
    test_history_pool()

