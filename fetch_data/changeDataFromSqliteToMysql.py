# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: changeDataFromSqliteToMysql.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-20 13:34
# Description: change data from sqlite to mysql
# ==============================================================================

import sys, os
import sqlite3
from repo import repo
sys.path.append("../tool")
from Log import Log


sqliteRepo = repo(True, True, "again_2_half.db", "algotrading", "12345678", None)
sqliteRepo.change_data_into_mysql()
