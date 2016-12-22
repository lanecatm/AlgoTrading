import sys, os
import sqlite3
import MySQLdb
import time
import datetime
import numpy as np
sys.path.append("../tool")
from Log import Log


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

    def extract_orders(self):
	sql = "SELECT * FROM algotradingDB.clent_orders WHERE COMPLETEDAMOUNT < STOCKAMOUNT"
	self.log.info("get_final statement : " + sql)
	self._mysql_cursor.execute(sql)
	data = self._mysql_cursor.fetchall()
	return data

    # quantanalysis MUST be string
    def save_qa_result(self, orderId, quantanalysis):
        sql = "UPDATE algotradingDB.clent_orders SET QUANTANALYSIS = '" + quantanalysis + "' WHERE ID = " + str(orderId)
	self.log.info("get_final statement : " + sql)
	self._mysql_cursor.execute(sql)

    # update the completed amount (and status) after trade
    def post_trade(self, orderId, completed_amount):
        sql = "UPDATE algotradingDB.clent_orders SET COMPLETEDAMOUNT = " + str(completed_amount) + " WHERE ID = " + str(orderId)
        self.log.info("get_final statement : " + sql)
        self._mysql_cursor.execute(sql)

    def post_schedule(self, orderId, update_time, next_update_time, time_interval, trade_time):
        sql = "UPDATE algotradingDB.clent_orders SET UPDATETIME = '" + update_time.strftime("%Y-%m-%d %H:%M:%S") + "', NEXTUPDATETIME = '" + next_update_time.strftime("%Y-%m-%d %H:%M:%S") + "', UPDATEINTERVAL = '" + time_interval.strftime("%H:%M:%S") + "', TRADETIME = '" + trade_time.strftime("%Y-%m-%d %H:%M:%S") + "' WHERE ID = " + str(orderId)
        self.log.info("get_final statement : " + sql)
        self._mysql_cursor.execute(sql)


