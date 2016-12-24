import sys
#sys.path.append("../cli/")
sys.path.append("../common/")
import clientOrder
import orderResult
from tradingUnit import tradingUnit
sys.path.append("../quant_analysis")
from TWAPQuantAnalysis import TWAPQuantAnalysis
from VWAPQuantAnalysis import VWAPQuantAnalysis
sys.path.append("../pool")
from poolFromSinaApi import poolFromSinaApi
from marketDataGetter import marketDataGetter
sys.path.append("../fetch_data")
from repoFromTushare import repoFromTushare
sys.path.append("../tool")
from Log import Log

import numpy as np
import MySQLdb
import datetime
import time
import sqlite3

import random
from repoForAT import repoForAT

class AlgoTrading:
    LOW_TRADE_BOUND = 200
    HIGH_TRADE_BOUND = 5000
    LOW_INTERVAL_BOUND = 500
    HIGH_INTERVAL_BOUND = 2000
    SMALL_INTERVAL = 1
    MID_INTERVAL = 2
    LARGE_INTERVAL = 4

    def __init__(self, rat, pool, repoEngine, findLastDays):
        self.log = Log()
        self.rat = rat
        self.pool = pool
        self.repoEngine = repoEngine
        self.findLastDays = findLastDays

    def init_orders(self):
        quantAnalysisTWAP = TWAPQuantAnalysis()
        quantAnalysisVWAP = VWAPQuantAnalysis(self.repoEngine)
        for order in self.rat.extract_uninit_orders():
            if order.algoChoice == 0:
                quantAnalysisDict = quantAnalysisTWAP.get_recommend_order_weight(order.stockAmount,
                                                      order.startTime, order.endTime,
                                                                                 None)
            elif order.algoChoice == 1:
                quantAnalysisDict = quantAnalysisVWAP.get_recommend_order_weight(order.stockAmount,
                                                      order.startTime, order.endTime,
                                                                                 self.findLastDays)
            self.rat.save_qa_result(quantAnalysisDict)





    def trade_request(self):
        self.trading_orders = self.rat.extract_trading_orders(datetime.datetime.now())
        for order in self.trading_orders:
            weight = order.quantAnalysisDict[order.tradeTime]
            amount = (order.stockAmount * weight - order.completedAmount) // 100
            unit = tradingUnit(order.orderId, order.stockId, order.buySell, True,
                               order.tradingType, amount)
            if order.nextUpdateTime <= order.endTime:
                succAmount, succMoney = self.pool.trade_first_price_order(unit)
            else:
                succAmount, succMoney = self.pool.trade_all_price_order(unit)
            self.rat.post_trade(order.completedAmount+succAmount, order.trunOver+succMoney)


    def refresh(self):
        self.refresh_orders = self.rat.extract_refresh_orders(datetime.datetime.now())
        for order in self.refresh_orders:
            # A
            order.updateTime = datetime.datetime.now()
            # B
            order.nextUpdateTime = order.updateTime + datetime.timedelta(minutes = order.updateTimeInterval)
            aboutToTrade = order.quantAnalysisDict[self.erase_seconds(order.nextUpdateTime)] - orders.completedAmount
            # D
            if aboutToTrade < LOW_TRADE_BOUND:
                order.trdeTime = None
            else:
                order.tradeTime = datetime.fromtimestamp(order.updateTime.timestamp() + random.random() * 60 * order.updateTimeInterval)
            # C
            if aboutToTrade < LOW_INTERVAL_BOUND:
                order.updateTimeInterval = SMALL_INTERVAL
            elif aboutToTrade < HIGH_INTERVAL_BOUND:
                order.updateTimeInterval = MID_INTERVAL
            else:
                order.updateTimeInterval = LARGE_INTERVAL

            self.rat.post_schedule(order.orderId, order.updateTime, order.nextUpdateTime, order.updateTimeInterval, order.tradeTime)

    # parameter datetime
    # output datetime in whole minutes
    def erase_seconds(self, t):
        return t - datetime.timedelta(seconds = t.second) - timedate.timedelta(microseconds = t.microsecond)
 


            
