#!/usr/bin/env python
# encoding: utf-8
# Python 2.7

"""
@time: 11/6/16
@description: 
"""
ID = 10000

class clientOrder:
    def __init__(self):
        # 默认参数
        global ID
        ID = ID + 1
        orderID = ID + 1
        stockID = 601006
        startTime = 2016-11-05
        endTime = 2016-11-06
        stockAmount = 1000
        quantAnalysisAlgChoice = True
        tradingAlgChoice = 'TWAP'
        # 买或卖
        tradingType = True
    def setOrderID(self, orderID):
        self.orderID = orderID
    def setStockID(self, stockID):
        self.stockID = stockID
    def setStartTime(self, startTime):
        self.startTime = startTime
    def setEdnTime(self, endTime):
        self.endTime = endTime
    def setStockAmout(self, stockAmount):
        self.stockAmount = stockAmount
    def setQuantAnalysisAlgChoice(self, quantAnalysisAlgChoice):
        self.quantAnalysisAlgChoice = quantAnalysisAlgChoice
    def setTradingAlgChoice(self, tradingAlgChoice):
        self.tradingAlgChoice = tradingAlgChoice
    def setTradingType(self, tradingType):
        self.tradingType = tradingType


class orderResult:
    def __init__(self):
        orderID = -1
        stockID = -1
        resultList
    pass

if __name__ == '__main__':
    pass