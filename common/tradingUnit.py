# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: TradingUnit.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:06
# Description: 交易结构体
# ==============================================================================

class tradingUnit:
    # attribute: buy True, sell False
    def __init__(self, orderId, stockId, buysell, amount, price, isSuccess,time):
        self.time = time
        self.stockId = stockId
        self.amount = amount
        self.buysell = buysell
        self.isSuccess = isSuccess
        self.price = price
        self.orderId = orderId

