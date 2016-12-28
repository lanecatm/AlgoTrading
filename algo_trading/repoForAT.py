# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: repoForAT.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-24 16:24
# Description: algotrading 访问数据库repo
# ==============================================================================

import sys, os
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
        quantAnalysisDictStr = str(quantAnalysisDict).replace("'", "\'")


        statement = "INSERT INTO algotradingDB.client_orders values( NULL, "\
                + str(orderInfo.stockId) + ", "\
                + "'" + orderInfo.startTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + "'" + orderInfo.endTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + str(orderInfo.stockAmount) + ", "\
                + str(orderInfo.buySell) + ", "\
                + str(orderInfo.algChoice) + ", "\
                + str(orderInfo.completedAmount) + ", "\
                + str(orderInfo.status) + ", "\
                + "'" + quantAnalysisDictStr + "', "\
                + str(orderInfo.processId) + ", "\
                + str(updateTime) + ", "\
                + str(nextUpdateTime) + ", "\
                + str(orderInfo.updateTimeInterval) + ", "\
                + str(tradeTime) + ", "\
                + str(orderInfo.tradingType) + ", "\
                + str(orderInfo.trunOver) + ", "\
                + str(orderInfo.avgPrice) + ")"
        self.log.info("insert statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()

    # 删除指定单号的订单
    # param orderId int
    def delete_order(self, orderId):
        statement = "DELETE FROM algotradingDB.client_orders WHERE ID = " + str(orderId)
        self.log.info("delete_order statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()

    # 寻找所有单子
    # return list<clientOrder>
    def extract_all_orders(self):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders"
        self.log.info("extract_all_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        for dataUnit in data:
            clientOrderUnit = clientOrder()
            clientOrderUnit.create_order_by_sql_list(dataUnit)
            ansList.append(clientOrderUnit)
        return ansList

    # 寻找一个单子
    # return clientOrder
    def extract_one_order(self, orderId):
        ansList = []
        statement = "SELECT * FROM algotradingDB.client_orders where id = " + str(orderId)
        self.log.info("extract_all_orders statement : " + statement)
        self._mysql_cursor.execute(statement)
        data = self._mysql_cursor.fetchall()
        if len(data) == 0:
            return None
        clientOrderUnit = clientOrder()
        clientOrderUnit.create_order_by_sql_list(data[0])
        return clientOrderUnit


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
    # 1. status 更新
    # 2. 量化分析结果
    # 3. 4个开始执行需要的指标
    # Note: quantanalysis 请插入原来的dict,也可以为None, 为None时不更新
    def save_qa_result(self, orderId, quantanalysis, timeInterval = 1):
        if quantanalysis == None:
            return False
        status = clientOrder.INIT
        quantAnalysisDictStr = str(quantanalysis).replace("'", "\\'")
        statement = "UPDATE algotradingDB.client_orders SET QUANTANALYSIS = '" + str(quantAnalysisDictStr) + "', "\
                + "TRADETIME = NULL, "\
                + "UPDATETIME = STARTTIME,"\
                + "NEXTUPDATETIME = STARTTIME, "\
                + "UPDATEINTERVAL = " + str(timeInterval) + ", "\
                + "STATUS = " + str(status) + " "\
                + "WHERE ID = " + str(orderId)
        self.log.info("save_qa_result statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()
        return True

    # 完成一次交易
    # update the completed amount (and status) after trade
    def post_trade(self, orderId, completed_amount, turnover):
        statement = "UPDATE algotradingDB.client_orders SET COMPLETEDAMOUNT = " + str(completed_amount)\
                + ", TURNOVER = " + str(turnover)\
                + ", AVGPRICE = " + str(turnover/completed_amount)\
                + ", TRADETIME = NULL "\
                + " WHERE ID = " + str(orderId)
        self.log.info("finish trade statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()

    # 更新
    def post_schedule(self, orderId, updateTime, nextUpdateTime, timeInterval, tradeTime):
        if tradeTime == None:
            tradeTimeStr = "NULL"
        else:
            tradeTimeStr = "'" + tradeTime.strftime("%Y-%m-%d %H:%M:%S") + "'"

        statement = "UPDATE algotradingDB.client_orders SET UPDATETIME = '" + updateTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + " NEXTUPDATETIME = '" + nextUpdateTime.strftime("%Y-%m-%d %H:%M:%S") + "', "\
                + " UPDATEINTERVAL = " + str(timeInterval) + ", "\
                + " TRADETIME = " + tradeTimeStr + " "\
                + " WHERE ID = " + str(orderId)
        self.log.info("post_schedule statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()

    # 终结整个交易单
    def complete_trade(self, orderId):
        statement = "UPDATE algotradingDB.client_orders SET STATUS = " + str(clientOrder.COMPLETED)\
                + " WHERE ID = " + str(orderId)
        self.log.info("complete_trade statement : " + statement)
        self._mysql_cursor.execute(statement)
        self._mysql_db.commit()



