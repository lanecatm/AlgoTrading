# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 16:52:15 2016

@author: Panh
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:03:16 2016

@author: Panh
"""

#import pymysql
import MySQLdb as pymysql
import calendar
import numpy as np

IPADDRESS = "192.168.191.1"
USER = "client"
PASSWORD = "123456"
class fetchStockMinuData(object):     
    def __init__(self):
        self.conn = pymysql.connect(host = IPADDRESS, user = USER, passwd = PASSWORD, port = 3306, charset = 'utf8',  db = 'stockamount')
        self.cur = self.conn.cursor()

    def getDateLength(self,year):
        if(calendar.isleap(year)==True):
            datelist = [31,29,31,30,31,30,31,31,30,31,30,31]  
        else:
            datelist = [31,28,31,30,31,30,31,31,30,31,30,31]
        return datelist

    def getTotalDateString(self,startDate, endDate):
        totalFilterDate = "("
        tmpStartDate = startDate.split("-")
        tmpEndDate = endDate.split("-")
        datenumber = 0
        totalFilterDateList = []
        
        if(int(tmpStartDate[0])<int(tmpEndDate[0])):
            totalFilterDate = totalFilterDate+ '"' + startDate + '"'
            totalFilterDateList.append('"' + startDate + '"')
            datenumber+=1
            datelength = self.getDateLength(int(tmpStartDate[0]))
            for dayindex in range(int(tmpStartDate[2])+1, datelength[int(tmpStartDate[1])]):
                datenumber+=1
                totalFilterDate = totalFilterDate + ", " + '"' +tmpStartDate[0]+'-'+tmpStartDate[1]+'-'+str(dayindex)+'"'
                totalFilterDateList.append('"' +tmpStartDate[0]+'-'+tmpStartDate[1]+'-'+str(dayindex)+'"')            
                
            for mouthindex in range(int(tmpStartDate[1]), 12):
                for dayindex in range(1, datelength[mouthindex]+1):
                    datenumber+=1
                    totalFilterDate = totalFilterDate + ", " + '"' +tmpStartDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"'
                    totalFilterDateList.append('"' +tmpStartDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"')
        
            if ((int(tmpEndDate[0])-int(tmpStartDate[0]))>1):
                for yearindex in range(int(tmpStartDate[0])+1, int(tmpEndDate[0])+1):
                    datelength = self.getDateLength(yearindex)
                    for mouthindex in range(0,12):
                        for dayindex in range(1, datelength[mouthindex]+1):
                            datenumber+=1
                            totalFilterDate = totalFilterDate + ", " + '"' +tmpStartDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"'
                            totalFilterDateList.append('"' +tmpStartDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"')
            else:
                datelength = self.getDateLength(int(tmpEndDate[0]))
                for mouthindex in range(0,int(tmpEndDate[1])):
                    for dayindex in range(1, datelength[mouthindex]+1):
                        datenumber+=1
                        totalFilterDate = totalFilterDate + ", " + '"' +tmpEndDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"'
                        totalFilterDateList.append('"' +tmpEndDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"')
          
        if(int(tmpStartDate[0])==int(tmpEndDate[0])):
            totalFilterDate = totalFilterDate+ '"' + startDate + '"'
            datenumber+=1
            datelength = self.getDateLength(int(tmpStartDate[0]))
            if(int(tmpStartDate[1])<int(tmpEndDate[1])): 
                for dayindex in range(int(tmpStartDate[2])+1, datelength[int(tmpStartDate[1])]+1):
                    datenumber+=1
                    totalFilterDate = totalFilterDate + ", " + '"' +tmpEndDate[0]+'-'+tmpStartDate[1]+'-'+str(dayindex)+'"'
                    totalFilterDateList.append('"' +tmpEndDate[0]+'-'+tmpStartDate[1]+'-'+str(dayindex)+'"')
                
                if((int(tmpEndDate[1])-int(tmpStartDate[1]))>1):
                    for mouthindex in range(int(tmpStartDate[1]),int(tmpEndDate[1])):
                        for dayindex in range(1, datelength[mouthindex]+1):
                            datenumber+=1
                            totalFilterDate = totalFilterDate + ", " + '"' +tmpEndDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"'
                            totalFilterDateList.append('"' +tmpEndDate[0]+'-'+str(mouthindex)+'-'+str(dayindex)+'"')
                else:
                    for dayindex in range(1, int(tmpEndDate[2])+1):
                        datenumber+=1
                        totalFilterDate = totalFilterDate + ", " + '"' +tmpEndDate[0]+'-'+tmpEndDate[1]+'-'+str(dayindex)+'"'
                        totalFilterDateList.append('"' +tmpEndDate[0]+'-'+tmpEndDate[1]+'-'+str(dayindex)+'"')
                                            
            if(int(tmpStartDate[1])==int(tmpEndDate[1])):
                for dayindex in range(int(tmpStartDate[2])+1,int(tmpEndDate[2])+1):
                    datenumber+=1
                    totalFilterDate = totalFilterDate + ", " + '"' +tmpEndDate[0]+'-'+tmpEndDate[1]+'-'+str(dayindex)+'"'
                    totalFilterDateList.append('"' +tmpEndDate[0]+'-'+tmpEndDate[1]+'-'+str(dayindex)+'"')
                        
        totalFilterDate = totalFilterDate + ")"
        
        #print (datenumber)
        #print (totalFilterDate)
        return datenumber,totalFilterDate,totalFilterDateList
    
    
    def getTotalMinuteString(self, startTime, endTime):
        totalFilterMinu = "("
        tmpStart = startTime.split("'")  #[0]=hour, [1]=minute
        tmpEnd = endTime.split("'")
        minutenumber = 0
        
        if(int(tmpStart[0])<int(tmpEnd[0])):
            totalFilterMinu = totalFilterMinu + '"' +startTime + '"'
            minutenumber+=1
            for minuteindex in range(int(tmpStart[1])+1,60):
                minutenumber+=1
                totalFilterMinu = totalFilterMinu + ", "+ '"' +(tmpStart[0]).zfill(2) + "'" + (str(minuteindex)).zfill(2) + '"' 
            
            if((int(tmpEnd[0])-int(tmpStart[0]))>1):
                for hourindex in range(int(tmpStart[0])+1,tmpEnd[0]):
                    for minuteindex in range(0,60):
                        minutenumber+=1
                        totalFilterMinu = totalFilterMinu + ", "+ '"' +(str(hourindex)).zfill(2) + "'" + (str(minuteindex)).zfill(2) + '"' 
            else:
                for minuteindex in range(0,int(tmpEnd[1])):
                    minutenumber+=1
                    totalFilterMinu = totalFilterMinu + ", "+ '"' +(tmpEnd[0]).zfill(2) + "'" + (str(minuteindex)).zfill(2) + '"' 
        
        totalFilterMinu = totalFilterMinu + ")"
        
        #print (minutenumber)
        #print (totalFilterMinu)
        return minutenumber, totalFilterMinu

    
    def fetchData(self, startDate, endDate, startTime, endTime):          
        print startDate, endDate, startTime, endTime
        SQL = """select date_tick,minu_tick,pric_tick, volu_tick from tickdata WHERE code_tick like "600000" AND date_tick in ("2013-10-24" , "2013-10-23") AND minu_tick in ("09'43" , "09'00")"""
    
        self.cur.execute(SQL)
        results = self.cur.fetchall()   
        #print (results)
        
        #startDate = "2016-10-20" #smaller
        #endDate = "2016-10-24"  #bigger
        #startTime = "13'00"  #smaller
        #endTime = "14'59"  #bigger
        
        dateNumber, totalFilterDate, totalFilterDateList = self.getTotalDateString(startDate, endDate)
        minuteNumber, totalFilterMinute = self.getTotalMinuteString(startTime, endTime)
           
        #create the numpy array to store data
        resultsArray = np.zeros((dateNumber,minuteNumber)) 
        resultsArray = resultsArray.astype(np.str)      
           
        #print ("---------------------------------------------------------------------------")
        for dateIndex in range(len(totalFilterDateList)):
        #index = 0
        #SQL = """select date_tick,minu_tick,amou_tick from stockdata WHERE code_tick like "600000" AND date_tick in """+totalFilterDate +""" AND minu_tick in """ + totalFilterMinute
            SQL = """select date_tick,minu_tick,pric_tick, amou_tick from tickdata WHERE code_tick like "600000" AND date_tick like """+ totalFilterDateList[dateIndex] +""" AND minu_tick in """ + totalFilterMinute    
            print SQL
            self.cur.execute(SQL)
            results = self.cur.fetchall()   
            #print (results)
            #print (len(results))
            if(results!=()): #
                for minuIndex in range(len(results)):
                #for minuIndex in range(minuteNumber):
                    tmpstring = results[minuIndex][0] + " "+results[minuIndex][1]+" "+ str(results[minuIndex][2])+" "+str(results[minuIndex][3])
                    resultsArray[dateIndex][minuIndex] = tmpstring
        
        #print (resultsArray)
        return resultsArray
    




"""
# 获取股票的成交数量
    # @param startDate dateTime 从哪一天开始(较大的天数，包含)
    # @param endDate dateTime 到哪一天结束(较小的天数，不包含)
    # @param startTime time 每一天中的开始时间(包含这一刻)
    # @param endTime time 每一天中的结束时间(不包含这一刻)
    # @return  np.array
    #          [[amount1, amount2, ..., amountn],
    #          [amount1, amount2, ..., amountn],
    #          ...                             
    #          ]
    # For Example
    # startDate = 10.5 endDate = 10.2 startTime = 13:00 endTime = 15:00
    # return [[10.5 13:00 amount, 10.5 13:01 amount, 10.5 13:02 amount, ..., 10.5 14:59 amount],
    #         [10.4 13:00 amount, 10.4 13:01 amount, 10.4 13:02 amount, ..., 10.4 14:59 amount],
    #         [10.3 13:00 amount, 10.3 13:01 amount, 10.3 13:02 amount, ..., 10.3 14:59 amount]]
    def get_amount(self, startDate, endDate, startTime, endTime):
        statement = "SELECT SUCCNUM FROM main.history_stock_info WHERE DATETIME(NOWDATE) > DATETIME(\"" + time.strftime("%Y-%m-%d", endDate) +"\") AND DATETIME(NOWDATE) <= DATETIME(\"" + time.strftime("%Y-%m-%d", startDate)\
                +"\") AND TIME(NOWTIME) < TIME(\"" + time.strftime("%H:%M:%S", endTime) + "\") AND TIME(NOWTIME) >= TIME(\"" + time.strftime("%H:%M:%S", startTime) + "\")"
        cursor = self._connection.execute(statement)
        self._connection.commit()
        data = cursor.fetchall()
        cursor.close()
        data = np.array(data)
        return data
        """
