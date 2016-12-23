# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: tradingRecordSaverUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-23 20:56
# Description: unit test for tradingRecordSaver
# ==============================================================================
import sys, datetime
import unittest
from tradingRecordSaver import tradingRecordSaver
sys.path.append("../common/")
from tradingUnit import tradingUnit
sys.path.append("../tool")
from Log import Log

class tradingRecordSaverUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_save_reocrd(self):
        saver = tradingRecordSaver("algotrading", "12345678", None)
        tradingUnitId = 1
        stockId = 600000
        time = datetime.datetime.strptime("2016-12-16 10:00:00" , "%Y-%m-%d %H:%M:%S")
        buysell = tradingUnit.BUY
        isSync = True
        tradingType = tradingUnit.FIRST_PRICE_ORDER 
        amount = 500
        testTradingUnit = tradingUnit(tradingUnitId, stockId, time, buysell, isSync, tradingType, amount)

        saver.save_record(testTradingUnit)
        tradingUnitAnsList = saver.get_history_record()
        for tradingUnitAns in tradingUnitAnsList:
            self.log.info("ans: " + str(tradingUnitAns))

if __name__ == '__main__':
    unittest.main()

