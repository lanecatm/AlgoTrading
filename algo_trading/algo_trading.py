#!/usr/bin/env python
# encoding: utf-8
# Python 2,7

"""
@time: 11/6/16
@author: Fengjun Chen
@description: 
"""
import sys
#sys.path.append("../cli/")
sys.path.append("../common/")
import clientOrder
import orderResult
from tradingUnit import tradingUnit
sys.path.append("../quant_analysis")
from TWAPQuantAnalysis import TWAPQuantAnalysis
from VWAPQuantAnalysis import VWAPQuantAnalysis
sys.path.append("../pool")
# import poolFromSinaApi
from poolFromTushare import poolFromTushare
from tradingRecordRepo import tradingRecordRepo
sys.path.append("../fetch_data")
from repoFromTushare import repoFromTushare
sys.path.append("../tool")
from Log import Log

import numpy as np
import MySQLdb
import datetime
import sqlite3

dbfile = 'test_0.1.db'

class algo_trading:
    # TBD
    #def __init__(self, ClientOrder):
    def __init__(self):
        #self.setParam(ClientOrder)
        self.marketGetter = repoFromTushare()
        self.saveEngine = tradingRecordRepo("test_trading_record.db")
        self.pool = poolFromTushare(self.marketGetter, self.saveEngine)
        self.log = Log()
        self.orders = []

    # 设置交易参数，传入一个 clientOrder 类
    def setParam(self, CO):
        self.clientOrder = CO
    
    # 将数据库中未完成的订单信息读到二维list orders 
    def extractOrder(self):
        db = MySQLdb.connect("localhost","root","weiyisjtu","algotradingDB")
        cursor = db.cursor()
        sql = "SELECT * FROM CLIENTORDERS WHERE COMPLETEDAMOUNT < STOCKAMOUNT"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                self.orders.append([])
                for i in range(12):
                    self.orders[-1].append(row[i])
        except:
            print "Error: unable to fetch client orders"
        db.close()

    # 获取真实情况下的Vwap值
    def getVwapActual(self, startTime, endTime):
        self.log.info("start time and end time:" + str(startTime) + " " + str(endTime))
        marketGetter = repoFromTushare()
        day = datetime.timedelta(days = 1)
        priceArray = marketGetter.get_price(startTime.date(), endTime.date() - day, startTime.time(), endTime.time())
        amountArray = marketGetter.get_amount(startTime.date(), endTime.date() - day, startTime.time(), endTime.time())
        sumArray = priceArray * amountArray
        self.log.info("vwap actual :\n" + str(sumArray))
        ansPrice = np.sum(sumArray) / np.sum(amountArray)
        self.log.info("vwap price:" + str(ansPrice))
        return ansPrice


    # 根据订单通过不同策略执行交易，返回list, 该 list 存储每个交易时间点返回的 tradingUnit。
    # TBD 斜率 下单, trade request for one order
    def tradeRequest(self):
        self.resultList = []
        tradingTime = self.clientOrder.startTime
        turnover = 0
        for i in range(len(self.quant_result)):
            tradingTime = tradingTime + datetime.timedelta(minutes=1)
            stockId = self.clientOrder.stockId
            amount = self.clientOrder.stockAmount * self.quant_result[i] # waht if  小数
            buysell = self.clientOrder.buysell
            inTradingUnit = tradingUnit(self.clientOrder.orderId, stockId, buysell, amount, None, None, tradingTime)
            # 执行 pool 交易
            #outTradingUnit = poolFromSinaApi.trade_order(inTradingUnit)
            outTradingUnit = self.pool.trade_order(inTradingUnit)
            self.resultList.append(outTradingUnit)
            
            turnover += outTradingUnit.price * amount
        actualprice = self.getVwapActual(self.clientOrder.startTime, self.clientOrder.endTime)
        # Conclude the results and get back to orders in db
        # update in database
        
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        avgprice = turnover/self.clientOrder.stockAmount
        cursor.execute('update orders set total=?,ap=?,wap=?,status=2 where id=?',(turnover, avgprice, actualprice, self.clientOrder.orderId))
        cursor.close()
        conn.commit()
        conn.close()
        

    # 获取量化分析结果，没有返回值。
    def getQuantAnalysisResult(self):
        if self.clientOrder.algChoice == "twap":
            self.quant_analysis = TWAPQuantAnalysis()
        elif self.clientOrder.algChoice == "vwap":
            self.quant_analysis = VWAPQuantAnalysis(self.marketGetter)
        self.quant_result = self.quant_analysis.getRecommendOrderWeight(self.clientOrder.startTime, self.clientOrder.endTime, self.clientOrder.timeInterval)


if __name__ == '__main__':
    pass
