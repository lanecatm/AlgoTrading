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
import numpy as np
sys.path.append("../tool")
from Log import Log
class repo:

    # 初始化为sqlite 数据库
    def __init__(self, file_path):
        # here should be abs path when connect db files
        self._file_path = file_path
        file_path_list = file_path.split('.')
        file_path_list[-1] = 'db'
        self._db_file_path = '.'.join(file_path_list)
        self.log = Log()
        #print self._db_file_path
        filename = sys._getframe().f_code.co_filename
        filePath = os.path.realpath(filename).rsplit('/', 1)[0]
        self.log.info("file path: " + filePath)
        self._connection = sqlite3.connect(filePath + "/"+ self._db_file_path)

    # 初始化为mysql 数据库
    def __init__(self, user, password, ip):
        if ip==None:
            db = MySQLdb.connect("localhost", user, password, "history")



    def __del__(self):
        """
        close db connection is necessary when process exits
        :return:
        """
        self._connection.close()


    # 插入抓到的原始数据
    # @param infoArr [x1, x1, ..., x32]
    def insert_data(self, infoArr):
        statement = "INSERT INTO main.history_stock_info VALUES(NULL,"
        for i in range(0, 31):
            statement = statement + infoArr[i] + ","
        statement = statement + infoArr[31] + ", "
        statement = statement + "datetime('now') )"
        #print statement
        cursor = self._connection.execute(statement)
        self._connection.commit()
        cursor.close()


    def change_data_into_mysql(self):
        # 找到表中最小的时间
        # 找到表中最大的时间
        for nowTime in range(startTime, endTime, 60):

            # 每间隔一分钟取出一条数据
            # 插入mysql中


    def get_amount(self):
        return

    def get_price(self):
        return

    def get_info(self, datetime)
    
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
