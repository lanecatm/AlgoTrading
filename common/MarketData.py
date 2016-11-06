# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: MarketData.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:38
# Description: marketdata 数据类
# ==============================================================================
import datetime

class MarketData:
    def __init__(self, originArr):
        #self.time
        self.buyPrice = []
        self.buyAmount = []
        self.sellPrice = []
        self.sellAmount = [] 
        for i in range(10, 20, 2):
            self.buyAmount.append(originArr[i])
            self.buyPrice.append(originArr[i+1])

        for i in range(20, 30, 2):
            self.sellAmount.append(originArr[i])
            self.sellPrice.append(originArr[i+1])

        
        self.time = datetime.datetime.strptime(originArr[-2] + originArr[-1], '"%Y-%m-%d""%H:%M:%S"')


