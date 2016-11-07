# -*- encoding:utf-8 -*-

import sys, os

def getCurrentFilePath():
    cur_path = sys.path[0]
    if os.path.isdir(cur_path):
        return cur_path
    elif os.path.isfile(cur_path):
        return os.path.dirname(cur_path)

def getAbsFilePath(filename):
    return getCurrentFilePath() + "/" + filename

