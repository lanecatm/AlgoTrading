# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: repo单元测试
# ==============================================================================
from repoFromTushare import repoFromTushare
import time

if __name__ == '__main__':
    repoEngine = repoFromTushare()
    repoEngine.get_amount(time.strptime("2016-10-24", "%Y-%m-%d"),time.strptime("2016-10-20", "%Y-%m-%d"),time.strptime("13:00:00", "%H:%M:%S"),time.strptime("14:59:00", "%H:%M:%S"))

