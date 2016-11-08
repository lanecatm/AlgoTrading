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
from MarketData import MarketData
import tradingUnit
sys.path.append("../fetch_data/")
from marketDataGetter import marketDataGetter

class poolFromSinaApi:
    def __init__(self, marketDataGetter):
        self.historyTradingList = []
        self.marketDataGetter = marketDataGetter
    
    # 获取交易数据
    def __get_market_trading_data(self):
        originArr = self.marketDataGetter.get_data()
        marketData = MarketData(originArr)
        return marketData

    # 判断这一单的执行情况
    def trade_order(self, tradingUnit):
        marketData = self.__get_market_trading_data()
        nowTradingList = []
        nowLeftAmount = tradingUnit.amount

        # 查询买1~买5/卖1~卖5
        for i in range(0, 5):
            nowTradingUnit = copy.deepcopy(tradingUnit)
            # 若是买入，把 price 和 marketAmount 设为买入量和买入价格，否则设为卖出量和卖出价格
            if nowTradingUnit.buysell == True:
                nowTradingUnit.price = marketData.sellPrice[i]
                marketAmount = marketData.sellAmount[i]
            else:
                nowTradingUnit.price = marketData.buyPrice[i]
                marketAmount = marketData.buyAmount[i]
            # 若可买入/卖出的量大于nowleftAmount，则完成交易，否则向下查询买/卖家不断买入/卖出。
            if nowLeftAmount <= marketAmount:
                nowTradingUnit.amount = nowLeftAmount
                nowLeftAmount = 0
                nowTradingList.append(nowTradingUnit)
                break
            else:
                nowTradingUnit.amount = tradingUnit.price[i]
                nowLeftAmount = nowLeftAmount - marketAmount
                nowTradingList.append(nowTradingUnit)

        # 把买1买2的子订单合成总订单
        succAmount = 0
        succMoney = 0
        for tmpUnit in nowTradingList:
            succAmount = tmpUnit.amount + succAmount
            succMoney = tmpUnit.amount * tmpUnit.price + succMoney
        ansTradingUnit = copy.deepcopy(tradingUnit)
        ansTradingUnit.amount = succAmount
        ansTradingUnit.price = succMoney / float(succAmount)
        ansTradingUnit.isSuccess = True
        return ansTradingUnit

        

