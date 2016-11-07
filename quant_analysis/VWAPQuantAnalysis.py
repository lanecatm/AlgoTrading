# -*- encoding:utf-8 -*-
# =============================================================================
# Filename: VWAPQuantAnalysis.py
# Author: Yuchang Xu
# Description: 简单滑动平均VWAP实现
# ==============================================================================
import sys
import datetime
import numpy as np
from quantAnalysisBase import quantAnalysisBase
sys.path.append("../fetch_data")
import repo
sys.path.append("../tool")
from Log import Log

class VWAPQuantAnalysis(quantAnalysisBase):

    def __init__(self, repoEngine):
        self.repoEngine = repoEngine
        self.log = Log()
        return
    
    # 目前timeInterval没有用到，全部以1分钟计
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval, findLastDays = 20):
        predictList = quantAnalysisBase.getHistoryData(self, startTime, endTime, timeInterval, findLastDays)
        ansWeightList = np.sum(predictList, axis = 0, dtype = np.float) / np.sum(predictList, dtype = np.float)
        self.log.info(str(ansWeightList))
        return ansWeightList

