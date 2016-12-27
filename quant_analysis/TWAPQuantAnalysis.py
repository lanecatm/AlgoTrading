# -*- encoding:utf-8 -*-
# ==============================================================================
# Filename: TWAPQuantAnalysis.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: TWAP实现
# ==============================================================================
import sys
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
from quantAnalysisBase import quantAnalysisBase

class TWAPQuantAnalysis(quantAnalysisBase):
    def __init__(self, isOpenLog = True):
        self.log = Log(isOpenLog)
        return
    
    # 包含开始，不包含结束时间
    def find_trading_time(self, startTime, endTime):
        self.log.info("find_trading_time: " + startTime.isoformat() + " " +endTime.isoformat())
        timeList = []
        timeDelta = (endTime - startTime).total_seconds()
        self.log.info("during hours: " + str(timeDelta / 3600))
        for secondOffset in range(0, int(timeDelta), 60):
            nowTime = startTime + datetime.timedelta(seconds = secondOffset)
            #self.log.info("nowtime " + nowTime.isoformat())
            if nowTime.date().isoweekday() < 6:
                if (nowTime.time() >= datetime.time(9,30) and nowTime.time() <= datetime.time(11,30)) or (nowTime.time() >= datetime.time(13,0) and nowTime.time() <= datetime.time(15,0)):
                    timeList.append(nowTime.strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info("timeList" + str(timeList))
        return timeList


    def get_recommend_order_weight(self, stockId, startTime, endTime, findLastDays):
        ansWeightList = []
        # 检查可以交易的时间点
        tradingTimeList = self.find_trading_time(startTime, endTime)
        tradingTimes = len(tradingTimeList)
        if tradingTimes == 0:
            return {}
        weight = 1.0 / tradingTimes         
        ansWeightList = [weight] * tradingTimes
        self.log.info("ansWeightList:" + str(ansWeightList))
        return self.format_output(np.array(ansWeightList), np.array(tradingTimeList), startTime.date())

