# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:07 2016

@author: Panh
"""

import tushare as ts
import pymysql
import traceback
import time
import numpy as np
import urllib


class acquireStockData(object): 
    
    def __init__(self, host = "localhost", user = "root", passwd = "haopan09", port = 3306, charset = 'utf8', db='stocktest'):
        self.host = host
        self.user = user 
        self.passwd = passwd
        self.port = port
        self.charset = charset
        self.db = db

    def connectMySQL(self):
        try:
            #self.conn = pymysql.connect(host = self.host, user = self.user , passwd = self.passwd, port = self.port, charset = self.charset, db= self.db )
            self.conn = pymysql.connect(host = self.host, user = self.user, port = self.port, charset = self.charset, db= self.db )
            self.cur = self.conn.cursor()
            #create the table for tick data (histort data for each second per day)
            SQL = "create table if not exists tick (code_tick varchar(20),\
                                                    date_tick varchar(20),\
                                                    time_tick varchar(20),\
                                                    price_tick float,\
                                                    change_tick varchar(10),\
                                                    volume_tick int,\
                                                    amount_tick int,\
                                                    type_tick varchar(10))"
            self.cur.execute(SQL)
            #create the table for hist data (history data for each day)
            SQL = "create table if not exists hist (code_hist varchar(20),\
                                                    date_hist varchar(20),\
                                                    open_hist float,\
                                                    high_hist float,\
                                                    close_hist float,\
                                                    low_hist float,\
                                                    volume_hist float,\
                                                    price_change_hist float,\
                                                    p_change_hist float,\
                                                    ma5_hist float,\
                                                    ma10_hist float,\
                                                    ma20_hist float,\
                                                    v_ma5_hist float,\
                                                    v_ma10_hist float,\
                                                    v_ma20_hist float,\
                                                    turnover_hist float)"
            self.cur.execute(SQL)    
            #create the temp table for today data for each second
            SQL = "create temporary table tmoToday (time_today varchar(20),\
                                                    price_today float,\
                                                    pchange_today float,\
                                                    change_today float,\
                                                    volume_today int,\
                                                    amount_today int,\
                                                    type_today varchar(29))"
            self.cur.execute(SQL)
                          
            return 1
        except:
            traceback.print_exc()
            return 0

    def storeSecondHistoryStockData(self, stockCodeString, dateString):  #'600000', '2016-10-25'      
        try:
            df = ts.get_tick_data(stockCodeString, dateString)  #data frame of tushare, same with pandas
            #transform the format timestamp to store
            timeFormat = ""
            for tmp_index in range(len(df)):
                timeTmp = df['time'][tmp_index]
                timeSplit = timeTmp.split(':')
                timeFormat = timeSplit[0]+'-'+timeSplit[1]+'-'+timeSplit[2]
                SQL = "insert into tick (code_tick, date_tick, time_tick, price_tick,\
                                         change_tick,volume_tick,amount_tick,type_tick)\
                                         values (%s,%r,%r,%f,%r,%d,%d,%r)"%(stockCodeString, \
                                         dateString, timeFormat, float(df['price'][tmp_index]), \
                                         df['change'][tmp_index], df['volume'][tmp_index], \
                                         df['amount'][tmp_index], df['type'][tmp_index])
                self.cur.execute(SQL)
                self.conn.commit()
        except:
            traceback.print_exc()
            print ("Fail to store the required data")
            return 0
            pass
        
      
    def storeDayHistoryStockData(self, stockCodeString, startDateString, endDateString):
        try:
            df = ts.get_hist_data(stockCodeString, start = startDateString, end = endDateString)
            for tmp_index in range(len(df)):   
                dateString = df.index[tmp_index]
                SQL = 'insert into hist (code_hist, date_hist, open_hist, high_hist,\
                                         close_hist, low_hist, volume_hist, price_change_hist,\
                                         p_change_hist,ma5_hist, ma10_hist, ma20_hist,\
                                         v_ma5_hist, v_ma10_hist, v_ma20_hist, turnover_hist)\
                                         values (%s, %r, %f, %f, %f, %f, %f, %f, %f, \
                                         %f, %f, %f, %f, %f, %f, %f)'%(stockCodeString, dateString, df['open'][tmp_index], df['high'][tmp_index],\
                                         df['close'][tmp_index], df['low'][tmp_index],df['volume'][tmp_index], df['price_change'][tmp_index], \
                                         df['p_change'][tmp_index], df['ma5'][tmp_index], df['ma10'][tmp_index], df['ma20'][tmp_index], \
                                         df['v_ma5'][tmp_index], df['v_ma10'][tmp_index], df['v_ma20'][tmp_index], df['turnover'][tmp_index])
                self.cur.execute(SQL)
                self.conn.commit()
        except:
            traceback.print_exc()
            print ("Fail to store the required data")
            return 0
            pass
        """
    def fetchTodayStockInfo(self,  codeString, storeFlag=None):
        todayDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        print (todayDate)
        if(storeFlag==None):
            storeFlag = 1
        try:
            df = ts.get_today_ticks(codeString)
            if(storeFlag == 0):
                #not store data in the database
                return df
            if(storeFlag == 1):
                #store the data in the database
                #for tmp_index in range(len(df)):
