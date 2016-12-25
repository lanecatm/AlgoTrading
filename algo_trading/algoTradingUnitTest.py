#!/usr/bin/env python
# encoding: utf-8
# Python 2.7

"""
@time: 12/25/16
@description: 
"""
import sys
import time
import datetime
import unittest
from repoForAT import repoForAT
from algoTrading import AlgoTrading
sys.path.append("../fetch_data")
from marketDataGetter import marketDataGetter
sys.path.append("../pool/")
from poolFromSinaApi import poolFromSinaApi
sys.path.append("../quant_analysis")
from TWAPQuantAnalysis import TWAPQuantAnalysis
from VWAPQuantAnalysis import VWAPQuantAnalysis
sys.path.append("../common")
from clientOrder import clientOrder

class repoTest:
    pass

class algoTradingUnitTest(unittest.TestCase):


    def setUp(self):
        self.at = self.new_algoTrading()

    def tearDown(self):
        pass

    def new_algoTrading(self):
        self.rat = repoForAT('algotrading', '12345678', None, None)
        dataGetter = marketDataGetter()
        pool = poolFromSinaApi(dataGetter, True)
        findLastdays = 7
        quantAnalysisTWAP = TWAPQuantAnalysis()
        repoEngine = repoTest()
        quantAnalysisVWAP = VWAPQuantAnalysis(repoEngine)
        at = AlgoTrading(self.rat, pool, repoEngine, findLastdays,
                         quantAnalysisTWAP, quantAnalysisVWAP)
        return at

    def new_order(self):
        orderInfo = clientOrder()
        stockId = 600000
        startTime = datetime.datetime(2016, 12, 11, 10, 00)
        endTime = datetime.datetime(2016, 12, 12, 11, 00)
        stockAmount = 10000
        buysell = 1
        algChoice = 0
        processId = 1
        tradingType = 1
        orderInfo.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        return orderInfo

    def test_init_orders(self):
        order_twap = self.new_order()
        order_vwap = self.new_order()
        order_vwap.algChoice = 1
        self.repo.insert_order(order_twap)
        self.repo.insert_order(order_vwap)
        self.at.init_orders()
        #self.assertEquals(????) #
        # TBD

    def test_complete_orders(self):
        # 这个函数很简单，不用测试
        pass

    def test_trade_request(self):
        # 没有测试数据啊
        pass

    def test_refresh(self):
        pass
