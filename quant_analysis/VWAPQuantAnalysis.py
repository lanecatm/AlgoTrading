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
    
    # 得到预测的每日下单量列表
    # param stockId int 股票代码
    # param startTime datetime 交易开始时间 较小
    # param endTime datetime 交易结束时间 较大
    # param findLastDays int 向前查找的天数
    # return 
    def get_recommend_order_weight(self, stockId, startTime, endTime, findLastDays):
        predictList, predictTime = self.get_history_data(stockId, startTime, endTime, findLastDays)
        self.log.info("predict list: \n" + str(predictList))
        self.log.info("sum :\n" + str(np.sum(predictList, axis = 0, dtype = np.float)))
        self.log.info("sum :\n" + str(np.sum(predictList, dtype = np.float)))
        ansWeightList = np.sum(predictList, axis = 0, dtype = np.float) / np.sum(predictList, dtype = np.float)
        self.log.info(str(ansWeightList))
        return self.format_output(ansWeightList, predictTime[0], startTime.date())

    def show_graph(self, ansWeightList):
        return


