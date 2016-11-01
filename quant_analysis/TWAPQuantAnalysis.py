# -*- encoding:utf-8 -*-
# ==============================================================================
# Filename: TWAPQuantAnalysis.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: TWAP实现
# ==============================================================================
from quantAnalysisBase import quantAnalysisBase
class TWAPQuantAnalysis(quantAnalysisBase):
    def __init__(self):
        return
    
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval):
        ansWeightList = []
        tradingTimes = (endTime - startTime)/timeInterval
        weight = 1.0 / tradingTimes         
        ansWeightList = [weight] * tradingTimes
        return ansWeightList

