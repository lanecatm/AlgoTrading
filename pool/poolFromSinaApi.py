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
from tradingUnit import tradingUnit
sys.path.append("../fetch_data/")
from marketDataGetter import marketDataGetter
from poolBase import poolBase
sys.path.append("../tool")
from Log import Log

class poolFromSinaApi(poolBase):
    TRADEUNIT = 100
    def __init__(self, dataGetter, isRealTime, recordSaver = None, isOpenLog = True):
        self.historyTradingList = []
        self.dataGetter = dataGetter
        self.isRealTime = isRealTime
        self.recordSaver = recordSaver
        self.log = Log(isOpenLog)
    
    # 获取交易数据
    def get_market_trading_data(self, tradingUnitOrder):
        if self.isRealTime:
            # 从dataGetter取数据
            originArr = self.dataGetter.get_data(tradingUnitOrder.stockId)
            marketData = MarketData(originArr)
        else:
            # 从repo取数据
            originArr = self.dataGetter.get_data(tradingUnitOrder.stockId, tradingUnitOrder.time)
            marketData = MarketData(originArr)
        self.log.info("get market data:" + str(marketData))
        return marketData

    def trade_order_sync(self, tradingUnitOrder):
        self.log.info("trade order sync:" + str(tradingUnitOrder))
        if tradingUnitOrder.tradingType == tradingUnit.FIRST_PRICE_ORDER:
            succAmount, succMoney = self.trade_first_price_order(tradingUnitOrder)
        elif tradingUnitOrder.tradingType == tradingUnit.ALL_PRICE_ORDER:
            succAmount, succMoney = self.trade_all_price_order(tradingUnitOrder)
        elif tradingUnitOrder.tradingType == tradingUnit.LIMITE_PRICE_ORDER:
            succAmount, succMoney = self.trade_limited_price_order(tradingUnitOrder)
        else:
            self.log.error("trading unit tradingType error")
            return
        tradingUnitOrder.refresh_order(succAmount, succMoney, True)
        if self.recordSaver != None:
            self.recordSaver.save_record(tradingUnitOrder)
        return tradingUnitOrder

    # 用买/卖1价格成交
    def trade_first_price_order(self, tradingUnitOrder):
        self.log.info("into trade_first_price_order")
        self.log.info(str(tradingUnitOrder.toString()))
        marketData = self.get_market_trading_data(tradingUnitOrder)
        if tradingUnitOrder.buysell == tradingUnit.BUY:
            self.log.info("buy")
            self.log.info("sell amount 0:" + str(marketData.sellAmount[0]))
            self.log.info("tradingUnitOrder amount:" + str(tradingUnitOrder.amount))
            self.log.info("sellAmount type:" + str(type(marketData.sellAmount[0])))
            self.log.info("order amount type:" + str(type(tradingUnitOrder.amount)))
            if tradingUnitOrder.amount < marketData.sellAmount[0]:
                self.log.info("need less than sell 1")
                succAmount = int(tradingUnitOrder.amount/100)*100
            else:
                self.log.info("need more than sell 1")
                succAmount = int(marketData.sellAmount[0]/100)*100
            succPrice = marketData.sellPrice[0]
            succMoney = succAmount * succPrice
        elif tradingUnitOrder.buysell == tradingUnit.SELL:
            self.log.info("sell")
            if tradingUnitOrder.amount < marketData.buyAmount[0]:
                self.log.info("need less than buy 1")
                succAmount = int(tradingUnitOrder.amount/100)*100
            else:
                self.log.info("need more than buy 1")
                succAmount = int(marketData.buyAmount[0]/100)*100
            succPrice = marketData.buyPrice[0]
            succMoney = succAmount * succPrice
        else:
            self.log.error("trading unit buysell error")
        return succAmount, succMoney

    # 限价单
    # 目前只买卖1的限价
    # TODO 修改限价单
    def trade_limited_price_order(self, tradingUnitOrder):
        self.log.info("into trade_limited_price_order")
        marketData = self.get_market_trading_data(tradingUnitOrder)
        if tradingUnitOrder.buysell == tradingUnit.BUY:
            # 买的情况
            if tradingUnitOrder.expectPrice >= marketData.sellPrice[0]:
                # 我的报价比卖一价格低
                if tradingUnitOrder.amount < marketData.sellAmount[0]:
                    # 数量足够
                    succAmount = int(tradingUnitOrder.amount/100)*100
                else:
                    # 数量不足
                    succAmount = int(marketData.sellAmount[0]/100)*100
                succPrice = marketData.sellPrice[0]
            else:
                succAmount = 0
                succPrice = 0
            succMoney = succAmount * succPrice
        elif tradingUnitOrder.buysell == tradingUnit.SELL:
            if tradingUnitOrder.expectPrice <= marketData.buyPrice[0]:
                if tradingUnitOrder.amount < marketData.buyAmount[0]:
                    succAmount = int(tradingUnitOrder.amount/100)*100
                else:
                    succAmount = int(marketData.buyAmount[0]/100)*100
                succPrice = marketData.buyPrice[0]
            else:
                succAmount = 0
                succPrice = 0
            succMoney = succAmount * succPrice
        else:
            self.log.error("trading unit buysell error")
        return succAmount, succMoney

    # 判断这一单的执行情况
    def trade_all_price_order(self, tradingUnitOrder):
        self.log.info("into trade_all_price_order")
        marketData = self.get_market_trading_data(tradingUnitOrder)
        nowTradingList = []
        nowLeftAmount = tradingUnitOrder.amount

        # 查询买1~买5/卖1~卖5
        for i in range(0, 5):
            nowTradingUnit = copy.deepcopy(tradingUnitOrder)
            # 若是买入，把 price 和 marketAmount 设为买入量和买入价格，否则设为卖出量和卖出价格
            if nowTradingUnit.buysell == tradingUnit.BUY:
                nowTradingUnit.price = marketData.sellPrice[i]
                marketAmount = marketData.sellAmount[i]
            elif nowTradingUnit.buysell == tradingUnit.SELL:
                nowTradingUnit.price = marketData.buyPrice[i]
                marketAmount = marketData.buyAmount[i]
            else:
                self.log.error("trading unit buysell error")
            # 若可买入/卖出的量大于nowleftAmount，则完成交易，否则向下查询买/卖家不断买入/卖出。
            if nowLeftAmount <= marketAmount:
                nowTradingUnit.amount = int(nowLeftAmount/100)*100
                nowLeftAmount = 0
                nowTradingList.append(nowTradingUnit)
                break
            else:
                nowTradingUnit.amount = int(marketAmount/100)*100
                nowLeftAmount = nowLeftAmount - marketAmount
                nowTradingList.append(nowTradingUnit)

        # 把买1买2的子订单合成总订单
        succAmount = 0
        succMoney = 0
        for tmpUnit in nowTradingList:
            self.log.info("amount type:" + str(tmpUnit.amount))
            self.log.info("price type:" + str(tmpUnit.price))
            self.log.info("succMoney type:" + str(tmpUnit.succMoney))
            succAmount = tmpUnit.amount + succAmount
            succMoney = tmpUnit.amount * tmpUnit.price + succMoney
        return succAmount, succMoney

        

