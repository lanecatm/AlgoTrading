# -*- encoding:utf-8 -*-
import sys, os
import sqlite3
import MySQLdb
import time
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log
sys.path.append("../common")
from clientOrder import clientOrder


class repoForAT:
    def __init__(self, user, password, ip, isOpenLog = True):
        self.log = Log(isOpenLog)
        if ip==None:
            self._mysql_db = MySQLdb.connect("localhost", user, password, "algotradingDB")
        else:
            self._mysql_db = MySQLdb.connect(ip, user, password, "algotradingDB")
        self._mysql_cursor = self._mysql_db.cursor()

    def __del__(self):
        self._mysql_cursor.close()
        self._mysql_db.close()

    # 新增一个order
    # param orderInfo clientOrder
    def insert_order(self, orderInfo):
        if orderInfo.quantAnalysisDict == None:
            quantAnalysisDict = {}
        else:
            quantAnalysisDict = orderInfo.quantAnalysisDict
        if orderInfo.updateTime == None:
            updateTime = "NULL"
        else:
            updateTime = "'" + orderInfo.updateTime.strftime("%Y-%m-%d %H:%M:%S") + "'"
        if orderInfo.nextUpdateTime == None:
            nextUpdateTime = "NULL"
        else:
            nextUpdateTime = "'" + orderInfo.nextUpdateTime.strftime("%Y-%m-%d %H:%M:%S") + "'"
        if orderInfo.tradeTime == None:
            tradeTime ="NULL"
        else:
            tradeTime = "'" + orderInfo.tradeTime.strftime("%Y-%m-%d %H:%M:%S") + "'"

        statement = "INSERT INTO algotradingDB.client_orders values( NULL, "\
                + str(orderInfo.stockId) + ", "\
                + "'" + orderInfo.startTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + "'" + orderInfo.endTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + str(orderInfo.stockAmount) + ", "\
                + str(orderInfo.buySell) + ", "\
                + str(orderInfo.algChoice) + ", "\
                + str(orderInfo.completedAmount) + ", "\
                + str(orderInfo.status) + ", "\
                + "'" + str(quantAnalysisDict) + "', "\
                + str(orderInfo.processId) + ", "\
                + str(updateTime) + ", "\
                + str(nextUpdateTime) + ", "\
                + str(orderInfo.updateTimeInterval) + ", "\
                + str(tradeTime) + ", "\
                + str(orderInfo.tradingType) + ", "\
                + str(orderInfo.trunOver) + ", "\
                + str(orderInfo.avgPrice) + ")"
        self.log.info("get_final statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()
    
    # 寻找没有量化分析的单号
    # return list<clientOrder>
    def extract_uninit_orders(self):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders WHERE STATUS = " + str(clientOrder.UNINIT)
        self.log.info("extract_uninit_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        for dataUnit in data:
            clientOrderUnit = clientOrder()
            clientOrderUnit.create_order_by_sql_list(dataUnit)
            ansList.append(clientOrderUnit)
        return ansList


    # 寻找未完成需要在当前时间点交易的单号
    # param nowTime datetime
    def extract_trading_orders(self, nowTime):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders WHERE TRADETIME <= '" + nowTime.strftime("%Y-%m-%d %H:%M:%S") + "'"\
                + " AND STATUS = " + str(clientOrder.INIT)
        self.log.info("extract_trading_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        for dataUnit in data:
            clientOrderUnit = clientOrder()
            clientOrderUnit.create_order_by_sql_list(dataUnit)
            ansList.append(clientOrderUnit)
        return ansList

    # 寻找未完成需要在当前时间点更新的单号
    # param nowTime datetime
    def extract_refresh_orders(self, nowTime):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders WHERE NEXTUPDATETIME <= '" + nowTime.strftime("%Y-%m-%d %H:%M:%S") + "'"\
                + " AND STATUS = " + str(clientOrder.INIT)
        self.log.info("extract_refresh_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        for dataUnit in data:
            clientOrderUnit = clientOrder()
            clientOrderUnit.create_order_by_sql_list(dataUnit)
            ansList.append(clientOrderUnit)
        return ansList

    # 需要更新为已完成状态的单号
    def extract_completed_orders(self, nowTime):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders WHERE ENDTIME <= '" + nowTime.strftime("%Y-%m-%d %H:%M:%S") + "'"\
                + " AND STATUS = " + str(clientOrder.INIT)
        self.log.info("extract_completed_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        for dataUnit in data:
            clientOrderUnit = clientOrder()
            clientOrderUnit.create_order_by_sql_list(dataUnit)
            ansList.append(clientOrderUnit)
        return ansList


    # 更新量化分析结果
    # status 更新
    # 量化分析结果
    # 4个开始执行需要的指标
    # quantanalysis MUST be string
    def save_qa_result(self, orderId, quantanalysis):
        sql = "UPDATE algotradingDB.client_orders SET QUANTANALYSIS = '" + quantanalysis + "' WHERE ID = " + str(orderId)
        self.log.info("get_final statement : " + sql)
        self._mysql_cursor.execute(sql)

    # 完成一次交易
    # update the completed amount (and status) after trade
    def post_trade(self, orderId, completed_amount, turnover):
        sql = "UPDATE algotradingDB.client_orders SET COMPLETEDAMOUNT = " + str(completed_amount) + ", TURNOVER = " + str(turnover) + ", AVGPRICE = " + str(turnover/completed_amount) + " WHERE ID = " + str(orderId)
        self.log.info("get_final statement : " + sql)
        self._mysql_cursor.execute(sql)

    # 更新
    def post_schedule(self, orderId, update_time, next_update_time, time_interval, trade_time):
        sql = "UPDATE algotradingDB.client_orders SET UPDATETIME = '" + update_time.strftime("%Y-%m-%d %H:%M:%S") + "', NEXTUPDATETIME = '" + next_update_time.strftime("%Y-%m-%d %H:%M:%S") + "', UPDATEINTERVAL = " + str(time_interval) + ", TRADETIME = '" + trade_time.strftime("%Y-%m-%d %H:%M:%S") + "' WHERE ID = " + str(orderId)
        self.log.info("get_final statement : " + sql)
        self._mysql_cursor.execute(sql)


