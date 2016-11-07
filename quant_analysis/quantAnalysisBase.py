# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: quantAnalysisBase.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: the base class
# ==============================================================================
# 模拟抽象类
import datetime
import numpy as np
def abstract():
    raise NotImplimentedError("Abstract")

class quantAnalysisBase:

    # 股票的开市时间
    stockStartTime = datetime.datetime.strptime("09:00:00" , "%H:%M:%S")
    # 股票的闭市时间
    stockEndTime = datetime.datetime.strptime("15:00:00" , "%H:%M:%S")

    def __init__(self):
        abstract()
        return

    def getHistoryData(self, startTime, endTime, timeInterval, findLastDays = 20):
        # 获取历史数据
        historyDataList = []
        predictList = []
        # 取多少天平均
        n = datetime.timedelta(days=findLastDays)
        # 下单开始和结束的时间差
        delta = (startTime.date() - endTime.date()).days
        self.log.info("days:" + str(delta))
        # 向数据库请求开始的日子
        startDate = startTime.date()
        # 向数据库请求结束的日子
        endDate = startDate - n
        if delta == 0:   
            # 在一天内部
            historyData = self.repoEngine.get_amount(startDate, endDate, startTime.time(), endTime.time())
            historyDataList.append(historyData)
        else:  
            # 多于一天
            historyData = self.repoEngine.get_amount(startDate, endDate, startTime.time(), self.stockEndTime.time())
            historyDataList.append(historyData)
            for i in range(delta - 1):
                historyData = self.repoEngine.get_amount(startDate, endDate, self.stockStartTime.time(), self.stockEndTime.time())
                historyDataList.append(historyData)
            historyData = self.repoEngine.get_amount(startDate, endDate, self.stockStartTime.time(), endTime.time())
            historyDataList.append(historyData)
        
        # 把列表拼接起来
        predictList = historyDataList[0]
        for i in range(1, len(historyDataList)):
            predictList = np.hstack((predictList,historyDataList[i]))
        self.log.info(str(predictList))
        return predictList

    def analysisHistoryData(self):
        abstract()
        return
    
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval):
        abstract()
        return
