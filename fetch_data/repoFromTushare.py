# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoFromTushare.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: 
# ==============================================================================

import sys, os
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
from clientFetchData import fetchStockMinuData
class repoFromTushare:
    def __init__(self):
        self.repoTushare = fetchStockMinuData()
        self.log = Log()

    def get_amount(self, startDate, endDate, startTime, endTime):
        importStartDate = endDate.strftime("%Y-%m-%d")
        importEndDate = startDate.strftime("%Y-%m-%d")
        importEndTime = endTime.strftime("%H'%M")
        importStartTime = startTime.strftime("%H'%M")
        ansArr = self.repoFromTushare.fetchData(startDate, endDate, startTime, endTime)
        self.log.info(str(ansArr))
