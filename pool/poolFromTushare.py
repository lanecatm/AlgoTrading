# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromTushare.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 13:05
# Description: Pool get data from history (Tushare)
# ==============================================================================
import copy
import sys
sys.path.append("../common/")
import MarketData
import TradingUnit
import copy

class poolFromTushare:
    def __init__(self, marketDataGetter):
        self.historyTradingList = []
        self.marketDataGetter = marketDataGetter
    
    def getMarketTradingData(self, time):
        #self.marketDataGetter
        return price, amount

    def tradeOrder(self, tradingUnit):
        # 这里完成的是市价单的操作
        # TODO 限价单
        nowTradingUnit = copy.deepcopy(tradingUnit)
        nowTradingUnit.isSuccess = True
        price, amount = self.getMarketTradingData(tradingUnit.time)
        nowTradingUnit.price = price
        return tradingUnit 

        

