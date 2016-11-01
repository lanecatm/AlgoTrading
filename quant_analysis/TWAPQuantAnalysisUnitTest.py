# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: TWAPQuantAnalysisUnitTest.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: TWAP单元测试
# ==============================================================================
from TWAPQuantAnalysis import TWAPQuantAnalysis

if __name__ == '__main__':
    quantAnalysisEngine = TWAPQuantAnalysis()
    weightArr = quantAnalysisEngine.getRecommendOrderWeight(0, 100, 10)
    print weightArr
    weightArr[6] = 10
    print weightArr

