# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: repo单元测试
# ==============================================================================
from repo import repo
import time
import unittest

sys.path.append("../tool")
from Log import Log

class repoUnitTest(unittest.TestCase):

    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_sqlite(self):
        return

    def test_mysql(self):
        mysqlRepo = repo()
        self.assertEqual(0, 0)
        return




if __name__ == '__main__':
    unittest.main()

