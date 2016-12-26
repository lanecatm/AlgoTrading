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
    BUY = 0
    SELL = 1
    LIMITE_PRICE_ORDER = 0
    FIRST_PRICE_ORDER = 1
    ALL_PRICE_ORDER = 2


    # param tradingUnitId int
    # param stockId int
    # param time datetime
    # param buysell bool
    # param isSync bool
    # param tradingType int
    # param amount int
    # param expectPrice double
    # 请不要输入字任何符串
    def __init__(self, tradingUnitId, stockId, time, buysell, isSync, tradingType, amount, expectPrice = None):
        # 交易单号 大单号
        self.tradingUnitId= tradingUnitId
        # 交易的股票id int
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

    # param amount int
    # param money double
    # param isSuccess bool
    def refresh_order(self, amount, money, isSuccess):
        self.succAmount = amount
        self.succMoney = money
        if amount == 0:
            self.price = 0
        else:
            self.price = money / amount
        self.isSuccess = isSuccess

    def toString(self):
        tradingInputInfo = " tradingUnitId " + str(self.tradingUnitId) + " stockId " + str(self.stockId) + " time " + self.time.strftime("%Y-%m-%d %H:%M:%S") + " amount " + str(self.amount) + " expect price " + str(self.expectPrice)
        tradingAttribute = " buysell " + str(self.buysell) + " isSync " + str(self.isSync) + " tradingType" + str(self.tradingType)
        tradingResult = " isSucc " + str(self.isSuccess) + " succ amount " + str(self.succAmount) + " succ momey " + str(self.succMoney) + " price " + str(self.price)
        return tradingInputInfo + tradingAttribute + tradingResult

    def __str__(self):
        return self.toString()
