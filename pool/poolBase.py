# -*- encoding:utf-8 -*-

# ==============================================================================
# Filename: poolBase.py
# Author: Xiaofu Huang
# E-mail: lanecatm@sjtu.edu.cn
# Last modified: 2016-12-22 11:24
# Description: pool 的接口
# ==============================================================================
import copy
import sys
sys.path.append("../common/")
from MarketData import MarketData
import tradingUnit
sys.path.append("../fetch_data/")
from marketDataGetter import marketDataGetter
sys.path.append("../tool/")
from Log import Log

class poolBase:
    def __init__(self):
        self.log = Log

    # 限价单:
    # 指定价格并且挂单直到主动撤单
    # 指定价格，买不到立即撤单
    # 市价单
    # 不指定价格，用(买一/卖一价格) 挂单直到主动撤单
    # 不指定价格, 用(买一/卖一价格) 买不到直接撤单
    # 不指定价格，用(买前五/卖前五价格) 挂单直到主动撤单
    # 不指定价格, 用(买前五/卖前五价格) 买不大直接撤单

    # 限价单:
    #   指定价格，买不到立即撤单
    # 市价单
    #   不指定价格, 用(买一/卖一价格) 买不到直接撤单
    #   不指定价格, 用(买前五/卖前五价格) 买不到直接撤单
    # 判断这一单的执行情况, 同步执行，立即返回
    # param tradingUnit
    # return tradingUnit
    def trade_order_sync(self, tradingUnit):
        return 

    # 限价单:
    #   指定价格并且挂单直到主动撤单
    # 市价单
    #   不指定价格，用(买一/卖一价格) 挂单直到主动撤单
    #   不指定价格，用(买前五/卖前五价格) 挂单直到主动撤单
    # 判断这一单的执行情况, 异步执行, 不立即返回, 通过search_order查询状态
    # param tradingUnit
    # return bool
    def trade_order_async(self, tradingUnit):
        return

    # 撤销一个订单
    # param tradingUnitId int
    # return bool 是否撤销成功
    # return tradingUnit/None
    def drop_order(self, tradingUnitId)
        return
    
    # 寻找一个order
    # param tradingUnitId int
    # return tradingUnit
    def search_order(self, tradingUnitId)
        return 

        

