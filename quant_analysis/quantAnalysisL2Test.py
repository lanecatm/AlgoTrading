
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
from repo import repo
from VWAPQuantAnalysis import VWAPQuantAnalysis


if __name__ == '__main__':
    repoEngine = repo(False, True , None, "algotrading", "12345678", None)

    VWAPAnalysis = VWAPQuantAnalysis(repoEngine)
    startDate=datetime.datetime.strptime("2016-12-15 13:00:00" , "%Y-%m-%d %H:%M:%S")
    endDate = datetime.datetime.strptime("2016-12-16 14:06:00", "%Y-%m-%d %H:%M:%S")

    ansDict = VWAPAnalysis.get_recommend_order_weight(600000, startDate, endDate, 2)
    ansDict = sorted(ansDict.iteritems(), key=lambda keyValue: datetime.datetime.strptime(keyValue[0], "%Y-%m-%d %H:%M:%S"), reverse = True)
    print ansDict
    
    #VWAPAnalysis.getRecommendOrderWeight(startDate, startDate + datetime.timedelta(hours = 10), 1)
