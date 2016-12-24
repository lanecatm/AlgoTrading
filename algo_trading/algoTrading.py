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
# import poolFromSinaApi
from poolFromTushare import poolFromTushare
from tradingRecordRepo import tradingRecordRepo
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
    def __init__(self):
        self.log = Log()
        self.rat = repoForAT()

    def init_orders(self) 

    def trade_request(self):
        self.trading_orders = rat.extract_trading_orders(datetime.datetime.now())
        for order in self.trading_orders:
            # Trade and update updateTimeInterval
            pass

    def refresh(self):
        self.refresh_orders = self.rat.extract_refresh_orders(datetime.datetime.now())
        for order in self.refresh_orders:
            order.updateTime = datetime.datetime.now()
            order.tradeTime = datetime.fromtimestamp(order.updateTime.timestamp() + random.random() * 60 * order.updateTimeInterval)
            order.nextUpdateTime = order.updateTime + datetime.timedelta(minutes = order.updateTimeInterval)
            aboutToTrade = orders.quantAnalysisDict[order.nextUpdateTime - datetime.timedelta(seconds = order.nextUpdateTime.second)]
            if 
            self.rat.post_schedule(order.orderId, order.updateTime, order.nextUpdateTime, order.updateTimeInterval, order.tradeTime)

    # parameter datetime
    # output datetime in whole minutes
    def eraseSeconds(self, )
 


            
