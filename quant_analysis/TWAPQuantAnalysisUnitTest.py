# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: TWAPQuantAnalysisUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: TWAP单元测试
# ==============================================================================

import time, sys
import datetime
import numpy as np
import unittest
sys.path.append("../tool")
from Log import Log
from TWAPQuantAnalysis import TWAPQuantAnalysis

class repoTest:
    def __init__(self):
        self.log = Log()

    def get_amount( self, stockId, startDate, endDate, startTime, endTime):
        self.log.info("repo input: " + str(startDate) + " "+ str(endDate) + " "+ str(startTime) + " " + str(endTime))
        timeArray = np.array([[startDate.strftime("%Y-%m-%d") + " 10:00:00", startDate.strftime("%Y-%m-%d") + " 10:01:00",startDate.strftime("%Y-%m-%d") + " 10:02:00",startDate.strftime("%Y-%m-%d")+ " 10:03:00"]]*5)
        return np.array([[1,2,3,4]]*5), timeArray

class TWAPQuantAnalysisUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_find_trading_time(self):
        quantAnalysisEngine = TWAPQuantAnalysis()
        startDate=datetime.datetime.strptime("2016-12-22 10:00:00" , "%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.strptime("2016-12-24 09:40:00", "%Y-%m-%d %H:%M:%S")
        timeList = quantAnalysisEngine.find_trading_time(startDate, endDate)
        self.assertEqual(len(timeList), 91 + 121 + 121 + 121)
        startDate=datetime.datetime.strptime("2016-12-22 08:00:00" , "%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.strptime("2016-12-22 09:40:00", "%Y-%m-%d %H:%M:%S")
        timeList = quantAnalysisEngine.find_trading_time(startDate, endDate)
        self.assertEqual(len(timeList), 10)
        return

    def test_get_recommend_order_weight(self):
        quantAnalysisEngine = TWAPQuantAnalysis()
        startDate=datetime.datetime.strptime("2016-12-22 10:00:00" , "%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.strptime("2016-12-23 09:40:00", "%Y-%m-%d %H:%M:%S")
        weightDict = quantAnalysisEngine.get_recommend_order_weight(60000, startDate, endDate, None)
        weightDictTuple = sorted(weightDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = True)
        self.log.info("weight dict:" + str(weightDictTuple))
        self.assertEqual(len(weightDict), 91 + 121 + 10)

        return 

if __name__ == '__main__':
    unittest.main()

