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
        predictTimeList = timeList[:]

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
        startTime = datetime.datetime.strptime(sortedDict[0][0], "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(sortedDict[-1][0], "%Y-%m-%d %H:%M:%S")
        #endTime = tradingRecordList[-1].time
        stockId = tradingRecordList[0].stockId


        vwapTmp, TWAPvalue = self.get_history_TWAP(stockId, startTime, endTime)
        print "vwap tmp:", vwapTmp
        print "twap tmp:", TWAPvalue

        dataArray, timeArray = quantAnalysisGetter.get_history_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        dataArray = dataArray / np.sum(dataArray[0], dtype = np.float)
        dataList = []
        for i in range(dataArray[0].shape[0]):
            dataList.append(np.sum(dataArray[0][0:i + 1]))
        print dataList
        if dataArray[0].shape[0] == len(predictTimeList):
            figHelper.draw_plot_fig(dataList, predictTimeList, color='g', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading VWAP Price: " + str(vwapTmp) + ", TWAP Price:" + str(TWAPvalue), label = "expect", linestyle = "--", rotation = True)
        else:
            print dataArray[0].shape[0] , len(predictTimeList)
            print str(dataArray[0])
            print str(predictTimeList)
            print str(timeArray)

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
        startTime = datetime.datetime.strptime(sortedDict[0][0], "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(sortedDict[-1][0], "%Y-%m-%d %H:%M:%S")
        #startTime = tradingRecordList[0].time
        #endTime = tradingRecordList[-1].time
        stockId = tradingRecordList[0].stockId

        vwapTmp, TWAPvalue = self.get_history_TWAP(stockId, startTime, endTime)
        print "vwap actual:", vwapTmp
        print "twap actual:", TWAPvalue
        
        dataArray, timeArray = quantAnalysisGetter.get_history_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        dataArray = dataArray / np.sum(dataArray[0], dtype = np.float)
        if dataArray[0].shape[0] == len(predictTimeList):
            figHelper.draw_plot_fig(dataArray[0].tolist(), predictTimeList, color='g', xLabel = "", yLabel = "percentage", title = "order " + str(orderId) + " trading, VWAP Price:" + str(vwapTmp) + ", TWAP Price:" + str(TWAPvalue), label = "expect", linestyle = "--", rotation = True)
        else:
            print dataArray[0].shape[0] , len(predictTimeList)
            print str(dataArray[0])
            print str(predictTimeList)
            print str(timeArray)


        figHelper.save()
        figHelper.finish()
        return

    def get_history_TWAP(self, stockId, startTime, endTime):
        quantAnalysisGetter = VWAPQuantAnalysis(self.historyRepo)
        dataArray, timeArray = quantAnalysisGetter.get_history_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        amountArray = dataArray / np.sum(dataArray[0], dtype = np.float)
        percentageArray = amountArray[0]
        priceArray, timeArray = quantAnalysisGetter.get_price_data(stockId,startTime, endTime + datetime.timedelta(minutes = 1), 7)
        priceArray = priceArray[0]
        VWAPvalue = percentageArray * priceArray
        TWAPvalue = np.sum(priceArray) / priceArray.shape[0]

        return np.sum(VWAPvalue), TWAPvalue

if __name__=="__main__":
    historyRepo = repo(False, True, None, "algotrading", "12345678", None, False)
    clientOrderRepo = repoForAT("algotrading", "12345678", None, False)
    tradingRepo = tradingRecordSaver("algotrading", "12345678", None, False)
    chart = chartCreater(historyRepo, clientOrderRepo, tradingRepo)
    chart.get_chart(20)
    chart.get_bar(20)


