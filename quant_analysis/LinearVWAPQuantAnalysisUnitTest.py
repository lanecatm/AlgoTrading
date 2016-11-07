# -*- encoding:utf-8 -*-


import time
import datetime
from LinearVWAPQuantAnalysis import LinearVWAPQuantAnalysis

class repoTest:
    def get_amount( self, startDate, endDate, startTime, endTime):
        return [[1,2,3,4]]*20
	#print startDate, endDate, startTime, endTime

if __name__ == '__main__':
    repoEngine = repoTest()

    LinearVWAPQuantAnalysis = LinearVWAPQuantAnalysis(repoEngine)
    startDate=datetime.datetime.strptime("2016-11-01 10:00:00" , "%Y-%m-%d %H:%M:%S")
    endDate = datetime.datetime.strptime("2016-10-30 13:00:00", "%Y-%m-%d %H:%M:%S")

    LinearVWAPQuantAnalysis.getRecommendOrderWeight(startDate, endDate, 1)
