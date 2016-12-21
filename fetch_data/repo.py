# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repo.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: Put data into data base
# ==============================================================================

import sys, os
import sqlite3
import MySQLdb
import time
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
class repo:


    def __init_sqlite(self, file_path):
        # here should be abs path when connect db files
        self._sqlite_file_path = file_path
        file_path_list = file_path.split('.')
        file_path_list[-1] = 'db'
        self._sqlite_db_file_path = '.'.join(file_path_list)
        filename = sys._getframe().f_code.co_filename
        filePath = os.path.realpath(filename).rsplit('/', 1)[0]
        self.log.info("file path: " + filePath)
        self._sqlite_connection = sqlite3.connect(filePath + "/"+ self._sqlite_db_file_path)


    def __init_mysql(self, user, password, ip):
        if ip==None:
            self._mysql_db = MySQLdb.connect("localhost", user, password, "algotradingDB")
        else:
            self._mysql_db = MySQLdb.connect(ip, user, password, "algotradingDB")
        self._mysql_cursor = self._mysql_db.cursor()

    # 初始化sqlite 和 mysql数据库
    def __init__(self, isSqlite, isMysql, file_path, user, password, ip, isOpenLog = True):
        self.log = Log(isOpenLog)
        self.isMysql = isMysql
        self.isSqlite = isSqlite
        if self.isSqlite:
            self.__init_sqlite(file_path)
        if self.isMysql:
            self.__init_mysql(user, password, ip)


    def __del__(self):
        if self.isMysql:
            self._mysql_cursor.close()
            self._mysql_db.close()

        if self.isSqlite:
            self._sqlite_connection.close()


    # 插入抓到的原始数据
    # @param infoArr [x1, x1, ..., x32]
    def insert_data(self, infoArr):
        statement = "INSERT INTO main.history_stock_info VALUES(NULL,"
        for i in range(0, 31):
            statement = statement + infoArr[i] + ","
        statement = statement + infoArr[31] + ", "
        statement = statement + "datetime('now') )"
        #print statement
        cursor = self._sqlite_connection.execute(statement)
        self._sqlite_connection.commit()
        cursor.close()


    # 把爬到的数据导入mysql
    def change_data_into_mysql(self):
        statement = "SELECT MAX(ID) FROM main.history_stock_info"
        cursor = self._sqlite_connection.execute(statement)
        self._sqlite_connection.commit()
        data = cursor.fetchall()
        cursor.close()
        maxId = data[0][0]
        self.log.info("max Id:" + str(maxId))
        for i in range(1, maxId):
            # 从sqlite 读取一条数据
            statement = "SELECT * FROM main.history_stock_info WHERE ID = " + str(i)
            cursor = self._sqlite_connection.execute(statement)
            self._sqlite_connection.commit()
            data = cursor.fetchall()
            cursor.close()

            # 插入mysql 一条数据
            statement = "INSERT INTO algotradingDB.history_stock_info values ("
            for dataTuple in data[0]:
                statement = statement + "'"+ str(dataTuple) + "'" + ","
            statement = statement[:-1]
            statement = statement + ")"
            #self.log.info("insert into mysql statement: " + statement)
            self._mysql_cursor.execute(statement)
            self._mysql_db.commit()
            #self.log.info("insert succ")
            if i % 1000 ==0 :
                self.log.info("insert "+str(i) + " succ")


    # 从mysql获取每个时间点的成交量
    # 包含startDate, 不包含endDate, 包含startTime, 不包含endTime
    # 周末直接跳过
    def get_amount(self, stockId, startDate, endDate, startTime, endTime):
        self.log.info(str(startDate) + str(endDate) + str(startTime) + str(endTime))
        delta = (startDate - endDate).days
        self.log.info("during date:" + str(delta))
        allAmountList = []
        allTimeList = []
        for dateIndex in range(delta):
            nowFindingDate = startDate - datetime.timedelta(days = dateIndex)
            # 为了防止最后一个时间点跨天，所以在此重新找到最后一个时间点的交易量
            # 最后一个时间点可能不在交易时间段内，这样为空，否则加入末尾
            statement = "select id, nowdate, time_format(nowtime, '%H:%i:%s'), succnum from algotradingDB.history_stock_info where id in (select min(id) from algotradingDB.history_stock_info where nowdate='" + nowFindingDate.isoformat() + "' and stockid='" + str(stockId) + "' and extract(hour_minute from nowtime)=extract(hour_minute from '" + endTime.strftime("%Y-%m-%d %H:%M:%S") + "')" + " group by extract(hour_minute from nowtime)) order by id"
            self.log.info("get_final statement : " + statement)
            self._mysql_cursor.execute(statement)
            data = self._mysql_cursor.fetchall()
            self.log.info(str(data))
            if len(data) == 0:
                isAddFinalData = False
            else:
                isAddFinalData = True
                finalData = data[0][3]

            # 找时间间隔的时候包含开始时间点不包含结束时间点
            statement = "select id, nowdate, time_format(nowtime, '%H:%i:%s'), succnum from algotradingDB.history_stock_info where id in (select min(id) from algotradingDB.history_stock_info where nowdate='" + nowFindingDate.isoformat() + "' and stockid='" + str(stockId) + "' and nowtime >= '" + startTime.strftime("%H:%M:%S") + "' and nowtime < '" + endTime.strftime("%H:%M:%S") + "' group by extract(hour_minute from nowtime)) order by id"
            self.log.info("get_amount statement : " + statement)
            self._mysql_cursor.execute(statement)
            data = self._mysql_cursor.fetchall()
            self.log.info ("get from mysql " + str(data))
            self.log.info ("get from mysql " + str(len(data)))
            dateAmountList = []
            dateTimeList = []
            if len(data) != 0:
                self.log.info("startTime:" + data[0][1].isoformat() + " " + data[0][2])
                self.log.info("endTime:" + data[-1][1].isoformat() + " " + data[-1][2])
                for i in range(len(data) - 1):
                    dateAmountList.append(data[i+1][3] - data[i][3])
                    dateTimeList.append(data[i][1].isoformat() + " " + data[i][2])
                if isAddFinalData:
                    dateAmountList.append(finalData - data[-1][3])
                    dateTimeList.append(data[-1][1].isoformat() + " " + data[-1][2])
                allAmountList.append(dateAmountList)
                allTimeList.append(dateTimeList)
        return allAmountList, allTimeList

    # 从mysql获取每个时间点的成交价格
    # 包含startDate, 不包含endDate, 包含startTime, 不包含endTime
    def get_price(self, stockId, startDate, endDate, startTime, endTime):
        self.log.info(str(startDate) + str(endDate) + str(startTime) + str(endTime))
        delta = (startDate - endDate).days
        self.log.info("during date:" + str(delta))
        allPriceList = []
        allTimeList = []
        for dateIndex in range(delta):
            nowFindingDate = startDate - datetime.timedelta(days = dateIndex)
            # 找时间间隔的时候包含开始时间点不包含结束时间点
            statement = "select id, nowdate, time_format(nowtime, '%H:%i:%s'), nowprice from algotradingDB.history_stock_info where id in (select min(id) from algotradingDB.history_stock_info where nowdate='" + nowFindingDate.isoformat() + "' and stockid='" + str(stockId) + "' and nowtime >= '" + startTime.strftime("%H:%M:%S") + "' and nowtime < '" + endTime.strftime("%H:%M:%S") + "' group by extract(hour_minute from nowtime)) order by id"
            self.log.info("get_amount statement : " + statement)
            self._mysql_cursor.execute(statement)
            data = self._mysql_cursor.fetchall()
            self.log.info ("get from mysql " + str(data))
            self.log.info ("get from mysql " + str(len(data)))
            datePriceList = []
            dateTimeList = []
            if len(data) != 0:
                self.log.info("startTime:" + data[0][1].isoformat() + " " + data[0][2])
                self.log.info("endTime:" + data[-1][1].isoformat() + " " + data[-1][2])
                for i in range(len(data)):
                    datePriceList.append(data[i][3])
                    dateTimeList.append(data[i][1].isoformat() + " " + data[i][2])
                allPriceList.append(datePriceList)
                allTimeList.append(dateTimeList)
        return allPriceList, allTimeList

    #def get_info(self, datetime)
    
