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
from poolFromSinaApi import poolFromSinaApi

sys.path.append("../fetch_data")
from marketDataGetter import marketDataGetter
sys.path.append("../tool")
from Log import Log

import datetime
import random
import time
from repoForAT import repoForAT

class AlgoTrading:
    TRADE_UNIT = 100
    LOW_INTERVAL_BOUND = 200
    HIGH_INTERVAL_BOUND = 1000
    ZOOM = 2

    def __init__(self, rat, pool, quantAnalysisEngineDict, findLastDays):
        self.log = Log()
        self.rat = rat
        self.pool = pool
        self.quantAnalysisEngineDict = quantAnalysisEngineDict
        self.findLastDays = findLastDays
        self.nowTime = None

    def set_time(self, nowTime):
        if self.nowTime == None:
            self.nowTime = nowTime
            return True

        if nowTime <= self.nowTime:
            self.log.error("could not set time before!" + "nowTime: " + str(self.nowTime)+ " setTime: " + str(nowTime))
            return False
        else:
            self.nowTime = nowTime
            return True


    def init_orders(self):
        for order in self.rat.extract_uninit_orders():
            self.log.info("extract uninit order:" + str(order))
            if order.algChoice < len(self.quantAnalysisEngineDict):
                quantAnalysisDict = self.quantAnalysisEngineDict[order.algChoice].get_recommend_order_weight(order.stockId, order.startTime, order.endTime, self.findLastDays)
            else:
                self.log.error("quantAnalisisList do not have algoChoice:" + str(order.algChoice))
            self.rat.save_qa_result(order.orderId, quantAnalysisDict)


    def complete_orders(self):
        for order in self.rat.extract_completed_orders(self.nowTime):
            self.log.info("extract completed orders: " + str(order))
            self.rat.complete_trade(order.orderId)

    def trade_request(self):
        self.trading_orders = self.rat.extract_trading_orders(self.nowTime)
        for order in self.trading_orders:
            #if self.erase_seconds(self.nowTime) == self.erase_seconds(order.nextUpdateTime):
            weight = order.quantAnalysisDict[self.erase_seconds(order.nextUpdateTime).strftime("%Y-%m-%d %H:%M:00")]
            self.log.info("quant analysis weight: " + str(weight))
            amount = (order.stockAmount * weight - order.completedAmount) // 100
            self.log.info("calculated amount:" + str(amount))
            unit = tradingUnit(order.orderId, order.stockId, order.buySell, True,
                               order.tradingType, amount)
            if order.nextUpdateTime <= order.endTime:
                succAmount, succMoney = self.pool.trade_first_price_order(unit)
            else:
                succAmount, succMoney = self.pool.trade_all_price_order(unit)
            self.rat.post_trade(order.completedAmount + succAmount, order.trunOver + succMoney)


    # TODO change timepoint to dict time
    def refresh(self):
        self.refresh_orders = self.rat.extract_refresh_orders(self.nowTime)
        for order in self.refresh_orders:
            # A
            order.updateTime = self.nowTime
            # B
            order.nextUpdateTime = order.updateTime + datetime.timedelta(minutes = order.updateTimeInterval)
            aboutToTrade = order.quantAnalysisDict[self.erase_seconds(order.nextUpdateTime)] - order.completedAmount
            # D
            if aboutToTrade < self.TRADE_UNIT:
                order.trdeTime = None
            elif order.nextUpdateTime > order.endTime:
                order.tradeTime = self.random_trading_time(order.updateTime, endTime.timestamp() - order.updateTime.timestamp())
            else:
                order.tradeTime = self.random_trading_time(order.updateTime, order.updateTimeInterval)
            # C
            if aboutToTrade <= self.LOW_INTERVAL_BOUND:
                order.updateTimeInterval = order.updateTimeInterval * self.ZOOM
            elif aboutToTrade >= self.HIGH_INTERVAL_BOUND:
                if order.updateTimeInterval > 1:
                    order.updateTimeInterval = order.updateTimeInterval / self.ZOOM

            self.rat.post_schedule(order.orderId, order.updateTime, order.nextUpdateTime, order.updateTimeInterval, order.tradeTime)

    # parameter datetime
    # output datetime in whole minutes
    def erase_seconds(self, t):
        return t - datetime.timedelta(seconds = t.second) - datetime.timedelta(microseconds = t.microsecond)

    # return tradingTime
    def random_trading_time(self, updateTime, updateTimeInterval):
        randomSeconds = int(random.random() * 60 *updateTimeInterval)
        return updateTime + datetime.timedelta(seconds = randomSeconds)


 

