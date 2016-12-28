# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoForATUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-24 16:21
# Description: repoForAT 单元测试
# ==============================================================================
import sys
import time
import datetime
import unittest
from repoForAT import repoForAT
sys.path.append("../common/")
from clientOrder import clientOrder
sys.path.append("../tool")
from Log import Log

class repoForATUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def new_order(self):
        orderInfo = clientOrder()
        stockId = 600000
        startTime = datetime.datetime(2016, 12, 11, 10, 00)
        endTime = datetime.datetime(2016, 12, 12, 11, 00)
        stockAmount = 10
        buysell = 10
        algChoice = 10
        processId = 1
        tradingType = 1
        orderInfo.create_order(stockId, startTime, endTime, stockAmount, buysell, algChoice, processId, tradingType)
        return orderInfo

    def test_insert_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)

    def test_delete_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        orderId = 1
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        repo.delete_order(1)

    def test_delete_all_orders(self):
        repo = repoForAT("algotrading", "12345678", None)
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        repo.insert_order(orderInfo)
        repo.delete_all_orders()


    def test_extract_uninit_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        originList = repo.extract_uninit_orders()

        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        newList = repo.extract_uninit_orders()

        self.assertEqual(len(originList), len(newList) - 1)

        originList = newList
        dictTest = {1:2}
        orderInfo.init_order(dictTest)
        repo.insert_order(orderInfo)
        orderInfo.status = clientOrder.COMPLETED
        repo.insert_order(orderInfo)

        newList = repo.extract_uninit_orders()
        self.assertEqual(len(originList), len(newList))

    def test_extract_trading_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        originList = repo.extract_trading_orders(datetime.datetime(2016,12,11,12))
        originListSmallTime = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 9))

        # 插入status为0的order
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        newList = repo.extract_trading_orders(datetime.datetime(2016,12,11,12))

        self.assertEqual(len(originList), len(newList))

        # 插入状态为1的order
        originList = newList
        dictTest = {1:2}
        orderInfo.init_order(dictTest)
        orderInfo.tradeTime = datetime.datetime(2016, 12, 11, 11, 30)
        repo.insert_order(orderInfo)

        newList = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 12))
        self.assertEqual(len(originList), len(newList) - 1)

        newListSmallTime = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 9))
        self.assertEqual(len(originListSmallTime), len(newListSmallTime))

        # 插入状态为2的order
        originList = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 12))
        orderInfo.status = clientOrder.COMPLETED
        repo.insert_order(orderInfo)
        newList = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 12))
        self.assertEqual(len(originList), len(newList))

    def test_extract_refresh_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        originList = repo.extract_refresh_orders(datetime.datetime(2016,12,11,12))
        originListSmallTime = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 9))

        # 插入status为0的order
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        newList = repo.extract_refresh_orders(datetime.datetime(2016,12,11,12))

        self.assertEqual(len(originList), len(newList))

        # 插入状态为1的order
        originList = newList
        dictTest = {1:2}
        orderInfo.init_order(dictTest)
        repo.insert_order(orderInfo)

        newList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 12))
        self.assertEqual(len(originList), len(newList) - 1)

        newListSmallTime = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 9))
        self.assertEqual(len(originListSmallTime), len(newListSmallTime))

        # 插入状态为2的order
        originList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 12))
        orderInfo.status = clientOrder.COMPLETED
        repo.insert_order(orderInfo)
        newList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 12))
        self.assertEqual(len(originList), len(newList))

    def test_extract_completed_order(self):
        repo = repoForAT("algotrading", "12345678", None)
        originList = repo.extract_completed_orders(datetime.datetime(2016,12,13))
        originListSmallTime = repo.extract_completed_orders(datetime.datetime(2016, 12, 12, 9))

        # 插入status为0的order
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)
        newList = repo.extract_completed_orders(datetime.datetime(2016,12,12,9))

        self.assertEqual(len(originListSmallTime), len(newList))

        # 插入状态为1的order
        dictTest = {1:2}
        orderInfo.init_order(dictTest)
        repo.insert_order(orderInfo)

        newList = repo.extract_completed_orders(datetime.datetime(2016, 12, 13))
        self.assertEqual(len(originList), len(newList) - 1)

        newListSmallTime = repo.extract_completed_orders(datetime.datetime(2016, 12, 12, 9))
        self.assertEqual(len(originListSmallTime), len(newListSmallTime))

        # 插入状态为2的order
        originList = repo.extract_completed_orders(datetime.datetime(2016, 12, 13))
        orderInfo.status = clientOrder.COMPLETED
        repo.insert_order(orderInfo)
        newList = repo.extract_completed_orders(datetime.datetime(2016, 12, 13))
        self.assertEqual(len(originList), len(newList))

    def test_save_qa_result(self):
        repo = repoForAT("algotrading", "12345678", None)
        # 2016-12-11 10:00
        # 2016-12-12 11:00

        # 插入order
        orderInfo = self.new_order()
        repo.insert_order(orderInfo)

        refreshOrderListBefore = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 10, 00))
        refreshOrderListBefore2 = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 12, 01))
        refreshOrderListBefore3 = repo.extract_refresh_orders(datetime.datetime(2016, 12, 13))
        # order init
        initOrderList = repo.extract_uninit_orders()
        for order in initOrderList:
            orderId = order.orderId 
            quantAnalysisDict = {1:10}
            timeInterval = 2
            repo.save_qa_result(orderId, quantAnalysisDict, timeInterval)

        # 获取更新的列表
        refreshOrderList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 10, 00))
        self.assertEqual(len(refreshOrderListBefore) + len(initOrderList), len(refreshOrderList))
        refreshOrderList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 10, 01))
        self.assertEqual(len(refreshOrderListBefore) + len(initOrderList), len(refreshOrderList))
        # 更新列表
        for order in refreshOrderList:
            self.log.info("refresh order:" + str(order))
            orderId = order.orderId
            updateTime = order.nextUpdateTime           
            nextUpdateTime = datetime.datetime(2016, 12, 11, 12, 00)
            for tmpOrder in initOrderList:
                if orderId == tmpOrder.orderId:
                    self.assertEqual(order.updateTimeInterval, 2)
            timeInterval = 12
            tradeTime = datetime.datetime(2016, 12, 11, 11, 30)
            repo.post_schedule(orderId, updateTime, nextUpdateTime, timeInterval, tradeTime)

        # 寻找待交易列表
        tradingList = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 11, 30))
        for order in tradingList:
            self.assertEqual(12, order.updateTimeInterval)
            orderId = order.orderId
            completed_amount = 10
            turnover = 10
            repo.post_trade(orderId, completed_amount, turnover)
        tradingList = repo.extract_trading_orders(datetime.datetime(2016, 12, 11, 11, 31))
        self.assertEqual(0, len(tradingList))

        refreshOrderList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 11, 40))
        self.assertEqual(0, len(refreshOrderList))
        for order in refreshOrderList:
            self.assertEqual(10, order.completedAmount)
            self.assertEqual(10, order.trunOver)
        
        # 第二次更新列表
        refreshOrderList = repo.extract_refresh_orders(datetime.datetime(2016, 12, 11, 12, 01))
        self.assertEqual(len(initOrderList) + len(refreshOrderListBefore2), len(refreshOrderList))

        # 完成列表
        completeOrderList = repo.extract_completed_orders(datetime.datetime(2016, 12, 13))
        self.assertEqual(len(completeOrderList), len(refreshOrderListBefore3) + len(initOrderList))
        for order in completeOrderList:
            repo.complete_trade(order.orderId)







if __name__ == '__main__':
    unittest.main()

