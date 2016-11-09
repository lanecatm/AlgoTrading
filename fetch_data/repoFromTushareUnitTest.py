# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoFromTushare.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-09 08:58
# Description: repo单元测试
# ==============================================================================
from repoFromTushare import repoFromTushare
from datetime import datetime

if __name__ == '__main__':
    repoEngine = repoFromTushare()
    repoEngine.get_amount(datetime.strptime("2016-10-12", "%Y-%m-%d"),datetime.strptime("2016-10-08", "%Y-%m-%d"),datetime.strptime("10:30:00", "%H:%M:%S"),datetime.strptime("11:50:00", "%H:%M:%S"))

