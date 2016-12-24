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
    TRADE_UNIT = 100
    LOW_INTERVAL_BOUND = 200
    HIGH_INTERVAL_BOUND = 1000
    ZOOM = 2

    def __init__(self):
        self.log = Log()
        self.rat = repoForAT()
        self.dataGetter = marketDataGetter()
        self.pool = poolFromSinaApi(self.dataGetter, True)


    def init_orders(self) 

    def trade_request(self):
        self.trading_orders = self.rat.extract_trading_orders(datetime.datetime.now())
        for order in self.trading_orders:
            weight = order.quantAnalysisDict[order.tradeTime]
            amount = order.stockAmount * weight - order.completedAmount
            unit = tradingUnit(order.orderId, order.stockId, order.buySell, True,
                               order.tradingType, amount)
            succAmount, succMoney = self.pool.trade_first_price_order(unit)
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
            if aboutToTrade < TRADE_UNIT:
                order.trdeTime = None
            elif order.nextUpdateTime > order.endTime:
                order.tradeTime = datetime.fromtimestamp(order.updateTime.timestamp() + random.random() * 60 *
            else:
                order.tradeTime = datetime.fromtimestamp(order.updateTime.timestamp() + random.random() * 60 * order.updateTimeInterval)
            # C
            if aboutToTrade <= LOW_INTERVAL_BOUND:
                order.updateTimeInterval = order.updateTimeInterval * ZOOM
            elif aboutToTrade >= HIGH_INTERVAL_BOUND:
                if order.updateTimeInterval > 1:
                    order.updateTimeInterval = order.updateTimeInterval / ZOOM
            

            self.rat.post_schedule(order.orderId, order.updateTime, order.nextUpdateTime, order.updateTimeInterval, order.tradeTime)

    # parameter datetime
    # output datetime in whole minutes
    def erase_seconds(self, t):
        return t - datetime.timedelta(seconds = t.second) - timedate.timedelta(microseconds = t.microsecond)
 


            
