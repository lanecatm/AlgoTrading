
# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: MarketDataUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 12:45
# Description: marketdata 单元测试
# ==============================================================================
import datetime
from MarketData import MarketData
import sys
sys.path.append("../fetch_data/")
import getData

if __name__=='__main__':
    originArr = getData.getData()
    marketData = MarketData(originArr)
    print marketData.sellPrice
    print marketData.sellAmount
    print marketData.buyPrice
    print marketData.buyAmount
    print marketData.time

