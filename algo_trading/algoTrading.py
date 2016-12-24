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

    def trade_request(self):
        self.trading_orders = rat.extract_trading_orders(datetime.datetime.now())
        for order in self.trading_orders:
            # Trade and update updateTimeInterval
            pass

    def refresh(self):
        self.refresh_orders = rat.extract_refresh_orders(datetime.datetime.now())
        for order in self.refresh_orders:
            order.updateTime = datetime.datetime.now()
            order.nextUpdateTime = order.updateTime + datetime.timedelta(minutes = order.updateTimeInterval)
            order.tradeTime = datetime.fromtimestamp(order.updateTime.timestamp()+)
                


            
