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
from clientFetchData_old import fetchStockMinuData
class repoFromTushare:
    def __init__(self):
        self.repoTushare = fetchStockMinuData()
        self.log = Log()

    def get_amount(self, startDate, endDate, startTime, endTime):
        # 这里endDate大, startDate小
        self.log.info(str(endDate))
        self.log.info(str(startTime))
        importStartDate = endDate.strftime("%Y-%m-%d")
        importEndDate = startDate.strftime("%Y-%m-%d")
        importEndTime = endTime.strftime("%H'%M")
        importStartTime = startTime.strftime("%H'%M")
        self.log.info(importStartDate + " " + importEndDate + " " + importStartTime + " " + importEndTime)
        ansArr = self.repoTushare.fetchData(importStartDate, importEndDate, importStartTime, importEndTime)
        self.log.info("ans: \n" + str(ansArr))
        return ansArr
