# -*- encoding:utf-8 -*-
# =============================================================================
# Filename: VWAPQuantAnalysis.py
# Author: Yuchang Xu
# Description: �򵥼�Ȩ����ƽ��VWAPʵ��
# ==============================================================================
from quantAnalysisBase import quantAnalysisBase
#from repo import get_amount
import sys
sys.path.append("../fetch_data")
import repo
import datetime
import numpy as np
class VWAPQuantAnalysis(quantAnalysisBase):
    def __init__(self, repoEngine):
        self.repoEngine = repoEngine
        return

    #def getHistoryData(self):
    #��ȡ��ʷ����
         
    
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval):
        #startTime=datetime.datetime.fromtimestamp(startTime)
	#endTime=datetime.datetime.fromtimestamp(endTime)
	ansWeightList = []
        historyDataList = []
        predictList = []
        startTimeList = []
        endTimeList = []
        n=datetime.timedelta(days=20)    #ȡ��������ƽ��
        delta = (endTime - startTime).days  #�µ���ʼ�ͽ���������
        startDate=startTime.date()
        endDate=startDate-n
        if delta == 0:   
        #������
            startTimeList.append(startTime.time())
            endTimeList.append(endTime.time())
        elif delta == 1:  
        #ֻ��һ��
            startTimeList.append(startTime.time())
            startTimeList.append(datetime.datetime.strptime('09:00:00', '%H:%M:%S').time())
            endTimeList.append(datetime.datetime.strptime('15:00:00', '%H:%M:%S').time())
            endTimeList.append(endTime.time())
        else:       
        #��һ������
            startTimeList.append(startTime.time())
            for i in range(delta-1):
                startTimeList.append(datetime.datetime.strptime('09:00:00', '%H:%M:%S').time())
                endTimeList.append(datetime.datetime.strptime('15:00:00', '%H:%M:%S').time())
            endTimeList.append(endTime.time())
        for j in range(len(startTimeList)):
            historyDataList = self.repoEngine.get_amount(startDate,endDate,startTimeList[j],endTimeList[j])
            tempDataList = zip(*historyDataList)
            lengthOfData = len(tempDataList)
            for i in range(lengthOfData):
                predictList.append(sum(tempDataList[i])/20.0)
        predictList = np.array(predictList)
        ansWeightList = predictList/sum(predictList)
	print ansWeightList
        return ansWeightList

