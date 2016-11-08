#!/usr/bin/env python
# encoding: utf-8
# Python 2,7

"""
@time: 11/6/16
@author: Fengjun Chen
@description: 
"""
import sys
sys.path.append("../common/")
import clientOrder
import orderResult
import tradingUnit
sys.path.append("../quant_analysis")
import TWAPQuantAnalysis
import VWAPQuantAnalysis
sys.path.append("../pool")
# import poolFromSinaApi
import poolFromTushare
import sqlite3
sys.path.append("../cli/")
from cli import dbfile

class algo_trading:
    def __init__(self, ClientOrder):
        self.setParam(ClientOrder)

    # 设置交易参数，传入一个 clientOrder 类
    def setParam(self, CO):
        self.clientOrder = CO

    # 根据订单通过不同策略执行交易，返回list, 该 list 存储每个交易时间点返回的 tradingUnit。
    def tradeRequest(self):
        self.resultList = []
        tradingTime = self.clientOrder.startTime
        turnover = 0
        # vwap = 0
        for i in range(len[self.quant_result]):
            tradingTime = tradingTime + self.clientOrder.timeInterval # ??? Define timeinterval --Yi
            stockId = self.clientOrder.stockId
            amount = self.clientOrder.stockAmount * self.quant_result[i] # waht if  小数
            buysell = self.clientOrder.buysell
            inTradingUnit = tradingUnit(tradingTime, stockId, amount, buysell, None, None, self.clientOrder.orderId)
            # 执行 pool 交易
            #outTradingUnit = poolFromSinaApi.trade_order(inTradingUnit)
            outTradingUnit = poolFromTushare.trade_order(inTradingUnit)
            self.resultList.append(outTradingUnit)
            
            turnover += outTradingUnit.price * amount
        # Conclude the results and get back to orders in db
        # update in database
        conn = sqlite3.connect(dbfile) 
        cursor = conn.cursor
        avgprice = turnover/self.clientOrder.amount
        cursor.execute('update orders set total=?,ap=?,wap=? where id=?',(turnover, avgprice, avgprice, sef.clientOrder.orderId))
        cursor.close()
        conn.commit()
        conn.close()
        

    # 获取量化分析结果，没有返回值。
    def getQuantAnalysisResult(self):
        if self.clientOrder.algChoice == "twap":
            quant_analysis = TWAPQuantAnalysis()
        elif self.clientOrder.algChoice == "vwap":
            quant_analysis = VWAPQuantAnalysis()
        self.quant_result = quant_analysis.getRecommendOrderWeight(self.clientOrder.startTime, self.clientOrder.endTime,
                                                      self.clientOrder.timeInterval)


if __name__ == '__main__':
    pass
