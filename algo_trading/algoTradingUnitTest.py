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
from algoTrading import AlgoTrading
sys.path.append("../common")
from clientOrder import clientOrder
from tradingUnit import tradingUnit
sys.path.append("../tool/")
from Log import Log

class MockPool():
    def __init__(self):
        self.log = Log()
        self.firstTime = 0
        self.allTime = 0

    def trade_order_sync(self, tradingUnitOrder):
        if tradingUnitOrder.tradingTpye == tradingUnit.ALL_PRICE_ORDER:
            self.allTime = self.allTime + 1
        if tradingUnitOrder.tradingType == tradingUnit.FIRST_PRICE_ORDER:
            self.firstTime = self.firstTime + 1
    def refresh(self):
        self.firstTime = 0
        self.allTime = 0


class MockQuantAnalysis():
    def __init__(self):
        self.log = Log()
        self.callTimes = 0
        self.startTimeList = []
        self.endTimeList = []

    def get_recommend_order_weight(self, stockId, startTime, endTime, findLastDays):
        self.callTimes = self.callTimes + 1
        return
    def refresh(self):
        self.callTimes = 0
        self.startTimeList = []
        self.endTimeList = []


class MockRepoFroAT():
    def __init__(self):
        self.log = Log()
        self.callUninitTime = 0
        self.callRefreshTime = 0
        self.callTradingTime = 0
        self.callCompleteTime = 0
        self.callSaveQA = 0
        self.callPostTrade = 0
        self.callPostSchedule = 0
        self.callCompleteTrade = 0
        self.saveQAList = []
        self.completeOrderNowTimeMinuteList = []

    def refresh(self):
        self.callUninitTime = 0
        self.callRefreshTime = 0
        self.callTradingTime = 0
        self.callCompleteTime = 0
        self.callSaveQA = 0
        self.callPostTrade = 0
        self.callPostSchedule = 0
        self.callCompleteTrade = 0
        self.saveQAList = []
        self.completeOrderNowTimeMinuteList = []



    def extract_uninit_orders(self):
        self.callUninitTime = self.callUninitTime + 1
        returnOrderList = []
        stockId = 600000
        startTime = datetime.datetime(2016,12,25,12,12,12)
        endTime = datetime.datetime(2016, 12, 26, 12, 12, 12)
        stockAmount = 1
        buysell = tradingUnit.BUY
        algChoice = clientOrder.TWAP
        processId = 1
        tradingType = 1
        order1 = clientOrder()
        order1.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        returnOrderList.append(order1)

        algChoice = clientOrder.VWAP
        stockAmount = 2
        order2 = clientOrder()
        order2.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        returnOrderList.append(order2)
        
        algChoice = clientOrder.LINEARVWAP
        stockAmount = 3
        order3 = clientOrder()
        order3.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        returnOrderList.append(order3)

        algChoice = clientOrder.VWAP
        stockAmount = 4
        order4 = clientOrder()
        order4.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        returnOrderList.append(order4)
        return returnOrderList

    def extract_trading_orders(self, nowTime):
        self.callTradingTime = self.callTradingTime + 1
        stockId = 600000
        startTime = datetime.datetime(2016,12,25,12,12,12)
        endTime = datetime.datetime(2016, 12, 26, 12, 12, 12)
        stockAmount = 1
        buysell = tradingUnit.BUY
        algChoice = clientOrder.TWAP
        processId = 1
        tradingType = 1
        order1 = clientOrder()
        order1.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        order1.orderId = 10
        order1.init_order({"2016-12-25 12:00:00": 0.1, "2016-12-25 12:01:00": 0.2,"2016-12-25 12:02:00": 0.4,"2016-12-25 12:03:00": 0.9,"2016-12-25 12:04:00": 0.95,"2016-12-25 12:05:00": 1.0})


        return

    def extract_refresh_orders(self, nowTime):
        self.callRefreshTime = self.callRefreshTime + 1
        return

    def extract_completed_orders(self, nowTime):
        self.callCompleteTime = self.callCompleteTime + 1
        returnList = []
        stockId = 600000
        startTime = nowTime
        endTime = nowTime
        stockAmount = 1
        buysell = tradingUnit.BUY
        algChoice = clientOrder.TWAP
        processId = 1
        tradingType = 1
        order1 = clientOrder()
        order1.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        # orderId是时间分钟
        order1.orderId = nowTime.minute
        returnList.append(order1)
        order2 = clientOrder()
        order2.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        order2.orderId = nowTime.minute
        returnList.append(order2)
        return returnList

    def save_qa_result(self, orderId, quantanalysis, timeInterval = 1):
        self.callSaveQA = self.callSaveQA + 1
        return

    def post_trade(self, orderId, completed_amount, turnover):
        self.callPostTrade = self.callPostTrade + 1
        return

    def post_schedule(self, orderId, updateTime, nextUpdateTime, timeInterval, tradeTime):
        self.callPostSchedule = self.callPostSchedule + 1
        return

    def complete_trade(self, orderId):
        self.callCompleteTrade = self.callCompleteTrade + 1
        self.completeOrderNowTimeMinuteList.append(orderId)
        return



class algoTradingUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def new_algoTrading(self):
        self.rat = MockRepoFroAT()
        self.pool = MockPool()
        self.quantAnalysisTWAP = MockQuantAnalysis()
        self.quantAnalysisVWAP = MockQuantAnalysis()
        self.quantAnalysisLinearVWAP = MockQuantAnalysis()
        findLastdays = 7
        quantAnalysisDict = {}
        quantAnalysisDict[clientOrder.TWAP] = self.quantAnalysisTWAP
        quantAnalysisDict[clientOrder.VWAP] = self.quantAnalysisVWAP
        quantAnalysisDict[clientOrder.LINEARVWAP] = self.quantAnalysisLinearVWAP
        at = AlgoTrading(self.rat, self.pool, quantAnalysisDict, findLastdays)
        return at

    def refresh(self):
        self.rat.refresh()
        self.pool.refresh()
        self.quantAnalysisTWAP.refresh()
        self.quantAnalysisVWAP.refresh()
        self.quantAnalysisLinearVWAP.refresh()


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

    def test_init(self):
        algoTrading = self.new_algoTrading()


    def test_erase_seconds(self):
        algoTradingEngine = self.new_algoTrading()
        time1 = datetime.datetime(2016, 12, 12, 1, 34, 22, 22)
        time2 = datetime.datetime(2016, 12, 12, 1, 34, 00, 51)
        newTime1 = algoTradingEngine.erase_seconds(time1)
        newTime2 = algoTradingEngine.erase_seconds(time2)
        self.assertEquals(newTime1, newTime2)
        self.assertEquals(type(time1), type(newTime1))

    def test_random_trading_time(self):
        algoTradingEngine = self.new_algoTrading()
        time1 = datetime.datetime(2016, 12, 12, 1, 34, 22)
        time2 = datetime.datetime(2016, 12, 12, 1, 38, 00)
        for i in range(1000):
            randomTime = algoTradingEngine.random_trading_time(time1, 10)
            self.assertLessEqual(time1, randomTime)
            self.assertGreater(time1 + datetime.timedelta(minutes = 10), randomTime)
            #self.log.info("random time:" + str(randomTime))

    def test_set_time(self):
        algoTradingEngine = self.new_algoTrading()
        initDate = datetime.datetime(2016, 12, 12, 12, 8)
        ans = algoTradingEngine.set_time(initDate)
        self.assertTrue(ans)
        ans = algoTradingEngine.set_time(initDate)
        self.assertFalse(ans)
        ans = algoTradingEngine.set_time(initDate + datetime.timedelta(seconds = 10))
        self.assertTrue(ans)
        ans = algoTradingEngine.set_time(initDate)
        self.assertFalse(ans)


    def test_init_orders(self):
        algoTradingEngine = self.new_algoTrading()
        algoTradingEngine.init_orders()
        # 读出不同的TWAP和VWAP结果 共4条
        # 调用save_qa_result 共4条
        self.assertEquals(self.quantAnalysisTWAP.callTimes, 1)
        self.assertEquals(self.quantAnalysisVWAP.callTimes, 2)
        self.assertEquals(self.quantAnalysisLinearVWAP.callTimes, 1)



    def test_complete_orders(self):
        algoTradingEngine = self.new_algoTrading()
        nowTime = datetime.datetime(2016, 12, 24, 12, 12, 00)
        algoTradingEngine.set_time(nowTime)
        algoTradingEngine.complete_orders()
        self.assertEquals(self.rat.callCompleteTime, 1)
        self.assertEquals(self.rat.callCompleteTrade, 2)
        self.assertEquals(self.rat.completeOrderNowTimeMinuteList[0], nowTime.minute)

        nowTime = datetime.datetime(2016, 12, 24, 12, 13, 00)
        algoTradingEngine.set_time(nowTime)
        algoTradingEngine.complete_orders()
        self.assertEquals(self.rat.callCompleteTime, 2)
        self.assertEquals(self.rat.callCompleteTrade, 4)
        self.assertEquals(self.rat.completeOrderNowTimeMinuteList[3], nowTime.minute)

    def test_trade_request(self):
        algoTradingEngine = self.new_algoTrading()
        nowTime = datetime.datetime(2016, 12, 24, 12, 12, 00)
        algoTradingEngine.set_time(nowTime)
        
        pass

    def test_refresh(self):
        pass

if __name__ == '__main__':
    unittest.main()
