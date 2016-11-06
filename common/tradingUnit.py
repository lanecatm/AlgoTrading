# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: TradingUnit.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:06
# Description: 交易结构体
# ==============================================================================

class TradingUnit:
    # attribute: buy True, sell False
    def __init__(self, time, stockId, amount, isSuccess, price, buysell):
        self.time == time
        self.stockId = stockId
        self.amount = amount
        self.buysell = buysell
        self.isSuccess = isSuccess
        self.price = price

