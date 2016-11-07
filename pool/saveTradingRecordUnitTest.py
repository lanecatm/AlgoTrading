# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: saveTradingRecord.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-07 21:18
# Description: save each trade record unit test
# ==============================================================================
from saveTradingRecord import saveTradingRecord
import sys
sys.path.append("../common/")
from tradingUnit import tradingUnit
import datetime
sys.path.append("../tool/")
from Log import Log

if __name__ == "__main__":
    savingEngine = saveTradingRecord("test_trading_record.db")
    tradingRecord = tradingUnit(orderId = 0, stockId = 0, buysell = False, amount = 1000, price = 1000, isSuccess = False,time = datetime.datetime.now())
    savingEngine.save_record(tradingRecord)



    
