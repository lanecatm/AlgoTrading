#!/usr/bin/env python
# encoding: utf-8
# Python 2,7

"""
@time: 11/6/16
@description: 
"""
import sys
sys.path.append("../common/")
import clientOrder
import orderResult
import tradingUnit
sys.path.append("../quant_analysis")
import TWAPQuantAnalysis
#import VWAPQuantAnalysis


class algo_trading:
    def __init__(self):
        # 默认参数
        self.clientOrder = clientOrder(10000, 601006, 2016-11-03, 2016-11-04, 1000, True, "TWAP", 60)

    # 设置交易参数，传入一个 clientOrder 类
    def SetParam(self, CO):
        self.clientOrder = CO

    # 根据订单通过不同策略执行交易，返回各时间点交易信息的list
    def TradeReques(self):
        self.resultList = []
        tradingTime = self.clientOrder.startTime
        for i in range(len[self.quant_result]):
            tradingTime = tradingTime + self.clientOrder.timeInterval
            stockId = self.clientOrder.stockId
            amount = self.clientOrder.stockAmount * self.quant_result[i]
            buysell = self.clientOrder.buysell
            unit = tradingUnit(tradingTime, stockId, amount, None, None, buysell)
            self.resultList.append(unit)
        return self.resultList

    # 获取量化分析结果
    def GetQuantAnalysisResult(self):
        if self.clientOrder.algChoice == "TWAP":
            quant_analysis = TWAPQuantAnalysis()
        #elif self.clientOrder.algChoice == "VWAP":
            #quant_analysis = VWAPQuantAnalysis()
        self.quant_result = quant_analysis.getRecommendOrderWeight(self.clientOrder.startTime, self.clientOrder.endTime,
                                                      self.clientOrder.timeInterval)


if __name__ == '__main__':
    pass