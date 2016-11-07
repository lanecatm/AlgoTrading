# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromSinaApiUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-07 20:03
# Description: unit test for pool
# ==============================================================================
import sys, datetime
from poolFromSinaApi import poolFromSinaApi
sys.path.append("../common/")
import MarketData
from tradingUnit import tradingUnit
sys.path.append("../tool")
from Log import Log

log = Log()

class mockMarketDataGetter:
    def get_data(self):
        arr = [0]*32
        arr[10] = 10
        log.info("mockMarketData " + str(arr))
        return arr


if __name__ == "__main__":
    mockMarket = mockMarketDataGetter()
    pool = poolFromSinaApi(mockMarket)
    testUnit = tradingUnit(orderId = 1, time = datetime.datetime.now(), stockId = 10001, amount = 100, isSuccess = None, price = None, buysell = True)

    pool.trade_order(testUnit)
