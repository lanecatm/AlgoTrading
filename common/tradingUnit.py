# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: TradingUnit.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:06
# Description: 交易结构体
# ==============================================================================
import datetime
class tradingUnit:
    self.BUY = 0
    self.SELL = 1
    self.LIMITE_PRICE_ORDER = 0
    self.FIRST_PRICE_ORDER = 1
    self.ALL_PRICE_ORDER = 2
    def __init__(self, tradingUnitId, stockId, time, buysell, isSync, tradingType, amount, expectPrice = None):
        # 交易单号
        self.tradingUnitId= tradingUnitId
        # 交易的股票id
        self.stockId = stockId
        # 发送交易订单时间
        self.time = time
        # 买股票还是卖股票
        self.buysell = buysell
        # 同步还是异步
        self.isSync = isSync
        # 交易类型
        self.tradingType = tradingType
        # 交易的股票数量
        self.amount = amount
        # 如果是限价单，那么限制交易的价格是
        self.expectPrice = expectPrice
        # 交易是否成功
        self.isSuccess = False
        # 交易成功量
        self.succAmount = 0
        # 交易用去总花费
        self.succMoney = 0
        # 交易平均每股价格
        self.price = 0

    def refresh_order(self, amount, money, isSuccess):
        self.succAmount = amount
        self.succMoney = momey
        self.price = money / amount
        self.isSuccess = isSuccess

    def toString(self):
        tradingInputInfo = " tradingUnitId " + str(self.tradingUnitId) + " stockId " + str(self.stockId) + " time " + self.time.strftime("%Y-%m-%d %H:%M:%S") + " amount " + str(self.amount) + " expect price " + str(expectPrice)
        tradingAttribute = " buysell " + str(self.buysell) + " isSync " + str(self.isSync) + " tradingType" + str(self.tradingType)
        tradingResult = " isSucc " + str(self.isSuccess) + " succ amount " + str(self.succAmount) + " succ momey " + str(self.succMoney) + " price " + str(self.price)
        return tradingInputInfo + tradingAttribute + tradingResult

