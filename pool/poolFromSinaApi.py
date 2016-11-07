# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromSinaApi.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:32
# Description: Pool get data from real time (sina api)
# ==============================================================================
import copy
import sys
sys.path.append("../common/")
import MarketData
import TradingUnit
sys.path.append("../fetch_data/")
import getData

class poolFromSinaApi:
    def __init__(self, marketDataGetter):
        self.historyTradingList = []
        self.marketDataGetter = marketDataGetter
    
    def get_market_trading_data(self):
        originArr = get_data()
        marketData = MarketData(originArr)
        #return self.marketDataGetter.get()

    def trade_order(self, tradingUnit):
        marketData = getMarketTradingData()
        if tradingUnit.attribute == True:
            # buy
            # 如果符合卖1卖2...查找下去
            nowTradingList = []
            nowLeftAmount = tradingUnit.amount
            for i in range(0, 5):
                nowTradingUnit = copy.deepcopy(tradingUnit)
                nowTradingUnit.price = marketData.sellPrice[i]
                nowTradingUnit.isSuccess = True
                if nowLeftAmount <= marketData.sellAmount[i]:
                    nowTradingUnit.amount = nowLeftAmount
                    nowLeftAmount = 0
                    nowTradingList.append(nowTradingUnit)
                    break
                else:
                    nowTradingUnit.amount = marketData.sellAmount[i]
                    nowLeftAmount = nowLeftAmount - marketData.sellAmount[i]
                    nowTradingList.append(nowTradingUnit)
        else:
            # sell
            # 如果符合买一买二...查找下去
            nowTradingUnit = copy.deepcopy(tradingUnit)
            nowTradingUnit.price = marketData.buyPrice[i]
            nowTradingList.append(nowTradingUnit)
            if nowLeftAmount <= marketData.buyAmount[i]:
                    nowTradingUnit.amount = nowLeftAmount
                    nowLeftAmount = 0
                    nowTradingList.append(nowTradingUnit)
                    break
                else:
                    nowTradingUnit.amount = marketData.buyAmount[i]
                    nowLeftAmount = nowLeftAmount - marketData.buyAmount[i]
                    nowTradingList.append(nowTradingUnit)

        return tradingUnit 

        

