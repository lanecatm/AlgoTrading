# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: quantAnalysisBase.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: the base class
# ==============================================================================
# 模拟抽象类
def abstract():
    raise NotImplimentedError("Abstract")

class quantAnalysisBase:
    def __init__(self):
        abstract()
        return

    def getHistoryData(self):
        # 获取历史数据
        # list<value, amount>
        abstract()
        return

    def analysisHistoryData(self):
        abstract()
        return
    
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval):
        abstract()
        return
