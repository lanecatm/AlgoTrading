# -*- encoding:utf-8 -*-
# =============================================================================
# Filename: VWAPQuantAnalysis.py
# Author: Yuchang Xu
# Description: 简单加权滑动平均VWAP实现
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
    def __init__(self, repoEngine, isOpenLog = True):
        self.log = Log(isOpenLog)
        self.repoEngine = repoEngine
        return

    # 得到预测的每日下单量列表
    # param stockId int 股票代码
    # param startTime datetime 交易开始时间 较小
    # param endTime datetime 交易结束时间 较大
    # param findLastDays int 向前查找的天数
    # return 
    def get_recommend_order_weight(self, stockId, startTime, endTime, findLastDays):
        predictList, predictTime = self.get_history_data(stockId, startTime, endTime, findLastDays)
        weightUnit = []
        actualFindLastDays = predictList.shape[0]
        findLastDays = actualFindLastDays
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
        return self.format_output(ansWeightList, predictTime[0], startTime.date())

