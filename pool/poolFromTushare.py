# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolFromTushare.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 13:05
# Description: Pool get data from history (Tushare)
# ==============================================================================
import copy
import sys
sys.path.append("../common/")
import MarketData
from tradingUnit import tradingUnit
import copy
from tradingRecordRepo import tradingRecordRepo
sys.path.append("../fetch_data")
import repoFromTushare
sys.path.append("../tool")
from Log import Log

class poolFromTushare:
    def __init__(self, marketDataGetter, saveEngine):
        self.historyTradingList = []
        self.marketDataGetter = marketDataGetter
        self.saveEngine = saveEngine
        self.log = Log()
    
    def get_market_trading_data(self, time):
        # TODO 连上数据库
        price, amount = self.marketDataGetter.get_single_data(time.date(), time.time())
        return price, amount

    def trade_order(self, tradingUnit):
        self.log.info("trading unit: \n" + str(tradingUnit))
        # 这里完成的是市价单的操作
        # TODO 限价单
        nowTradingUnit = copy.deepcopy(tradingUnit)
        nowTradingUnit.isSuccess = True
        price, amount = self.get_market_trading_data(tradingUnit.time)
        nowTradingUnit.price = price
        self.saveEngine.save_record(nowTradingUnit)
        return nowTradingUnit

        

