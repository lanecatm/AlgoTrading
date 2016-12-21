# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: repo单元测试
# ==============================================================================
import sys
from repo import repo
import time
import datetime
import unittest

sys.path.append("../tool")
from Log import Log

class repoUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_sqlite(self):
        sqliteRepo = repo(True, True, "again_2.db", "algotrading", "12345678", None)
        #sqliteRepo.change_data_into_mysql()
        return

    def test_mysql_get_amount(self):
        mysqlRepo = repo(False, True , None, "algotrading", "12345678", None)
        startTime = datetime.datetime(2016,12,17,9,30,0)
        endTime = datetime.datetime(2016,12,14, 14,0,0)
        data, time = mysqlRepo.get_amount(600000, startTime.date(), endTime.date(), startTime.time(), endTime.time())
        self.assertEqual(len(data), 2)
        self.assertEqual(len(time), 2)
        for dataLine in data:
            self.assertEqual(len(dataLine), 181)
        for dataLine in time:
            self.assertEqual(len(dataLine), 181)

    def test_mysql_get_price(self):
        mysqlRepo = repo(False, True , None, "algotrading", "12345678", None)
        startTime = datetime.datetime(2016,12,17,9,30,0)
        endTime = datetime.datetime(2016,12,14, 14,0,0)
        data, time = mysqlRepo.get_price(600000, startTime.date(), endTime.date(), startTime.time(), endTime.time())
        self.assertEqual(len(data), 2)
        self.assertEqual(len(time), 2)
        for dataLine in data:
            self.assertEqual(len(dataLine), 181)
        for dataLine in time:
            self.assertEqual(len(dataLine), 181)
        return




if __name__ == '__main__':
    unittest.main()

