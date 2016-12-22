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
from LinearVWAPQuantAnalysis import LinearVWAPQuantAnalysis

class repoTest:
    def __init__(self):
        self.log = Log()

    def get_amount( self, stockId, startDate, endDate, startTime, endTime):
        self.log.info("repo input: " + str(startDate) + " "+ str(endDate) + " "+ str(startTime) + " " + str(endTime))
        timeArray = np.array([[startDate.strftime("%Y-%m-%d") + " 10:00:00", startDate.strftime("%Y-%m-%d") + " 10:01:00",startDate.strftime("%Y-%m-%d") + " 10:02:00",startDate.strftime("%Y-%m-%d")+ " 10:03:00"]]*5)
        return np.array([[1,2,3,4], [4, 3, 2, 1], [0,0,0,0], [0,0,0,0],[0,0,0,0]]), timeArray

class LinearVWAPQuantAnalysisUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_get_recommend_order_weight(self):
        repoEngine = repoTest()
        LinearVWAPAnalysis = LinearVWAPQuantAnalysis(repoEngine)
        startDate=datetime.datetime.strptime("2016-12-22 10:00:00" , "%Y-%m-%d %H:%M:%S")
        endDate = datetime.datetime.strptime("2016-12-23 09:40:00", "%Y-%m-%d %H:%M:%S")
        ansDict = LinearVWAPAnalysis.get_recommend_order_weight(600000, startDate, endDate, 5)
        self.assertEqual(len(ansDict), 8)
        ansDict = LinearVWAPAnalysis.get_recommend_order_weight(600000, startDate, startDate + datetime.timedelta(hours = 10), 5)
        self.assertEqual(len(ansDict), 4)
        ansDictPair = sorted(ansDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = False)
        self.log.info("ans:" + str(ansDictPair))
        self.assertTrue(ansDictPair[0][1] < ansDictPair[1][1])
        return 




if __name__ == '__main__':
    unittest.main()


