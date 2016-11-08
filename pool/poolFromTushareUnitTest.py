# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromTushareUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-08 00:36
# Description: unit test for pool
# ==============================================================================
import datetime
from poolFromTushare import poolFromTushare
from tradingRecordRepo import tradingRecordRepo
import sys
sys.path.append("../tool")
from Log import Log
sys.path.append("../common/")
from tradingUnit import tradingUnit
class mockMarketDataGetter:
    def get_data(self):
        return 20.0, 100

if __name__ == "__main__":
    log = Log()
    marketGetter = mockMarketDataGetter()
    saveEngine = tradingRecordRepo("test_trading_record.db")
    tradingRecord = tradingUnit(orderId = 0, stockId = 0, buysell = False, amount = 1000, price = None, isSuccess = False,time = datetime.datetime.now())
    log.info(str(tradingRecord))
    pool = poolFromTushare(marketGetter, saveEngine)
    tradingRecord = pool.trade_order(tradingRecord)
    log.info(str(tradingRecord))


