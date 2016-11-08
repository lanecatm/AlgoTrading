# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:52:15 2016

@author: Panh
"""

#import pymysql
import MySQLdb as pymysql
import calendar
import numpy as np
import datetime
import time
import sys
sys.path.append("../tool")
from Log import Log

IPADDRESS = "192.168.191.1"
USER = "client"
PASSWORD = "123456"

class fetchStockMinuData(object):     
    def __init__(self):
        self.conn = pymysql.connect(host = IPADDRESS, user = USER, passwd = PASSWORD, port = 3306, charset = 'utf8',  db = 'stockamount')
        self.cur = self.conn.cursor()
        self.log = Log()

    def getTotalDateString(self,startDate, endDate):
        datenumber = (startDate - endDate).days
        totalFilterDateList = []
        for i in range(datenumber):
            days = datetime.timedelta(days=i)
            dateTmp = (startDate - days).strftime("%Y-%m-%d")
            self.log.info(str(dateTmp))
            totalFilterDateList.append(dateTmp)
        self.log.info("date number:" + str(datenumber))
        self.log.info("date list:" + str(totalFilterDateList))
        return datenumber, totalFilterDateList


    def getTotalMinuteString(self, startTime, endTime):
        endTime = datetime.datetime.strptime(endTime.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        startTime = datetime.datetime.strptime(startTime.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        self.log.info("starttime:" + str(startTime))
        self.log.info("endtime:" + str(endTime))
        minutenumber = (endTime - startTime).seconds / 60
        self.log.info(str(minutenumber))
        totalFilterMinu = "("
        for i in range(minutenumber):
            minutes = datetime.timedelta(minutes = i)
            minuteTmp = startTime + minutes
            if i < minutenumber - 1:
                totalFilterMinu = totalFilterMinu + "\"" + minuteTmp.strftime("%H'%M")+ "\", "
            else:
                totalFilterMinu = totalFilterMinu + "\"" + minuteTmp.strftime("%H'%M")+ "\""

        totalFilterMinu = totalFilterMinu + ")"
        self.log.info("minutenumber:" + str(minutenumber))
        self.log.info("totalFilterMinu" + str(totalFilterMinu))
        return minutenumber, totalFilterMinu


    def fetchData(self, startDate, endDate, startTime, endTime):          
        self.log.info(str(startDate) + str(endDate) + str(startTime) + str(endTime))
        SQL = """select date_tick,minu_tick,pric_tick, volu_tick from tickdata WHERE code_tick like "600000" AND date_tick in ("2013-10-24" , "2013-10-23") AND minu_tick in ("09'43" , "09'00")"""

        self.cur.execute(SQL)
        results = self.cur.fetchall()   

        #startDate = "2016-10-20" #smaller
        #endDate = "2016-10-24"  #bigger
        #startTime = "13'00"  #smaller
        #endTime = "14'59"  #bigger

        dateNumber, totalFilterDateList = self.getTotalDateString(startDate, endDate)
        minuteNumber, totalFilterMinute = self.getTotalMinuteString(startTime, endTime)

        #create the numpy array to store data
        resultsArray = np.zeros((dateNumber,minuteNumber)) 
        resultsArray = resultsArray.astype(np.str)      

        for dateIndex in range(len(totalFilterDateList)):
            SQL = """select date_tick,minu_tick,pric_tick, amou_tick from tickdata WHERE code_tick like "600000" AND date_tick like """+ totalFilterDateList[dateIndex] +""" AND minu_tick in """ + totalFilterMinute    
            self.log.info(SQL)
            self.cur.execute(SQL)
            results = self.cur.fetchall()   
            #print (results)
            #print (len(results))
            if(results!=()): #
                for minuIndex in range(len(results)):
                    #for minuIndex in range(minuteNumber):
                    #tmpstring = results[minuIndex][0] + " "+results[minuIndex][1]+" "+ str(results[minuIndex][2])+" "+str(results[minuIndex][3])
                    tmpstring = results[minuIndex][3]
                    resultsArray[dateIndex][minuIndex] = tmpstring

        #print (resultsArray)
        return resultsArray

    def fetchSingleData(self, currentDate, currentMinu):
        currentDate = "2016-10-11" #smaller
        currentMinu = "10'05"  #smaller
        SQL = """select date_tick,minu_tick,pric_tick, volu_tick from tickdata WHERE code_tick like "600000" AND date_tick like '""" + currentDate + """'  AND minu_tick like \"""" + currentMinu + "\""
        self.cur.execute(SQL)
        results = self.cur.fetchall()   
        #print (results[0])
        return results[0]


# unittest
if __name__=="__main__":
    getter = fetchStockMinuData()
    getter.getTotalDateString(datetime.datetime.strptime("2016-10-12", "%Y-%m-%d").date(),datetime.datetime.strptime("2016-10-10", "%Y-%m-%d").date())
    getter.getTotalMinuteString(datetime.datetime.strptime("03:00:00", "%H:%M:%S").time(),datetime.datetime.strptime("08:00:00", "%H:%M:%S").time())
    
