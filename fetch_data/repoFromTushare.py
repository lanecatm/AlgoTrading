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

class repoFromTushare(object):     
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


    def get_amount(self, startdate, enddate, starttime, endtime):          
        self.log.info(str(startdate) + str(enddate) + str(starttime) + str(endtime))
        sql = """select date_tick,minu_tick,pric_tick, volu_tick from tickdata where code_tick like "600000" and date_tick in ("2013-10-24" , "2013-10-23") and minu_tick in ("09'43" , "09'00")"""

        self.cur.execute(sql)
        results = self.cur.fetchall()   
        datenumber, totalfilterdatelist = self.getTotalDateString(startdate, enddate)
        minutenumber, totalfilterminute = self.getTotalMinuteString(starttime, endtime)

        #create the numpy array to store data
        resultsarray = np.zeros((datenumber,minutenumber)) 
        resultsarray = resultsarray.astype(np.float)      

        for dateindex in range(len(totalfilterdatelist)):
            sql = "select date_tick,minu_tick,pric_tick, amou_tick from tickdata where code_tick like \"600000\" and date_tick like \""+ totalfilterdatelist[dateindex] +"\" and minu_tick in " + totalfilterminute + "  ORDER BY minu_tick asc"
            self.log.info(sql)
            self.cur.execute(sql)
            results = self.cur.fetchall()   
            if(results!=()): #
                for minuindex in range(len(results)):
                    self.log.info("get_amount time:" + str(results[minuindex][0:2]))
                    self.log.info("amount:" + str(results[minuindex][3]))
                    #tmpstring = results[minuindex][0] + " "+results[minuindex][1]+" "+ str(results[minuindex][2])+" "+str(results[minuindex][3])
                    tmpstring = results[minuindex][3]
                    resultsarray[dateindex][minuindex] = tmpstring

        self.log.info("get_amount:\n" + str(resultsarray))
        return resultsarray

    def get_price(self, startdate, enddate, starttime, endtime):          
        datenumber, totalfilterdatelist = self.getTotalDateString(startdate, enddate)
        minutenumber, totalfilterminute = self.getTotalMinuteString(starttime, endtime)
        #create the numpy array to store data
        resultsarray = np.zeros((datenumber,minutenumber)) 
        resultsarray = resultsarray.astype(np.float)      

        for dateindex in range(len(totalfilterdatelist)):
            sql = "select date_tick,minu_tick,pric_tick, amou_tick from tickdata where code_tick like \"600000\" and date_tick like \""+ totalfilterdatelist[dateindex] +"\" and minu_tick in " + totalfilterminute    
            self.log.info(sql)
            self.cur.execute(sql)
            results = self.cur.fetchall()   
            if(results!=()): #
                for minuindex in range(len(results)):
                    tmpstring = results[minuindex][2]
                    resultsarray[dateindex][minuindex] = tmpstring
        self.log.info("get_price:\n" + str(resultsarray))
        return resultsarray


    def get_single_data(self, currentDate, currentMinu):
        currentDate = currentDate.strftime("%Y-%m-%d")
        currentMinu = datetime.datetime.strptime(currentMinu.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S").strftime("%H'%M")
        self.log.info("get_single_data time: " + currentDate + ", " + currentMinu)
        SQL = "select date_tick,minu_tick,pric_tick, volu_tick from tickdata WHERE code_tick like \"600000\" AND date_tick like \"" + currentDate + "\"  AND minu_tick like \"" + currentMinu + "\""
        self.log.info(SQL)
        self.cur.execute(SQL)
        results = self.cur.fetchall()   
        if(results!=()): #
            return results[0][2], results[0][3]
        else:
            return 0, 0


# unittest
if __name__=="__main__":
    getter = fetchStockMinuData()
    getter.getTotalDateString(datetime.datetime.strptime("2016-10-12", "%Y-%m-%d").date(),datetime.datetime.strptime("2016-10-10", "%Y-%m-%d").date())
    getter.getTotalMinuteString(datetime.datetime.strptime("03:00:00", "%H:%M:%S").time(),datetime.datetime.strptime("08:00:00", "%H:%M:%S").time())
    
