# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: tradingRecordRepo.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-11-07 21:18
# Description: save each trade record
# ==============================================================================
import copy
import sys
sys.path.append("../common/")
from tradingUnit import tradingUnit
import datetime
import sqlite3
sys.path.append("../tool")
from Log import Log
class tradingRecordRepo:
    def __init__(self, file_path):
        # here should be abs path when connect db files
        self._file_path = file_path
        file_path_list = file_path.split('.')
        file_path_list[-1] = 'db'
        self._db_file_path = '.'.join(file_path_list)
        #print self._db_file_path
        self._connection = sqlite3.connect(self._db_file_path)
        self.log = Log()


    def __del__(self):
        """
        close db connection is necessary when process exits
        :return:
        """
        self._connection.close()

    def save_record(self, tradingRecord):
        statement = "INSERT INTO main.trading_record VALUES(NULL,"\
                + str(tradingRecord.orderId) + ", "\
                + str(tradingRecord.stockId) + ", "\
                + str((int)(tradingRecord.buysell)) + ", "\
                + str(tradingRecord.price) + ", "\
                + str(tradingRecord.amount) + ", "\
                + str((int)(tradingRecord.isSuccess)) + ", "\
                + "\"" + tradingRecord.time.strftime("%Y-%m-%d") + "\", "\
                + "\"" + tradingRecord.time.strftime("%H:%M:%S") + "\")"
        self.log.info("statement: " + statement)
        cursor = self._connection.execute(statement)
        self._connection.commit()
        cursor.close()

    def get_history_record(self):
        statement = "SELECT * FROM main.trading_record"
        cursor = self._connection.execute(statement)
        self._connection.commit()
        data = cursor.fetchall()
        cursor.close()
        self.log.info("get data:\n" + str(data))
        tradingRecordList = []
        for unitData in data:
            timeToInsert = datetime.datetime.strptime(unitData[7] + unitData[8], "%Y-%m-%d%H:%M:%S")
            tradingRecord = tradingUnit(unitData[1], unitData[2], unitData[3], unitData[5], unitData[4], unitData[6], timeToInsert )
            tradingRecordList.append(tradingRecord)
        return tradingRecordList


 
