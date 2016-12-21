# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: VWAPQuantAnalysisUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-04 16:00
# Description: VWAPQuantAnalysis单元测试
# ==============================================================================
import time, sys
import datetime
import numpy as np
import unittest
sys.path.append("../tool")
from Log import Log
from VWAPQuantAnalysis import VWAPQuantAnalysis

class repoTest:
    def __init__(self):
        self.log = Log()

    def get_amount( self, stockId, startDate, endDate, startTime, endTime):
        self.log.info("repo input: " + str(startDate) + " "+ str(endDate) + " "+ str(startTime) + " " + str(endTime))
        timeArray = np.array([[startDate.strftime("%Y-%m-%d") + " 10:00:00", startDate.strftime("%Y-%m-%d") + " 10:01:00",startDate.strftime("%Y-%m-%d") + " 10:02:00",startDate.strftime("%Y-%m-%d")+ " 10:03:00"]]*5)
        return np.array([[1,2,3,4]]*5), timeArray

class VWAPQuantAnalysisUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_get_recommend_order_weight(self):
        repoEngine = repoTest()
        VWAPAnalysis = VWAPQuantAnalysis(repoEngine)
        startDate=datetime.datetime.strptime("2016-12-22 10:00:00" , "%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.strptime("2016-12-23 09:40:00", "%Y-%m-%d %H:%M:%S")
        ansDict = VWAPAnalysis.get_recommend_order_weight(600000, startDate, endDate, 5)
        self.assertEqual(len(ansDict), 8)
        ansDict = VWAPAnalysis.get_recommend_order_weight(600000, startDate, startDate + datetime.timedelta(hours = 10), 5)
        self.assertEqual(len(ansDict), 4)
        return 




if __name__ == '__main__':
    unittest.main()

