# -*- encoding:utf-8 -*-
import sys
import datetime
import random

sys.path.append("../common/")
import clientOrder
from tradingUnit import tradingUnit

sys.path.append("../tool")
from Log import Log


class algoTrading:
    TRADE_UNIT = 100
    LOW_INTERVAL_BOUND = 200
    HIGH_INTERVAL_BOUND = 1000
    ZOOM = 2

    def __init__(self, rat, pool, quantAnalysisEngineDict, findLastDays, isOpenLog = True):
        self.log = Log(isOpenLog)
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
            self.log.info("trading request:" + str(order))
            #if self.erase_seconds(self.nowTime) == self.erase_seconds(order.nextUpdateTime):
            # 有nextUpdateTime的情况
            # TODO 没有的话为1
            if order.nextUpdateTime < order.endTime:
                self.log.info("order.quantAnalysisDict:" + str(order.quantAnalysisDict))
                weight = order.quantAnalysisDict[self.erase_seconds(order.nextUpdateTime).strftime("%Y-%m-%d %H:%M:00")]
                self.log.info("quant analysis weight: " + str(weight))
                amount = int((order.stockAmount * weight - order.completedAmount)/self.TRADE_UNIT) * self.TRADE_UNIT
                self.log.info("completed amount:" + str(order.completedAmount))
                self.log.info("calculated amount:" + str(amount))
                unit = tradingUnit(order.orderId, order.stockId, self.nowTime, order.buySell, True, tradingUnit.FIRST_PRICE_ORDER, amount)
                succTradingUnit = self.pool.trade_order_sync(unit)
                succAmount = succTradingUnit.succAmount
                succMoney = succTradingUnit.succMoney
                self.log.info("trade succ amount: " + str(succAmount))
                self.log.info("trade succ money: " + str(succMoney))
            else:
                amount = int((order.stockAmount - order.completedAmount)/self.TRADE_UNIT) * self.TRADE_UNIT
                self.log.info("calculated amount:" + str(amount))
                unit = tradingUnit(order.orderId, order.stockId, self.nowTime, order.buySell, True, tradingUnit.ALL_PRICE_ORDER, amount)
                succTradingUnit = self.pool.trade_order_sync(unit)
                succAmount = succTradingUnit.succAmount
                succMoney = succTradingUnit.succMoney
                self.log.info("trade succ amount: " + str(succAmount))
                self.log.info("trade succ money: " + str(succMoney))
            self.rat.post_trade(order.orderId, order.completedAmount + succAmount, order.trunOver + succMoney)


    def refresh(self):
        self.refresh_orders = self.rat.extract_refresh_orders(self.nowTime)
        for order in self.refresh_orders:
            self.log.info("refresh order:" + str(order))
            # A
            order.updateTime = self.nowTime
            # B
            # change timepoint to dict time
            sortedDict = sorted(order.quantAnalysisDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = False)
            self.log.info("sorted dict:" + str(sortedDict))
            # 可能会超过最后一个index
            index = 0
            for timeWeight in sortedDict:
                if timeWeight[0] == self.nowTime.strftime("%Y-%m-%d %H:%M:00"):
                    break
                index = index + 1
            if index >= len(sortedDict):
                continue
            nextUpdateTimeIndex = index + order.updateTimeInterval
            self.log.info("index:" + str(index))
            self.log.info("update index:" + str(nextUpdateTimeIndex))
            self.log.info("all index: " + str(len(sortedDict)))
            if nextUpdateTimeIndex >= len(sortedDict) - 1:
                self.log.info("final time point")
                # 到了结束时间
                order.nextUpdateTime = order.endTime
                self.log.info("final nextUpdateTime:" + str(order.nextUpdateTime))
                # 结束时间可能不能购买股票, 所以使用列表最后一个时间
                aboutToTrade = order.stockAmount - order.completedAmount
                actualEndTime = datetime.datetime.strptime(sortedDict[-1][0], "%Y-%m-%d %H:%M:%S")
                order.updateTimeInterval = (actualEndTime - order.updateTime).seconds / 60
                maxIndexNum = len(sortedDict) - index
            else:
                order.nextUpdateTime = datetime.datetime.strptime(sortedDict[nextUpdateTimeIndex][0], "%Y-%m-%d %H:%M:%S")
                weight = sortedDict[nextUpdateTimeIndex][1]
                aboutToTrade = weight * order.stockAmount - order.completedAmount
                maxIndexNum = order.updateTimeInterval

            self.log.info("about to trade : " + str(aboutToTrade))
            # D
            if aboutToTrade < self.TRADE_UNIT:
                order.trdeTime = None
            else:
                randomIndex, randomSeconds = self.random_trading_time(index, maxIndexNum)
                self.log.info("random trade index:" + str(randomIndex))
                order.tradeTime = datetime.datetime.strptime(sortedDict[randomIndex][0], "%Y-%m-%d %H:%M:%S")
                self.log.info("trade time:" + str(order.tradeTime))
                if order.tradeTime >= order.nextUpdateTime:
                    self.log.error("trade time > nextUpdateTime " + str(order.tradeTime) + ", " + str(order.nextUpdateTime))
            # C
            if aboutToTrade <= self.LOW_INTERVAL_BOUND:
                self.log.info("increase interval")
                order.updateTimeInterval = order.updateTimeInterval * self.ZOOM
            elif aboutToTrade >= self.HIGH_INTERVAL_BOUND:
                self.log.info("decrease interval")
                if order.updateTimeInterval > 1:
                    order.updateTimeInterval = order.updateTimeInterval / self.ZOOM

            self.rat.post_schedule(order.orderId, order.updateTime, order.nextUpdateTime, order.updateTimeInterval, order.tradeTime)

    # parameter datetime
    # output datetime in whole minutes
    def erase_seconds(self, t):
        return t - datetime.timedelta(seconds = t.second) - datetime.timedelta(microseconds = t.microsecond)

    # return tradingTime
    # TODO 修改random
    def random_trading_time(self, startIndex, maxIndex):
        return startIndex + int(random.random() * maxIndex), int(random.random()*60)


 

