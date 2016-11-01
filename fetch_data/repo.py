# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repo.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-10-26 17:05
# Description: Put data into data base
# ==============================================================================

import sqlite3
class repo:
    def __init__(self, file_path):
        # here should be abs path when connect db files
        self._file_path = file_path
        file_path_list = file_path.split('.')
        file_path_list[-1] = 'db'
        self._db_file_path = '.'.join(file_path_list)
        #print self._db_file_path
        self._connection = sqlite3.connect(self._db_file_path)


    def __del__(self):
        """
        close db connection is necessary when process exits
        :return:
        """
        self._connection.close()


    # 插入抓到的数据
    # @param infoArr [x1, x1, ..., x32]
    def insert_data(self, infoArr):
        statement = "INSERT INTO main.history_stock_info VALUES(NULL,"
        for i in range(0, 31):
            statement = statement + infoArr[i] + ","
        statement = statement + infoArr[31] + ")"
        #print statement
        cursor = self._connection.execute(statement)
        self._connection.commit()
        cursor.close()
    
    # 获取股票的成交数量
    # @param startDate dateTime 从哪一天开始
    # @param endDate dateTime 到哪一天结束
    # @param startTime time 每一天中的开始时间(包含这一刻)
    # @param endTime time 每一天中的结束时间(不包含这一刻)
    # @return [[amount1, amount2, ..., amountn]
    #          [amount1, amount2, ..., amountn]
    #          ...                             
    #         ]
    def get_amount(self, startDate, endDate, startTime, endTime):
        

        
        return 
