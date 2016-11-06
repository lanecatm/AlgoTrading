# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: tradingUnit.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:06
# Description: 交易结构体
# ==============================================================================

class tradingUnit:
    def __init__(time, stockId, amount, isSuccess, price):
        self.time == time
        self.stockId = stockId
        self.amount = amount
        self.isSuccess = isSuccess
        self.price = price

