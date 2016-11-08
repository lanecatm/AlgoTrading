
# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: quantAnalysisL2Test.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-08 21:38
# Description: quantAnalysis 集成测试
# ==============================================================================
import sys
sys.path.append("../fetch_data")
import datetime
import numpy as np
from VWAPQuantAnalysis import VWAPQuantAnalysis
from repoFromTushare import repoFromTushare


if __name__ == '__main__':
    repoEngine = repoFromTushare()

    VWAPAnalysis = VWAPQuantAnalysis(repoEngine)
    startDate=datetime.datetime.strptime("2016-10-21 13:00:00" , "%Y-%m-%d %H:%M:%S")
    endDate = datetime.datetime.strptime("2016-10-21 14:06:00", "%Y-%m-%d %H:%M:%S")

    VWAPAnalysis.getRecommendOrderWeight(startDate, endDate, 1)
    
    VWAPAnalysis.getRecommendOrderWeight(startDate, startDate + datetime.timedelta(hours = 10), 1)
