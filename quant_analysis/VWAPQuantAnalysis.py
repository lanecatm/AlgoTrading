# -*- encoding:utf-8 -*-
# =============================================================================
# Filename: VWAPQuantAnalysis.py
# Author: Yuchang Xu
# Description: �򵥼�Ȩ����ƽ��VWAPʵ��
# ==============================================================================
from quantAnalysisBase import quantAnalysisBase
from repo import get_amount
import datetime
import numpy as np
class VWAPQuantAnalysis(quantAnalysisBase):
    def __init__(self):
        return

    def getHistoryData(self):
    #��ȡ��ʷ����
         
    
    def getRecommendOrderWeight(self, startTime, endTime, timeInterval):
        ansWeightList = []
        historyDataList = []
        predictList = []
        startTimeList = []
        endTimeList = []
        n=datetime.timedelta(days=20)    #ȡ��������ƽ��
        delta=(endTime-startTime).days  #�µ���ʼ�ͽ���������
        startDate=startTime.date()
        endDate=startDate-n
        if delta == 0:   
        #������
            startTimeList.append(startTime.time())
            endTimeList.append(endTime.time())
        else if delta == 1:  
        #ֻ��һ��
            startTimeList.append(startTime.time())
            startTimeList.append(datetime.datetime.strptime('09:00:00', '%H:%M:%S').time())
            endTimeList.append(datetime.datetime.strptime('15:00:00', '%H:%M:%S').time())
            endTimeList.append(endTime.time())
        else:       
        #��һ������
            startTimeList.append(startTime.time())
            for i in range(delta-1):
                startTimeList.append(datetime.datetime.strptime('09:00:00', '%H:%M:%S').time()))
                endTimeList.append(datetime.datetime.strptime('15:00:00', '%H:%M:%S').time())
            endtimeList.append(endTime.time())
        for j in range(len(startTime)):
            historyDataList = get_amount(startDate,endDate,startTime[j],endTime[j])
            tempDataList = zip(*historyDataList)
            lengthOfData = len(tempDataList)
            for i in range(lengthOfData):
                predictList.append(sum(tempDataList[i])/20.0)
        predictList = np.array(predictList)
        ansWeightList = predictList/sum(predictList)
        return ansWeightList

