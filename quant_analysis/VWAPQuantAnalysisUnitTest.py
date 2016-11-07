
# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: VWAPQuantAnalysisUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-04 16:00
# Description: VWAPQuantAnalysis单元测试
# ==============================================================================
import time
import datetime
import numpy as np
from VWAPQuantAnalysis import VWAPQuantAnalysis

class repoTest:
    def get_amount( self, startDate, endDate, startTime, endTime):
        print startDate, endDate, startTime, endTime
        return np.array([[1,2,3,4]]*20)

if __name__ == '__main__':
    repoEngine = repoTest()

    VWAPAnalysis = VWAPQuantAnalysis(repoEngine)
    startDate=datetime.datetime.strptime("2016-11-01 10:00:00" , "%Y-%m-%d %H:%M:%S")
    endDate = datetime.datetime.strptime("2016-10-31 13:00:00", "%Y-%m-%d %H:%M:%S")

    VWAPAnalysis.getRecommendOrderWeight(startDate, endDate, 1)
    
    VWAPAnalysis.getRecommendOrderWeight(startDate, startDate + datetime.timedelta(hours = 10), 1)
