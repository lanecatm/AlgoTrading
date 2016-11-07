# -*- encoding:utf-8 -*-
# =============================================================================
# Filename: VWAPQuantAnalysis.py
# Author: Yuchang Xu
# Description: 线性滑动平均VWAP实现
# ==============================================================================
from quantAnalysisBase import quantAnalysisBase
import sys
sys.path.append("../fetch_data")
import repo
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
class LinearVWAPQuantAnalysis(quantAnalysisBase):
    def __init__(self, repoEngine):
        self.log = Log()
        self.repoEngine = repoEngine
        return

    def getRecommendOrderWeight(self, startTime, endTime, timeInterval, findLastDays = 20):
        predictList = quantAnalysisBase.getHistoryData(self, startTime, endTime, timeInterval, findLastDays)
        weightUnit = []
        for i in range(findLastDays, 0, -1):
            weightUnit.append([i / ((1.0 + findLastDays) * findLastDays / 2.0)])
        self.log.info("weightUnit\n" + str(weightUnit))
        weight = weightUnit
        for i in range(predictList.shape[1] - 1):
            weight = np.hstack((weight,weightUnit))
        self.log.info("weight\n" + str(weight))
        predictList = predictList * weight
        ansWeightList = np.sum(predictList, axis = 0, dtype = np.float) / np.sum(predictList, dtype = np.float)
        self.log.info("ans\n" + str(ansWeightList))
        return ansWeightList

