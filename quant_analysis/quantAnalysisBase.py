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
import sys
sys.path.append("../tool")
from Log import Log
def abstract():
    raise NotImplementedError

class quantAnalysisBase:

    # 股票的开市时间
    stockStartTime = datetime.datetime.strptime("09:30:00" , "%H:%M:%S")
    # 股票的闭市时间
    stockEndTime = datetime.datetime.strptime("15:00:00" , "%H:%M:%S")

    def __init__(self):
        self.log = Log()
        abstract()
        return

    # param weightArray np.array [percentage1, percentage2, ..., percentagen]
    # param timeArray np.array [datetimestring1, datetimestring2, ..., datetimestringn]
    # param tradingStartDate datetime.date 交易开始的日期 防止跨天交易
    # return dict {time1: percentage1, time2: percentage2, ...}
    # example: tradingStartDate 2016-12-23
    # return {2016-12-23 10:03:00': 1.0, '2016-12-23 10:00:00': 0.10000000000000001, '2016-12-23 10:01:00': 0.30000000000000004, '2016-12-23 10:02:00': 0.60000000000000009}
    def format_output(self, weightArray, timeArray, tradingStartDate):
        ansDict = {}
        self.log.info("format_output weight array:" + str(weightArray))
        self.log.info("format_output time array:" + str(timeArray))
        self.log.info("tradingStartDate:" + tradingStartDate.isoformat())
        if weightArray.shape[0] != timeArray.shape[0]:
            self.log.info("the length of weightArray is different to timeArray, " + str(weightArray.shape[0]) + ", " + str(timeArray.shape[0]))
        if timeArray.shape[0] == 0:
            return ansDict
        
        # 由于可能跨天，所以要拼接交易时间
        historyTime = datetime.datetime.strptime(timeArray[0], "%Y-%m-%d %H:%M:%S")
        datedelta = tradingStartDate - historyTime.date()

        for i in range(weightArray.shape[0]):
            # 累计百分比
            sumPercentage = np.sum(weightArray[ : i + 1])
            timeString = (datetime.datetime.strptime(timeArray[i], "%Y-%m-%d %H:%M:%S") + datedelta).strftime("%Y-%m-%d %H:%M:00")
            ansDict[timeString] = sumPercentage
        self.log.info("ansDict:" + str(ansDict))
        return ansDict

    # param stockId int
    # param startTime datetime 交易开始时间
    # param endTime datetime 交易结束时间
    # param findLastDays int 向前寻找多少天
    # return predictList np.array 交易量
    # return predictTimeList np.array 交易量对应时间点
    # predictList [[startTime.date()-1 startTime.time() 的交易量, ..., endTime.date() - 1 endTime.time() 的交易量],
    #              [startTime.date()-2 startTime.time() 的交易量, ..., endTime.date() - 2 endTime.time() 的交易量],
    #              ...
    #              [startTime.date()-findLastDays startTime.time() 的交易量, ..., endTime.date() - findLastDays endTime.time() 的交易量]]
    # 时间间隔默认1分钟, 获取某只股票交易时间段前的交易百分比列表
    def get_history_data(self, stockId, startTime, endTime, findLastDays):
        self.log.info("get history data " + str(stockId) +  "start time: " + startTime.isoformat() + " end time: " + endTime.isoformat())
        # 获取历史数据
        historyDataList = []
        historyTimeList = []
        predictList = []
        predictTimeList = []
        # 取多少天平均
        # 要加上非工作日的时间
        n = datetime.timedelta(days=findLastDays)
        # 下单开始和结束的时间差
        delta = (endTime.date() - startTime.date()).days
        self.log.info("days:" + str(delta))
        # 向数据库请求开始的日子
        startDate = startTime.date() - datetime.timedelta(days = 1 + delta)
        # 向数据库请求结束的日子
        endDate = startDate - n
        if delta == 0:   
            # 在一天内部
            historyData, historyTime = self.repoEngine.get_amount(stockId, startDate, endDate, startTime.time(), endTime.time())
            historyDataList.append(historyData)
            historyTimeList.append(historyTime)
        else:  
            # 多于一天
            historyData, historyTime = self.repoEngine.get_amount(stockId, startDate, endDate, startTime.time(), self.stockEndTime.time())
            historyDataList.append(historyData)
            historyTimeList.append(historyTime)
            for i in range(delta - 1):
                startDate = startDate + datetime.timedelta(days = 1)
                endDate = endDate + datetime.timedelta(days = 1)
                historyData, historyTime = self.repoEngine.get_amount(stockId, startDate, endDate, self.stockStartTime.time(), self.stockEndTime.time())
                historyDataList.append(historyData)
                historyTimeList.append(historyTime)
            startDate = startDate + datetime.timedelta(days = 1)
            endDate = endDate + datetime.timedelta(days = 1)
            historyData, historyTime = self.repoEngine.get_amount(stockId, startDate, endDate, self.stockStartTime.time(), endTime.time())
            historyDataList.append(historyData)
            historyTimeList.append(historyTime)
        
        # 把列表拼接起来
        predictList = historyDataList[0]
        predictTimeList = historyTimeList[0]
        for i in range(1, len(historyDataList)):
            predictList = np.hstack((predictList,historyDataList[i]))
            predictTimeList = np.hstack((predictTimeList, historyTimeList[i]))
        self.log.info(str(predictList))
        self.log.info(str(predictTimeList))
        return predictList, predictTimeList

    # 分析历史数据
    def analysis_history_data(self):
        abstract()
        return
    
    # 得到预测的每日下单量列表
    def get_recommend_order_weight(self, stockId, startTime, endTime, findLastDays):
        abstract()
        return
