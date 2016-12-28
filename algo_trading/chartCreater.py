# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: chartCreater.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-24 16:24
# Description: 图表显示
# ==============================================================================

import sys, os
import MySQLdb
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
from FigHelper import FigHelper
sys.path.append("../common")
from clientOrder import clientOrder
sys.path.append("../fetch_data")
from repo import repo
sys.path.append("../pool")
from tradingRecordSaver import tradingRecordSaver
from repoForAT import repoForAT
sys.path.append("../quant_analysis")
from quantAnalysisBase import quantAnalysisBase
from VWAPQuantAnalysis import VWAPQuantAnalysis


class chartCreater():
    def __init__(self, historyRepo, clientOrderRepo, tradingRepo):
        self.historyRepo = historyRepo
        self.tradingRepo = tradingRepo
        self.clientOrderRepo = clientOrderRepo
        self.log = Log()

    def get_chart(self, orderId):
        order = self.clientOrderRepo.extract_one_order(orderId)
        figHelper = FigHelper()
        #figHelper.set_save()

        sortedDict = sorted(order.quantAnalysisDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = False)
        valueList = []
        timeList = []
        for timePercantage in sortedDict:
            #if index%(len(sortedDict)/xLabelNumber) == 0:
            timeList.append(datetime.datetime.strptime(timePercantage[0], "%Y-%m-%d %H:%M:%S"))
            valueList.append(timePercantage[1])
        figHelper.draw_plot_fig(valueList, timeList, color='r', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading percentage", label = "predicted", linestyle = "-", rotation = True)
        predictTimeList = timeList

        percentageList = []
        timeList = []
        allAmount = order.stockAmount
        nowSuccAmount = 0
        tradingRecordList = self.tradingRepo.get_history_record(orderId)
        for tradeRecord in tradingRecordList:
            nowSuccAmount = nowSuccAmount + tradeRecord.succAmount
            percentageList.append(nowSuccAmount / float(order.stockAmount))
            timeList.append(tradeRecord.time)
        figHelper.draw_plot_fig(percentageList, timeList, color='b', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading percentage", label = "actual", linestyle = "-", rotation = True)

        quantAnalysisGetter = VWAPQuantAnalysis(self.historyRepo)
        startTime = tradingRecordList[0].time
        endTime = tradingRecordList[-1].time
        stockId = tradingRecordList[0].stockId
        dataArray, timeArray = quantAnalysisGetter.get_history_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        dataArray = dataArray / np.sum(dataArray[0], dtype = np.float)
        dataList = []
        for i in range(dataArray[0].shape[0]):
            dataList.append(np.sum(dataArray[0][0:i + 1]))
        print dataList
        if dataArray[0].shape[0] == len(predictTimeList):
            figHelper.draw_plot_fig(dataList, predictTimeList, color='g', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading percentage", label = "expect", linestyle = "--", rotation = True)
        else:
            print dataArray[0].shape[0] , len(predictTimeList)

        figHelper.save()
        figHelper.finish()

    def get_bar(self, orderId):
        order = self.clientOrderRepo.extract_one_order(orderId)
        figHelper = FigHelper()
        #figHelper.set_save()

        percentageList = []
        timeList = []
        allAmount = order.stockAmount
        nowSuccAmount = 0
        tradingRecordList = self.tradingRepo.get_history_record(orderId)
        for tradeRecord in tradingRecordList:
            percentageList.append(tradeRecord.succAmount / float(order.stockAmount))
            timeList.append(tradeRecord.time)
        figHelper.draw_bar_fig(percentageList, timeList, color='b')
        sortedDict = sorted(order.quantAnalysisDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = False)

        valueList = []
        timeList = []
        lastTimePercantage = 0
        lastTimePoint = None
        predictTimeList =[]
        for timePercantage in sortedDict:
            nowtimePoint = datetime.datetime.strptime(timePercantage[0], "%Y-%m-%d %H:%M:%S")
            if lastTimePoint != None:
                if nowtimePoint - lastTimePoint > datetime.timedelta(minutes = 1):
                    timeList.append(lastTimePoint +  datetime.timedelta(minutes = 1))
                    valueList.append(0)
                    timeList.append(datetime.datetime.strptime(timePercantage[0], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(minutes = 1))
                    valueList.append(0)
            lastTimePoint = nowtimePoint

            #if index%(len(sortedDict)/xLabelNumber) == 0:
            timeList.append(datetime.datetime.strptime(timePercantage[0], "%Y-%m-%d %H:%M:%S"))
            predictTimeList.append(datetime.datetime.strptime(timePercantage[0], "%Y-%m-%d %H:%M:%S"))
            valueList.append(timePercantage[1] - lastTimePercantage)
            lastTimePercantage = timePercantage[1]
        figHelper.draw_plot_fig(valueList, timeList, color='r', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading percentage", label = "predicted", linestyle = "-", rotation = True)

        quantAnalysisGetter = VWAPQuantAnalysis(self.historyRepo)
        startTime = tradingRecordList[0].time
        endTime = tradingRecordList[-1].time
        stockId = tradingRecordList[0].stockId
        dataArray, timeArray = quantAnalysisGetter.get_history_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        dataArray = dataArray / np.sum(dataArray[0], dtype = np.float)
        if dataArray[0].shape[0] == len(predictTimeList):
            figHelper.draw_plot_fig(dataArray[0].tolist(), predictTimeList, color='g', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading percentage", label = "expect", linestyle = "--", rotation = True)
        else:
            print dataArray[0].shape[0] , len(predictTimeList)

        figHelper.save()
        figHelper.finish()
        return

    def get_history_TWAP(self, stockId, startTime, endTime):
        return

if __name__=="__main__":
    historyRepo = repo(False, True, None, "algotrading", "12345678", None, False)
    clientOrderRepo = repoForAT("algotrading", "12345678", None)
    tradingRepo = tradingRecordSaver("algotrading", "12345678", None)
    chart = chartCreater(historyRepo, clientOrderRepo, tradingRepo)
    chart.get_chart(4)
    chart.get_bar(4)


