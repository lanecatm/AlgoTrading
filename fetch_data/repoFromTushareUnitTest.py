# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: repo单元测试
# ==============================================================================
from repoFromTushare import repoFromTushare
from datetime import datetime

if __name__ == '__main__':
    repoEngine = repoFromTushare()
    repoEngine.get_amount(datetime.strptime("2016-10-12", "%Y-%m-%d"),datetime.strptime("2016-10-10", "%Y-%m-%d"),datetime.strptime("13:30:00", "%H:%M:%S"),datetime.strptime("14:59:00", "%H:%M:%S"))