"""

    def fetchDayStockInfo(self, dataType, codeString, dateFilter):
        filterString = ""
        if(dataType == 'all'):
            filterString = "code_hist, date_hist, open_hist, high_hist, \
                            close_hist, low_hist, volume_hist, price_change_hist, \
                            p_change_hist, ma5_hist, ma10_hist, ma20_hist, \
                            v_ma5_hist, v_ma10_hist, v_ma20_hist, turnover_hist "
        else:
            filterString = "code_hist, date_hist, "
            tmpSplit = dataType.split(',')
            for i in range(len(tmpSplit)-1):
                filterString += tmpSplit[i]+'_hist, '
            filterString += tmpSplit[-1]+'_hist '
 
        #SQL = "select open_hist, date_hist from hist where date_hist like '" + dateFilter + "%'";
        SQL = "select "+ filterString+ "from hist where code_hist like '" +  codeString + "' and date_hist like '"+ dateFilter + "%'"; 
        self.cur.execute(SQL)
        results = self.cur.fetchall()
        return results
    
    def fetchSecondStockInfo(self, dataType, codeString, dateFilter, timeFilter): #date format like 2016-10-25,time format like 14:00:00
        #add the table selection and feature filter
        #transform the format timestamp to fetch
        filterString = ""
        if(dataType == 'all'):
            filterString = "code_tick, date_tick, time_tick, price_tick, \
                            change_tick, volume_tick, amount_tick, type_tick"
        else:
            filterString = "code_tick, date_tick, "
            tmpSplit = dataType.split(',')
            for i in range(len(tmpSplit)-1):
                filterString += tmpSplit[i]+'_tick, '
            filterString += tmpSplit[-1]+'_tick '
            
        timeFilter = timeFilter.replace(':', '-')

        SQL = "select " + filterString+ " from tick where code_tick like '"+ codeString + "' and time_tick like '"+ timeFilter + "%' and date_tick like '"+ dateFilter+"%'"
        self.cur.execute(SQL)
        results = self.cur.fetchall()   
        return results
     
     
    def spiderCurrentTimeStockDataViaSina(self, codeString):
        url = "http://hq.sinajs.cn/list=sh" + codeString
        pagerequest = urllib.request.Request(url)
        pagereponse = urllib.request.urlopen(pagerequest)
        stockhtml = pagereponse.read().decode('gbk') 
        #start fetch each data of the stock
        tmp1 = stockhtml.split("=")
        tmp2 = tmp1[-1].split(";")
        tmp3 = tmp2[0].split(",") # tmp3[-1] is invalid information
        del tmp3[-1]
        return tmp3
        """ 0：”大秦铁路”，股票名字；
            1：”27.55″，今日开盘价；
            2：”27.25″，昨日收盘价；
            3：”26.91″，当前价格；
            4：”27.55″，今日最高价；
            5：”26.20″，今日最低价；
            6：”26.91″，竞买价，即“买一”报价；
            7：”26.92″，竞卖价，即“卖一”报价；
            8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
            9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
            10：”4695″，“买一”申请4695股，即47手；
            11：”26.91″，“买一”报价；
            12：”57590″，“买二”
            13：”26.90″，“买二”
            14：”14700″，“买三”
            15：”26.89″，“买三”
            16：”14300″，“买四”
            17：”26.88″，“买四”
            18：”15100″，“买五”
            19：”26.87″，“买五”
            20：”3100″，“卖一”申报3100股，即31手；
            21：”26.92″，“卖一”报价
            (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
            30：”2008-01-11″，日期；
            31：”15:05:32″，时间；
     
     """
     
     

    def closeConnection(self):
        # drop the temp table
        self.cur.execute("drop temporary table tmpToday")
        self.cur.close()
        self.conn.close()
        
    
