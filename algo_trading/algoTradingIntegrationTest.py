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
    rat = repoForAT("algotrading", "12345678", None, isOpenLog = True)

    # 初始化pool
    poolDataMarketGetter = marketDataGetter()
    poolDataRepoGetter = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = False)
    poolRecordSaver = tradingRecordSaver("algotrading", "12345678", None)
    poolRealTime = poolFromSinaApi(poolDataMarketGetter, True, poolRecordSaver)
    poolHistory = poolFromSinaApi(poolDataRepoGetter, False, poolRecordSaver)
    
    # 初始化quantAnalysisDict
    repoForQuantAnalysis = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = False)
    quantAnalysisDict = {}
    quantAnalysisDict[clientOrder.TWAP] = TWAPQuantAnalysis()
    quantAnalysisDict[clientOrder.VWAP] = VWAPQuantAnalysis(repoForQuantAnalysis)
    quantAnalysisDict[clientOrder.LINEARVWAP] = LinearVWAPQuantAnalysis(repoForQuantAnalysis)
 

    findLastDays = 7
    algoTradingEngine = algoTrading( rat, poolHistory, quantAnalysisDict, findLastDays)

    log.info("init succ")

    order1 = clientOrder()
    stockId = 600000
    startTime = datetime.datetime(2016, 12, 23, 10, 00)
    endTime = datetime.datetime(2016, 12, 23, 14, 00)
    stockAmount = 10000
    buysell = 0
    algChoice = 1
    processId = 1
    tradingType = 1
    order1.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
    rat.insert_order(order1)


    startTime = datetime.datetime(2016,12, 23, 9,30 )
    for i in range(1000):
        algoTradingEngine.set_time(startTime)
        startTime = startTime + datetime.timedelta(minutes = 1)
        algoTradingEngine.init_orders()
        algoTradingEngine.refresh()
        algoTradingEngine.trade_request()
        algoTradingEngine.complete_orders()

if __name__ == "__main__":
    test_history_pool()

