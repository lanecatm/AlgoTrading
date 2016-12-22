# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: MarketData.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-06 10:38
# Description: marketdata 数据类
# ==============================================================================
import datetime
import sys
sys.path.append("../tool")
from Log import Log
class MarketData:
    # 这个类可能由数据库挖出的东西初始化,也可能用直接从爬下来的数据字符串数组初始化
    def __init__(self, originArr):
        self.log = Log()
        # TODO 添加stockId的传入
        # stockId int
        if isinstance(originArr[0], str):
            self.stockId = int(originArr[0])
        else:
            self.stockId = originArr[0]
        #self.time
        self.buyPrice = []
        self.buyAmount = []
        self.sellPrice = []
        self.sellAmount = [] 
        for i in range(10, 20, 2):
            if isinstance(originArr[i], str):
                self.buyAmount.append(int(originArr[i]))
                self.buyPrice.append(float(originArr[i+1]))
            else:
                self.buyAmount.append(originArr[i])
                self.buyPrice.append(originArr[i+1])

        for i in range(20, 30, 2):
            if isinstance(originArr[i], str):
                self.sellAmount.append(int(originArr[i]))
                self.sellPrice.append(float(originArr[i+1]))
            else:
                self.sellAmount.append(originArr[i])
                self.sellPrice.append(originArr[i+1])

        
        self.log.info("date from arr:" + str(originArr[-2]))
        self.log.info("time from arr:" + str(originArr[-1]))
        self.time = datetime.datetime.strptime(originArr[-2] + originArr[-1], '"%Y-%m-%d""%H:%M:%S"')

    def __str__(self):
        return "stock id: " + str(self.stockId) + " time " + str(self.time) + " buyarr " + str(self.buyPrice) + str(self.buyAmount) + " sellarr " + str(self.sellPrice) + str(self.sellAmount)


