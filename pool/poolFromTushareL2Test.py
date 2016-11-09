# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromTushareL2Test.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-09 11:21
# Description: pool and repo test
# ==============================================================================
import datetime
from poolFromTushare import poolFromTushare
from tradingRecordRepo import tradingRecordRepo
import sys
sys.path.append("../tool")
from Log import Log
sys.path.append("../common/")
from tradingUnit import tradingUnit
sys.path.append("../fetch_data")
from repoFromTushare import repoFromTushare

if __name__ == "__main__":
    log = Log()
    marketGetter = repoFromTushare()
    saveEngine = tradingRecordRepo("test_trading_record.db")
    tradingRecord = tradingUnit(orderId = 0, stockId = 0, buysell = False, amount = 1000, price = None, isSuccess = False,time = datetime.datetime.strptime("2016-10-14 14:00:00", "%Y-%m-%d %H:%M:%S"))
    log.info(tradingRecord.toString())
    pool = poolFromTushare(marketGetter, saveEngine)
    tradingRecord = pool.trade_order(tradingRecord)
    log.info(tradingRecord.toString())


