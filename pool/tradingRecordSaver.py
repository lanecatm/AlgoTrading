# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: tradingRecordSaver.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-23 20:40
# Description: save each trade record
# ==============================================================================
import sys, os
import MySQLdb
sys.path.append("../common/")
from tradingUnit import tradingUnit
import datetime
sys.path.append("../tool")
from Log import Log
class tradingRecordSaver:
    def __init__(self, user, password, ip, isOpenLog = True):
        if ip==None:
            self._mysql_db = MySQLdb.connect("localhost", user, password, "algotradingDB")
        else:
            self._mysql_db = MySQLdb.connect(ip, user, password, "algotradingDB")
        self._mysql_cursor = self._mysql_db.cursor()
        self.log = Log(isOpenLog)

    def __del__(self):
        self._mysql_cursor.close()
        self._mysql_db.close()

    def save_record(self, tradingRecord):
        self.log.info("save record " + str(tradingRecord))
        if tradingRecord.expectPrice == None:
            expectPrice = "NULL"
        else:
            expectPrice = tradingRecord.expectPrice
        statement = "INSERT INTO algotradingDB.outside_pool_record VALUES(NULL, "\
                + str(tradingRecord.tradingUnitId) + ", "\
                + str(tradingRecord.stockId) + ", "\
                + "'" + tradingRecord.time.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + str(tradingRecord.buysell) + ", "\
                + str(tradingRecord.isSync) + ", "\
                + str(tradingRecord.tradingType) + ", "\
                + str(tradingRecord.amount) + ", "\
                + str(expectPrice) + ", "\
                + str(tradingRecord.isSuccess) + ", "\
                + str(tradingRecord.succAmount) + ", "\
                + str(tradingRecord.succMoney) + ", "\
                + str(tradingRecord.price) + ")"
        self.log.info("statement: " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()

    def get_history_record(self, orderId = None):
        if orderId == None:
            statement = "SELECT * FROM algotradingDB.outside_pool_record"
        else:
            statement = "SELECT * FROM algotradingDB.outside_pool_record WHERE ORDERID = " + str(orderId)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        tradingRecordList = []
        for unitData in data:
            self.log.info("get history record " + str(unitData))
            tradingRecord = tradingUnit(unitData[1], unitData[2], unitData[3], unitData[4], unitData[5], unitData[6], unitData[7], unitData[8])
            tradingRecord.refresh_order(unitData[10], unitData[11], unitData[9])
            tradingRecordList.append(tradingRecord)
        return tradingRecordList


 
