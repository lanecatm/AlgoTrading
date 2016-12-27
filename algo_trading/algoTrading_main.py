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
def history_pool(startTime, endTime, findLastDays = 7, isOpenLog = False):

    # 初始化algotrading的repo
    rat = repoForAT("algotrading", "12345678", None, isOpenLog = isOpenLog)

    # 初始化pool
    poolDataMarketGetter = marketDataGetter(isOpenLog = isOpenLog)
    poolDataRepoGetter = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
    poolRecordSaver = tradingRecordSaver("algotrading", "12345678", None, isOpenLog = isOpenLog)
    poolRealTime = poolFromSinaApi(poolDataMarketGetter, True, poolRecordSaver, isOpenLog = isOpenLog)
    poolHistory = poolFromSinaApi(poolDataRepoGetter, False, poolRecordSaver, isOpenLog = isOpenLog)
    
    # 初始化quantAnalysisDict
    repoForQuantAnalysis = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
    quantAnalysisDict = {}
    quantAnalysisDict[clientOrder.TWAP] = TWAPQuantAnalysis(isOpenLog = isOpenLog)
    quantAnalysisDict[clientOrder.VWAP] = VWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
    quantAnalysisDict[clientOrder.LINEARVWAP] = LinearVWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
 

    algoTradingEngine = algoTrading( rat, poolHistory, quantAnalysisDict, findLastDays, isOpenLog = isOpenLog)

    log.info("init succ")

    index = 0
    while(startTime < endTime):
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
    history_pool()

