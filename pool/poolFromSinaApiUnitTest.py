# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromSinaApiUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-07 20:03
# Description: unit test for pool
# ==============================================================================
import sys, datetime
from poolFromSinaApi import poolFromSinaApi
sys.path.append("../common/")
import unittest
import MarketData
from tradingUnit import tradingUnit
sys.path.append("../tool")
from Log import Log
sys.path.append("../fetch_data")
from marketDataGetter import marketDataGetter
from repo import repo
from tradingRecordSaver import tradingRecordSaver

class mockMarketDataGetter:
    def __init__(self):
        return

    def get_data(self, stockId):
        testList = ['600000', '16.320', '16.320', '16.190', '16.330', '16.140', '16.190', '16.200', '11499190', '186428629.000', '1000', '16.190', '2000', '16.180', '3000', '16.170', '4000', '16.160', '5000', '16.150', '1000', '16.200', '2000', '16.210', '3000', '16.220', '4000', '16.230', '5000', '16.240', '"2016-12-22"', '"15:00:00"']
        return testList

class poolFromSinaApiUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_get_market_trading_data_realtime(self):
        dataGetter = marketDataGetter() 
        pool = poolFromSinaApi(dataGetter, True)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.ALL_PRICE_ORDER 
        amount = 1000
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        marketData = pool.get_market_trading_data(testTradingUnit)
        self.log.info("final market data: " + str(marketData))

    def test_get_market_trading_data_not_realtime(self):
        dataGetter = repo(False, True , None, "algotrading", "12345678", None)
        pool = poolFromSinaApi(dataGetter, False)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.ALL_PRICE_ORDER 
        amount = 1000
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        marketData = pool.get_market_trading_data(testTradingUnit)
        self.log.info("final market data: " + str(marketData))
        self.assertEqual(marketData.time, time)

    def test_trade_first_price_order(self):
        dataGetter = mockMarketDataGetter()
        pool = poolFromSinaApi(dataGetter, True)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.FIRST_PRICE_ORDER 
        amount = 500
        # 未超过界限
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_first_price_order(testTradingUnit)
        self.assertEqual(succAmount, amount)
        amount = 1200
        # 超过界限
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_first_price_order(testTradingUnit)
        self.assertEqual(succAmount, 1000)

    def test_trade_all_price_order(self):
        dataGetter = mockMarketDataGetter()
        pool = poolFromSinaApi(dataGetter, True)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.ALL_PRICE_ORDER 
        amount = 500
        # 未超过界限
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_all_price_order(testTradingUnit)
        self.assertEqual(succAmount, amount)
        amount = 1200
        # 超过第一界限
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_all_price_order(testTradingUnit)
        self.assertEqual(succAmount, 1200)
        self.assertEqual(int(succMoney), int(1000*16.20 + 200*16.21))

        # 超过第5界限
        amount = 120000
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_all_price_order(testTradingUnit)
        self.assertEqual(succAmount, 1000 + 2000 + 3000 + 4000 + 5000)
        self.assertEqual(int(succMoney), int(1000*16.20 + 2000*16.21 + 3000*16.22 + 4000*16.23 + 5000* 16.24))

        buysell = tradingUnit.SELL
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        succAmount, succMoney = pool.trade_all_price_order(testTradingUnit)
        self.assertEqual(succAmount, 1000 + 2000 + 3000 + 4000 + 5000)
        self.assertEqual(int(succMoney), int(1000*16.19 + 2000*16.18 + 3000*16.17 + 4000*16.16 + 5000* 16.15))


    def test_trade_limit_price_order(self):
        dataGetter = mockMarketDataGetter()
        pool = poolFromSinaApi(dataGetter, True)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.FIRST_PRICE_ORDER 
        amount = 500
        expectPrice = 10
        # 未超过界限
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount, expectPrice)
        succAmount, succMoney = pool.trade_limited_price_order(testTradingUnit)
        self.assertEqual(succAmount, 0)
        amount = 1200
        # 超过界限
        expectPrice = 17
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount, expectPrice)
        succAmount, succMoney = pool.trade_limited_price_order(testTradingUnit)
        self.assertEqual(succAmount, 1000)

    def test_trade_order_sync(self):
        dataGetter = mockMarketDataGetter()
        pool = poolFromSinaApi(dataGetter, True)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.FIRST_PRICE_ORDER 
        amount = 500
        # 未超过界限
        self.log.info("expect see into first price order")
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        ansTradingUnit = pool.trade_order_sync(testTradingUnit)

        self.log.info("expect see into all price order")
        tradingType = tradingUnit.ALL_PRICE_ORDER
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        ansTradingUnit = pool.trade_order_sync(testTradingUnit)

        self.log.info("expect see into limit price order")
        tradingType = tradingUnit.LIMITE_PRICE_ORDER
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount, 20)
        ansTradingUnit = pool.trade_order_sync(testTradingUnit)



    def test_trade_order_sync_with_pool(self):
        dataGetter = mockMarketDataGetter()
        saver = tradingRecordSaver("algotrading", "12345678", None)
        pool = poolFromSinaApi(dataGetter, True, saver)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.FIRST_PRICE_ORDER 
        amount = 500
        # 未超过界限
        self.log.info("expect see into first price order")
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)
        lengthBefore = len(saver.get_history_record())
        ansTradingUnit = pool.trade_order_sync(testTradingUnit)
        lengthAfter = len(saver.get_history_record())
        self.assertEqual(lengthBefore, lengthAfter - 1)







if __name__ == "__main__":
    unittest.main()









