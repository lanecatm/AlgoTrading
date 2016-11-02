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

if __name__ == '__main__':
    repoEngine = repo("test.db")
    print repoEngine.get_amount(time.strptime("2016-11-01", "%Y-%m-%d"),time.strptime("2016-10-31", "%Y-%m-%d"),time.strptime("09:10:00", "%H:%M:%S"),time.strptime("09:13:00", "%H:%M:%S"))

