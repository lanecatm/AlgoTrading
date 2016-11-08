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
        # 这里endDate大, startDate小
        importStartDate = str(endDate.tm_year) + "-" + str(endDate.tm_mon) + "-" + str(endDate.tm_mday)
        importEndDate = str(startDate.tm_year) + "-" + str(startDate.tm_mon) + "-" + str(startDate.tm_mday)
        importEndTime = str(endTime.tm_hour) + "'" + str(endTime.tm_min)
        importStartTime = str(startTime.tm_hour) + "'" + str(startTime.tm_min)
        self.log.info(importStartDate + " " + importEndDate + " " + importStartTime + " " + importEndTime)
        ansArr = self.repoTushare.fetchData(importStartDate, importEndDate, importStartTime, importEndTime)
        self.log.info(str(ansArr))
