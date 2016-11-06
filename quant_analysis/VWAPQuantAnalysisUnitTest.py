
# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: VWAPQuantAnalysisUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-04 16:00
# Description: VWAPQuantAnalysis单元测试
# ==============================================================================
import time
#import datetime
from VWAPQuantAnalysis import VWAPQuantAnalysis

class repoTest:
    def get_amount(self, startDate, endDate, startTime, endTime):
        print startDate, endDate, startTime, endTime

if __name__ == '__main__':
    repoEngine = repoTest

    VWAPAnalysis = VWAPQuantAnalysis(repoEngine)
    startDate= time.strptime("2016-11-01 10:00:00" , "%Y-%m-%d %H:%M:%S")
    endDate = time.strptime("2016-10-10 13:00:00", "%Y-%m-%d %H:%M:%S")

    VWAPAnalysis.getRecommendOrderWeight(startDate, endDate, 1)
    
