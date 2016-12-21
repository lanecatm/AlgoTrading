# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: quantAnalysisBaseUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-21 20:42
# Description: quantAnalysisBase单元测试
# ==============================================================================
import time
import sys
import datetime
import numpy as np
import unittest
sys.path.append("../tool")
from Log import Log
from quantAnalysisBase import quantAnalysisBase

class testQuantAnalysis(quantAnalysisBase):
    def __init__(self):
        self.log = Log()
        self.repoEngine = testRepo()
        return
class testRepo:
    def __init__(self):
        self.log = Log()
    def get_amount(self, stockId, startDate, endDate, startTime, endTime):
        self.log.info("repo input: " + str(startDate) + " "+ str(endDate) + " "+ str(startTime) + " " + str(endTime))
        return np.array([[1, 2, 3, 4]]*5), np.array([["2016-12-21 10:00:00", "2016-12-21 10:01:00","2016-12-21 10:02:00", "2016-12-21 10:03:00"]]*5)


class quantAnalysisBaseUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_format_output(self):
        quantAnalysisEngine = testQuantAnalysis()
        weightArray = np.array([0.1, 0.2, 0.3, 0.4])
        timeArray = np.array(["2016-12-21 10:00:00", "2016-12-21 10:01:00","2016-12-21 10:02:00", "2016-12-21 10:03:00"])
        startDate = datetime.date(2016,12,23)
        ansDict = quantAnalysisEngine.format_output(weightArray, timeArray, startDate)
        self.assertEqual(int(ansDict["2016-12-23 10:00:00"] * 10), 1)
        self.assertEqual(int(ansDict["2016-12-23 10:01:00"] * 10), 3)
        self.assertEqual(int(ansDict["2016-12-23 10:02:00"] * 10), 6)
        self.assertEqual(int(ansDict["2016-12-23 10:03:00"] * 10), 10)
        return 

    def test_get_history_data(self):
        quantAnalysisEngine = testQuantAnalysis()
        stockId = 600000
        startTime = datetime.datetime(2016, 12, 25, 10, 30, 00)
        endTime = datetime.datetime(2016, 12, 27, 17, 00, 00)
        findLastDays = 7
        self.log.info("except 2016-12-22 2016-12-15 10:30:00 15:00:00")
        self.log.info("except 2016-12-23 2016-12-16 09:30:00 15:00:00")
        self.log.info("except 2016-12-24 2016-12-17 09:30:00 17:00:00")
        quantAnalysisEngine.get_history_data(stockId, startTime, endTime, findLastDays)


if __name__ == '__main__':
    unittest.main()

