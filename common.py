#!/usr/bin/env python
# encoding: utf-8
# Python 2.7

"""
@time: 11/6/16
@description: 
"""
ID = 10000

class clientOrder:
    # 初始化 client(sorderID, stockID, startTime, endTime, stockAmount,
                 #quantAnalysisAlgChoice, tradingAlgChoice, trading)
    def __init__(self, *args):
        # 默认参数
        if len(args) != 8:
            raise BaseException("Class clientOrder: the number of parameters must be 8!")
        self.orderID = args[0]
        self.stockID = args[1]
        self.startTime = args[2]
        self.endTime = args[3]
        self.stockAmount = args[4]
        self.quantAnalysisAlgChoice = args[5]
        self.tradingAlgChoice = args[6]
        # 买或卖
        self.tradingType = args[7]


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
    # 初始化 orderResult(orderID, stockID)
    def __init__(self, *args):
        if len(args) != 2:
            raise BaseException("Class orderResult: the number of parameters must be 2!")
        self.orderID = args[0]
        self.stockID = args[1]
        resultList = []
    def setOrderID(self, orderID):
        self.orderID = orderID
    def setStockID(self, stockID):
        self.stockID = stockID

class tradingUnit:
    # 初始化 tradingUnit(time, stockID, amount)
    def __init__(self, *args):
        if len(args) != 3:
            raise BaseException("Class tradingUnit: the number of parameters must be 3!")
        self.time = args[0]
        self.stockID = args[1]
        self.amount = args[2]
        self.isSuccess = False;
        self.price = -1;

if __name__ == '__main__':
    pass