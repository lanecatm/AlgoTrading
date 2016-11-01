# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: Repo.py
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

    def insert_data(self, infoArr):
        statement = "INSERT INTO main.history_stock_info VALUES(NULL,"
        for i in range(0, 31):
            statement = statement + infoArr[i] + ","
        statement = statement + infoArr[31] + ")"
        #print statement
        cursor = self._connection.execute(statement)
        self._connection.commit()
        cursor.close()

