# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 21:21:11 2016

@author: user
"""
import sys
import datetime
import random

sys.path.append("../algo_trading")
from algoTrading import algoTrading
from repoForAT import repoForAT
#import algotrading_main

sys.path.append("../tool")
from Log import Log

sys.path.append("../common/")
from clientOrder import clientOrder
from tradingUnit import tradingUnit

sys.path.append("../quant_analysis")
from TWAPQuantAnalysis import TWAPQuantAnalysis
from VWAPQuantAnalysis import VWAPQuantAnalysis
from LinearVWAPQuantAnalysis import LinearVWAPQuantAnalysis

sys.path.append("../pool")
from poolFromSinaApi import poolFromSinaApi
from tradingRecordSaver import tradingRecordSaver

sys.path.append("../fetch_data")
from marketDataGetter import marketDataGetter
from repo import repo
from chartCreater import chartCreater
import multiprocessing

from PyQt4 import QtGui
def realtime_pool(findLastDays = 7, isOpenLog = False):

    # 初始化algotrading的repo
    rat = repoForAT("algotrading", "12345678", None, isOpenLog = isOpenLog)

    # 初始化pool
    poolDataMarketGetter = marketDataGetter(isOpenLog = isOpenLog)
    poolDataRepoGetter = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
    poolRecordSaver = tradingRecordSaver("algotrading", "12345678", None, isOpenLog = isOpenLog)
    poolRealTime = poolFromSinaApi(poolDataMarketGetter, True, poolRecordSaver, isOpenLog = isOpenLog)
    poolHistory = poolFromSinaApi(poolDataRepoGetter, False, poolRecordSaver, isOpenLog = isOpenLog)
    
    # 初始化quantAnalysisDict
    repoForQuantAnalysis = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
    quantAnalysisDict = {}
    quantAnalysisDict[clientOrder.TWAP] = TWAPQuantAnalysis(isOpenLog = isOpenLog)
    quantAnalysisDict[clientOrder.VWAP] = VWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
    quantAnalysisDict[clientOrder.LINEARVWAP] = LinearVWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
 

    algoTradingEngine = algoTrading( rat, poolRealTime, quantAnalysisDict, findLastDays, isOpenLog = isOpenLog)

    log.info("init succ")

    index = 0
    while(1):
        algoTradingEngine.set_time(datetime.datetime.now())
        startTime = startTime + datetime.timedelta(minutes = 1)
        algoTradingEngine.init_orders()
        algoTradingEngine.refresh()
        algoTradingEngine.trade_request()
        algoTradingEngine.complete_orders()
        index = index + 1
        if index%60 == 0:
            log.info("now time:" + str(startTime))
 
class TestWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(TestWindow, self).__init__(parent)
        self.repoAT = repoForAT('algotrading', '12345678', None, False)
        self.repoMonitor = tradingRecordSaver('algotrading', '12345678', None, False)
        self.repoHistory = repo(False, True, None, "algotrading", '12345678', None, False)
        self.setWindowTitle(u'算法交易GUI')
        self.p = None
        
        """--------------------------全局变量--------------------------"""
        self.startYear = 0
        self.startMonth = 0
        self.startDay = 0
        self.startHour = 0
        self.startMinute = 0
        self.startSecond = 0
        self.startTimeString = str(self.startYear)+'-'+str(self.startMonth)+'-'+str(self.startDay)+' '+str(self.startHour)+':'+str(self.startMinute)+':'+str(self.startSecond)
        
        self.endYear = 0
        self.endMonth = 0
        self.endDay = 0
        self.endHour = 0
        self.endMinute = 0
        self.endSecond = 0
        self.endTimeString = str(self.endYear)+'-'+str(self.endMonth)+'-'+str(self.endDay)+' '+str(self.endHour)+':'+str(self.endMinute)+':'+str(self.endSecond)

        self.firstTimeYear = 0
        self.firstTimeMonth = 0
        self.firstTimeDay = 0
        self.firstTimeHour = 0
        self.firstTimeMinute = 0
        self.firstTimeSecond = 0
        self.firstTimeString = str(self.firstTimeYear)+'-'+str(self.firstTimeMonth)+'-'+str(self.firstTimeDay)+' '+str(self.firstTimeHour)+':'+str(self.firstTimeMinute)+':'+str(self.firstTimeSecond)

        self.secondTimeYear = 0
        self.secondTimeMonth = 0
        self.secondTimeDay = 0
        self.secondTimeHour = 0
        self.secondTimeMinute = 0
        self.secondTimeSecond = 0
        self.secondTimeString = str(self.secondTimeYear)+'-'+str(self.secondTimeMonth)+'-'+str(self.secondTimeDay)+' '+str(self.secondTimeHour)+':'+str(self.secondTimeMinute)+':'+str(self.secondTimeSecond)
  
        self.orderId = 0
        self.orderIdDisplay = ''
        self.stockId = 0#int
        self.stockIdDisplay = ''
        self.startTime = 0#datetime
        self.startTimeDisplay = ''
        self.endTime = 0#datetime
        self.endTimeDisplay = ''
        self.stockAmount = 0#int
        self.stockAmountDisplay = ''
        self.buySell = 0#tradingUnit.BUY 0  .SELL 1
        self.buySellDisplay = ''
        self.algChoice = 0#clientOrder.TWAP 0 .VWAP 1 .LINEARVWAP 2
        self.algChoiceDisplay = ''
        self.processId = 0#...
        self.processIdDisplay = ''
        self.tradingType = 0#...
        self.tradingTypeDisplay = ''
        self.firstTime = 0#datetime
        self.firstTimeDisplay = ''
        self.secondTime = 0#datetime
        self.secondTimeDisplay = ''
        
        """--------------------------布局变量--------------------------"""
        self.layout = QtGui.QGridLayout()
        """--------------------------股票ID设置--------------------------"""
        self.stockId = QtGui.QPushButton(u'股票ID')
        pal = self.stockId.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.stockId.setPalette(pal)
        self.layout.addWidget(self.stockId,0,6)
        
        self.stockIdEdit = QtGui.QComboBox()
        self.stockIdEdit.addItem("600000")
        self.stockIdEdit.addItem("601006")
        self.stockIdEdit.addItem("601377")
        self.layout.addWidget(self.stockIdEdit,0,7)
         
        """--------------------------开始时间定义--------------------------"""
        self.startTimeButton = QtGui.QPushButton(u'开始时间')
        pal = self.startTimeButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.startTimeButton.setPalette(pal)
        self.layout.addWidget(self.startTimeButton,1,6)
        
        self.startTimeEdit = QtGui.QPushButton(u'编辑开始时间')

        self.layout.addWidget(self.startTimeEdit,1,7)
        self.startTimeEdit.clicked.connect(self.startTimeEditFun)
        
        """--------------------------结束时间定义--------------------------"""
        self.endTimeButton = QtGui.QPushButton(u'结束时间')
        pal = self.endTimeButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.endTimeButton.setPalette(pal)
        self.layout.addWidget(self.endTimeButton,2,6)
        
        self.endTimeEdit = QtGui.QPushButton(u'编辑结束时间')
        self.layout.addWidget(self.endTimeEdit,2,7)
        self.endTimeEdit.clicked.connect(self.endTimeEditFun)
        
        """--------------------------股票数量定义--------------------------"""
        self.stockAmountButton = QtGui.QPushButton(u'股票数量')
        pal = self.stockAmountButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.stockAmountButton.setPalette(pal)
        self.layout.addWidget(self.stockAmountButton,3,6)
        
        self.stockAmountEdit = QtGui.QSpinBox()
        self.stockAmountEdit.setRange(0,1000000000)
        self.layout.addWidget(self.stockAmountEdit,3,7)
        
        """--------------------------操作类型定义--------------------------"""
        self.operateTypeButton = QtGui.QPushButton(u'操作类型')
        pal = self.operateTypeButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.operateTypeButton.setPalette(pal)
        self.layout.addWidget(self.operateTypeButton,4,6)
        
        self.operateTypeEdit = QtGui.QComboBox()
        self.operateTypeEdit.addItem("BUY")
        self.operateTypeEdit.addItem("SELL")
        self.layout.addWidget(self.operateTypeEdit,4,7)
        
        """--------------------------算法选择定义--------------------------"""
        self.algChoiceButton = QtGui.QPushButton(u'算法选择')
        pal = self.algChoiceButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.algChoiceButton.setPalette(pal)
        self.layout.addWidget(self.algChoiceButton,5,6)
        
        self.algChoiceEdit = QtGui.QComboBox()
        self.algChoiceEdit.addItem("TWAP")
        self.algChoiceEdit.addItem("VWAP")
        self.algChoiceEdit.addItem("LINEARVWAP")
        self.layout.addWidget(self.algChoiceEdit,5,7)
        
        """------------------------------------------"""
        self.processIdButton = QtGui.QPushButton(u'进程ID')
        pal = self.processIdButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.processIdButton.setPalette(pal)
        self.layout.addWidget(self.processIdButton,6,6)
        
        self.processIdEdit = QtGui.QComboBox()
        self.processIdEdit.addItem("1")
        self.processIdEdit.addItem("Other")
        self.layout.addWidget(self.processIdEdit,6,7)
        
        """--------------------------交易类型定义--------------------------"""
        self.tradingTypeButton = QtGui.QPushButton(u'交易类型')
        pal = self.tradingTypeButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('blue'))
        self.tradingTypeButton.setPalette(pal)
        self.layout.addWidget(self.tradingTypeButton,7,6)
        
        self.tradingTypeEdit = QtGui.QComboBox()
        self.tradingTypeEdit.addItem("None")
        self.layout.addWidget(self.tradingTypeEdit,7,7)
        
        """--------------------------确定订单按钮--------------------------"""
        self.confirmButton = QtGui.QPushButton(u'确定订单')
        pal = self.confirmButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('red'))
        self.confirmButton.setPalette(pal)
        self.layout.addWidget(self.confirmButton,8,6,1,2)
        self.confirmButton.clicked.connect(self.confirmOrderFun)
        
        """--------------------------清空设置按钮暂不用--------------------------"""
        self.emptyButton = QtGui.QPushButton(u'清空所有订单')
        pal = self.emptyButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('red'))
        self.emptyButton.setPalette(pal)
        self.layout.addWidget(self.emptyButton,9,6,1,2)
        self.emptyButton.clicked.connect(self.emptyOrderFun)
        
        """--------------------------输入记录表按钮--------------------------"""
        self.inputTableLabel = QtGui.QTableWidget()
        self.inputTableLabel.setColumnCount(7)
        self.inputTableLabel.setRowCount(1000)
        self.inputInfoUpdate  = QtGui.QPushButton(u'输入记录表(点击刷新数据)')
        self.inputInfoUpdate.clicked.connect(self.pushInputInfoUpdateFun)
        pal = self.inputInfoUpdate.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('green'))
        self.inputInfoUpdate.setPalette(pal)
        self.layout.addWidget(self.inputInfoUpdate,10,0, 1,6)
        self.layout.addWidget(self.inputTableLabel,11,0, 10,6)
        """set the table item title"""
        self.inputTableLabel.setItem(0,0, QtGui.QTableWidgetItem(u'订单ID'))
        self.inputTableLabel.setItem(0,1, QtGui.QTableWidgetItem(u'股票ID'))
        self.inputTableLabel.setItem(0,2, QtGui.QTableWidgetItem(u'开始时间'))
        self.inputTableLabel.setItem(0,3, QtGui.QTableWidgetItem(u'结束时间'))
        self.inputTableLabel.setItem(0,4, QtGui.QTableWidgetItem(u'股票数量'))
        self.inputTableLabel.setItem(0,5, QtGui.QTableWidgetItem(u'操作类型'))
        self.inputTableLabel.setItem(0,6, QtGui.QTableWidgetItem(u'算法选择'))
        
        """--------------------------输出记录表按钮--------------------------"""
        self.outputTableLabel = QtGui.QTableWidget()
        self.outputTableLabel.setColumnCount(6)
        self.outputTableLabel.setRowCount(1000)
        self.outputInfoUpdate = QtGui.QPushButton(u'输出记录表(点击刷新数据)')
        self.outputInfoUpdate.clicked.connect(self.pushOutputInfoUpdateFun)
        pal = self.outputInfoUpdate.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('green'))
        self.outputInfoUpdate.setPalette(pal)
        self.layout.addWidget(self.outputInfoUpdate,21,0, 1,6)
        self.layout.addWidget(self.outputTableLabel,22,0, 10,6)
        """set the table item title"""
        self.outputTableLabel.setItem(0,0, QtGui.QTableWidgetItem(u'订单ID'))
        self.outputTableLabel.setItem(0,1, QtGui.QTableWidgetItem(u'股票ID'))
        self.outputTableLabel.setItem(0,2, QtGui.QTableWidgetItem(u'是否成功'))
        self.outputTableLabel.setItem(0,3, QtGui.QTableWidgetItem(u'成功数量'))
        self.outputTableLabel.setItem(0,4, QtGui.QTableWidgetItem(u'交易总价'))
        self.outputTableLabel.setItem(0,5, QtGui.QTableWidgetItem(u'交易单价'))
        
        
        """--------------------------监控池数据表按钮--------------------------"""
        self.monitorPoolTableLabel = QtGui.QTableWidget()
        self.monitorPoolTableLabel.setColumnCount(9)
        self.monitorPoolTableLabel.setRowCount(1000)
        self.monitorPoolUpdate = QtGui.QPushButton(u'监控池数据表(点击刷新数据)')
        self.monitorPoolUpdate.clicked.connect(self.pushMonitorPoolUpdateFun)
        pal = self.monitorPoolUpdate.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('green'))
        self.monitorPoolUpdate.setPalette(pal)
        self.layout.addWidget(self.monitorPoolUpdate,0,0, 1,6)
        self.layout.addWidget(self.monitorPoolTableLabel,1,0, 9,6)
        """set the table item title"""
        self.monitorPoolTableLabel.setItem(0,0, QtGui.QTableWidgetItem(u'交易单号'))
        self.monitorPoolTableLabel.setItem(0,1, QtGui.QTableWidgetItem(u'交易股票ID'))
        self.monitorPoolTableLabel.setItem(0,2, QtGui.QTableWidgetItem(u'交易订单时间'))
        self.monitorPoolTableLabel.setItem(0,3, QtGui.QTableWidgetItem(u'交易类型'))
        self.monitorPoolTableLabel.setItem(0,4, QtGui.QTableWidgetItem(u'交易方式'))
        self.monitorPoolTableLabel.setItem(0,5, QtGui.QTableWidgetItem(u'交易股票数量'))
        self.monitorPoolTableLabel.setItem(0,6, QtGui.QTableWidgetItem(u'交易价格'))
        self.monitorPoolTableLabel.setItem(0,7, QtGui.QTableWidgetItem(u'交易成功数量'))
        self.monitorPoolTableLabel.setItem(0,8, QtGui.QTableWidgetItem(u'交易总金额'))
        
        
        """--------------------------图片1信息按钮--------------------------"""
        self.pictureOneLabel = QtGui.QLabel()
        self.pictureOneLabel.setPixmap(QtGui.QPixmap('J:\\GUI\\kline.png'))
        #self.layout.addWidget(self.pictureOneLabel,11,6, 10,3) #4 5
        
        self.pictureOneUpdate = QtGui.QPushButton(u'交易量累积图')
        self.pictureOneUpdate.clicked.connect(self.pushPictureOne)
        pal = self.pictureOneUpdate.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('black'))
        self.pictureOneUpdate.setPalette(pal)
        self.layout.addWidget(self.pictureOneUpdate,10,6) #1 5
        
        self.pictureTwoUpdate = QtGui.QPushButton(u'交易量分时图')
        self.pictureTwoUpdate.clicked.connect(self.pushPictureTwo)
        pal = self.pictureTwoUpdate.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('black'))
        self.pictureTwoUpdate.setPalette(pal)
        self.layout.addWidget(self.pictureTwoUpdate,10,7)
        
        
        """--------------------------图片1信息order选择按钮--------------------------"""
        self.pictureOneOrderEdit = QtGui.QSpinBox()
        self.pictureOneOrderEdit.setRange(0,10000)
        self.layout.addWidget(self.pictureOneOrderEdit,10,8)
        
        
        """--------------------------附加参数窗口--------------------------"""
        self.poolType = QtGui.QPushButton(u'pool类型')
        self.layout.addWidget(self.poolType,0,8)
        self.poolTypeEdit = QtGui.QComboBox()
        self.poolTypeEdit.addItem("Backtest")
        self.poolTypeEdit.addItem("Realtime")
        self.layout.addWidget(self.poolTypeEdit,1,8)
        
        self.modeChoice = QtGui.QPushButton(u'模式')
        self.layout.addWidget(self.modeChoice,2,8)
        self.modeChoiceEdit = QtGui.QComboBox()
        self.modeChoiceEdit.addItem("Debug")
        self.modeChoiceEdit.addItem("Release")
        self.layout.addWidget(self.modeChoiceEdit,3,8)
        
        self.timeParaOne = QtGui.QPushButton(u'pool开始时间')
        self.layout.addWidget(self.timeParaOne,4,8)
        self.timeParaOneEdit = QtGui.QPushButton(u'开始时间编辑')
        self.layout.addWidget(self.timeParaOneEdit,5,8)
        self.timeParaOneEdit.clicked.connect(self.firstParaTimeEditFun)
        
        self.timeParaTwo = QtGui.QPushButton(u'pool结束时间')
        self.layout.addWidget(self.timeParaTwo,6,8)
        self.timeParaTwoEdit = QtGui.QPushButton(u'结束时间编辑')
        self.layout.addWidget(self.timeParaTwoEdit,7,8)
        self.timeParaTwoEdit.clicked.connect(self.secondParaTimeEditFun)
      
        
        """--------------------------附加参数确定按钮--------------------------"""
        self.confirmParaButton = QtGui.QPushButton(u'确定参数')
        self.confirmParaButton.clicked.connect(self.pushconfirmParaButtonFun)
        pal = self.confirmParaButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('red'))
        self.confirmParaButton.setPalette(pal)
        self.layout.addWidget(self.confirmParaButton,8,8)
        
        """--------------------------附加参数清空按钮--------------------------"""
        self.emptyParaButton = QtGui.QPushButton(u'清空参数')
        pal = self.emptyParaButton.palette()
        pal.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('red'))
        self.emptyParaButton.setPalette(pal)
        self.layout.addWidget(self.emptyParaButton,9,8)

        self.setLayout(self.layout)
        self.show()
        
             
    """--------------------------确认订单按钮--------------------------"""    
    def confirmOrderFun(self):
        print ("This is confirm order button")
        self.stockIdDisplay = self.stockIdEdit.currentText()
        self.stockId = int(self.stockIdEdit.currentText())
        self.startTimeDisplay = self.startTimeString
        self.startTime = datetime.datetime.strptime(self.startTimeString, "%Y-%m-%d %H:%M:%S")
        self.endTimeDisplay = self.endTimeString
        self.endTime = datetime.datetime.strptime(self.endTimeString, "%Y-%m-%d %H:%M:%S")
        self.stockAmountDisplay = self.stockAmountEdit.text()
        self.stockAmount = int(self.stockAmountEdit.text())
        self.buySellDisplay = self.operateTypeEdit.currentText()
        if(self.operateTypeEdit.currentText() == 'BUY'):
            self.buySell = tradingUnit.BUY
        else:
            self.buySell = tradingUnit.SELL
        self.algChoiceDisplay = self.algChoiceEdit.currentText()
        if(self.algChoiceEdit.currentText() == 'TWAP'):
            self.algChoice = clientOrder.TWAP
        elif(self.algChoiceEdit.currentText() == 'VWAP'):
            self.algChoice = clientOrder.VWAP
        else:
            self.algChoice = clientOrder.LINEARVWAP
        self.processIdDisplay = self.processIdEdit.currentText()
        self.processId = int(self.processIdEdit.currentText())
        self.tradingTypeDisplay = self.tradingTypeEdit.currentText()
        self.tradingType = 1
        #self.orderId+=1
        
        order = clientOrder()
        order.create_order(self.stockId, self.startTime, self.endTime, self.stockAmount, self.buySell, self.algChoice, self.processId, self.tradingType)

        repoAT = repoForAT('algotrading', '12345678', None, False)
        repoAT.insert_order(order)
        orderList = repoAT.extract_all_orders()
        rowIndex = 1
        for order in orderList:
            self.fillInputTable(order, rowIndex)
            rowIndex = rowIndex + 1

        """在此将输入数据导入数据库
            注意相应数据的格式，string转int datetime等"""

        
    def emptyOrderFun(self):
        print "empty order"
        repoAT = repoForAT('algotrading', '12345678', None, False)
        orderList = repoAT.extract_all_orders()
        allRow = len(orderList)
        repoAT.delete_all_orders()
        for rowIndex in range(1, allRow + 1):
            self.clearInputTable(rowIndex)
            rowIndex = rowIndex + 1
        return
    def clearInputTable(self, rownumber):
        self.inputTableLabel.setItem(rownumber,0, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,1, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,4, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,5, QtGui.QTableWidgetItem(""))
        self.inputTableLabel.setItem(rownumber,6, QtGui.QTableWidgetItem(""))

    # rowNumber from 1
    def fillInputTable(self, order, rownumber):
        self.inputTableLabel.setItem(rownumber,0, QtGui.QTableWidgetItem(str(order.orderId)))
        self.inputTableLabel.setItem(rownumber,1, QtGui.QTableWidgetItem(str(order.stockId)))
        self.inputTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem(str(order.startTime)))
        self.inputTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem(str(order.endTime)))
        self.inputTableLabel.setItem(rownumber,4, QtGui.QTableWidgetItem(str(order.stockAmount)))
        if order.buySell == tradingUnit.BUY:
            self.inputTableLabel.setItem(rownumber,5, QtGui.QTableWidgetItem("BUY"))
        else:
            self.inputTableLabel.setItem(rownumber,5, QtGui.QTableWidgetItem("SELL"))
        if order.algChoice == clientOrder.TWAP:
            self.inputTableLabel.setItem(rownumber,6, QtGui.QTableWidgetItem("TWAP"))
        elif order.algChoice == clientOrder.VWAP:
            self.inputTableLabel.setItem(rownumber,6, QtGui.QTableWidgetItem("VWAP"))
        elif order.algChoice == clientOrder.LINEARVWAP:
            self.inputTableLabel.setItem(rownumber,6, QtGui.QTableWidgetItem("LINEARVWAP"))
        #self.inputTableLabel.setItem(rownumber,7, QtGui.QTableWidgetItem(self.processIdDisplay))
        #self.inputTableLabel.setItem(rownumber,8, QtGui.QTableWidgetItem(self.tradingTypeDisplay))
    def pushInputInfoUpdateFun(self):

        repoAT = repoForAT('algotrading', '12345678', None, False)
        orderList = repoAT.extract_all_orders()
        rowIndex = 1
        for order in orderList:
            self.fillInputTable(order, rowIndex)
            rowIndex = rowIndex + 1


    
    def pushOutputInfoUpdateFun(self):
        """在此从数据库中导入输出数据
            注意相应数据的格式，int datetime转string等"""
        print "read output"
        repoAT = repoForAT('algotrading', '12345678', None, False)
        orderList = repoAT.extract_all_orders()
        rownumber = 1
        for order in orderList:
            self.outputTableLabel.setItem(rownumber,0, QtGui.QTableWidgetItem(str(order.orderId)))
            self.outputTableLabel.setItem(rownumber,1, QtGui.QTableWidgetItem(str(order.stockId)))
            if order.status == clientOrder.UNINIT:
                self.outputTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem("waiting to init"))
            elif order.status == clientOrder.INIT:
                self.outputTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem("doing"))
            elif order.status == clientOrder.COMPLETED:
                self.outputTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem("completed"))

            self.outputTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem(str(order.completedAmount)))
            self.outputTableLabel.setItem(rownumber,4, QtGui.QTableWidgetItem(str(order.trunOver)))
            self.outputTableLabel.setItem(rownumber,5, QtGui.QTableWidgetItem(str(order.avgPrice)))
            rownumber = rownumber + 1
            
    def pushMonitorPoolUpdateFun(self):
        print "read pool"
        repoMonitor = tradingRecordSaver('algotrading', '12345678', None, False)

        tradeList = repoMonitor.get_history_record()
        """在此从数据库中导入输出数据
            注意相应数据的格式，int datetime转string等"""
        rownumber = 1
        print "poolNumber", len(tradeList)
        for tradeOrder in tradeList:
            self.monitorPoolTableLabel.setItem(rownumber,0, QtGui.QTableWidgetItem(str(tradeOrder.tradingUnitId)))
            self.monitorPoolTableLabel.setItem(rownumber,1, QtGui.QTableWidgetItem(str(tradeOrder.stockId)))
            self.monitorPoolTableLabel.setItem(rownumber,2, QtGui.QTableWidgetItem(str(tradeOrder.time)))
            if tradeOrder.buysell == tradingUnit.BUY:
                self.monitorPoolTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem("BUY"))
            elif tradeOrder.buysell == tradingUnit.SELL:
                self.monitorPoolTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem("SELL"))
            else:
                self.monitorPoolTableLabel.setItem(rownumber,3, QtGui.QTableWidgetItem("OTHER"))
            if tradeOrder.tradingType == tradingUnit.FIRST_PRICE_ORDER:
                self.monitorPoolTableLabel.setItem(rownumber,4, QtGui.QTableWidgetItem("LIMIT PRICE"))
            elif tradeOrder.tradingType == tradingUnit.ALL_PRICE_ORDER:
                self.monitorPoolTableLabel.setItem(rownumber,4, QtGui.QTableWidgetItem("MARKET PRICE"))

            self.monitorPoolTableLabel.setItem(rownumber,5, QtGui.QTableWidgetItem(str(tradeOrder.amount)))
            self.monitorPoolTableLabel.setItem(rownumber,6, QtGui.QTableWidgetItem(str(tradeOrder.price)))
            self.monitorPoolTableLabel.setItem(rownumber,7, QtGui.QTableWidgetItem(str(tradeOrder.succAmount)))
            self.monitorPoolTableLabel.setItem(rownumber,8, QtGui.QTableWidgetItem(str(tradeOrder.succMoney)))
            rownumber = rownumber + 1
        
    def pushconfirmParaButtonFun(self):
        self.firstTime = datetime.datetime.strptime(self.firstTimeString, "%Y-%m-%d %H:%M:%S")
        self.secondTime = datetime.datetime.strptime(self.secondTimeString, "%Y-%m-%d %H:%M:%S")
        if(self.modeChoiceEdit.currentText()=='Debug'):
            isOpenLog = True
        else:
            isOpenLog = False
        if(self.poolTypeEdit.currentText()=='Realtime'):
            isRealtime = True
        else:
            isRealtime = False
        # TODO open algotrading
        print self.firstTime, self.secondTime, isOpenLog, isRealtime
        if self.p != None:
            isOpenProcess = self.p.is_alive()
            print "push run button, isOpen:", isOpenProcess
        else:
            isOpenProcess = False
        if isOpenProcess:
            print "process is open, could not open another"
        else:
            print "run pool"
            self.p = HistoryPoolProcess(self.firstTime,self.secondTime, 7, isOpenLog)
            self.p.start()


          
    """--------------------------编辑开始时间窗口定义--------------------------"""
    def startTimeEditFun(self):
        print ("This is start time edit")
        customQDialog = QtGui.QDialog()
        customQDialog.setWindowTitle(u'编辑开始时间窗口')
        layout = QtGui.QGridLayout()
        
        startyear = QtGui.QPushButton(u'年')
        layout.addWidget(startyear,0,0)
        self.startYearEdit = QtGui.QLineEdit()
        layout.addWidget(self.startYearEdit,1,0)
        
        startmonth = QtGui.QPushButton(u'月')
        layout.addWidget(startmonth,0,1)
        self.startMonthEdit = QtGui.QLineEdit()
        layout.addWidget(self.startMonthEdit,1,1)
        
        startday = QtGui.QPushButton(u'日')
        layout.addWidget(startday,0,2)
        self.startDayEdit = QtGui.QLineEdit()
        layout.addWidget(self.startDayEdit,1,2)
        
        starthour = QtGui.QPushButton(u'时')
        layout.addWidget(starthour,2,0)
        self.startHourEdit = QtGui.QLineEdit()
        layout.addWidget(self.startHourEdit,3,0)
        
        startminute = QtGui.QPushButton(u'分')
        layout.addWidget(startminute,2,1)
        self.startMinuteEdit = QtGui.QLineEdit()
        layout.addWidget(self.startMinuteEdit,3,1)
        
        startsecond = QtGui.QPushButton(u'秒')
        layout.addWidget(startsecond,2,2)
        self.startSecondEdit = QtGui.QLineEdit()
        layout.addWidget(self.startSecondEdit,3,2)
        
        startconfirm = QtGui.QPushButton(u'确定')
        layout.addWidget(startconfirm,4,0)
        
        startemptyset = QtGui.QPushButton(u'默认设置')
        layout.addWidget(startemptyset,4,1,1,2)
        
        startconfirm.clicked.connect(self.pushStartTimeConfirm)
        startemptyset.clicked.connect(self.pushStartTimeEmpty)
        
        customQDialog.setLayout(layout)
        customQDialog.exec_()
   
    """--------------------------编辑结束时间窗口定义--------------------------"""
    def endTimeEditFun(self):
        print ("This is end time edit")
        customQDialog = QtGui.QDialog()
        customQDialog.setWindowTitle(u'编辑结束时间窗口')
        layout = QtGui.QGridLayout()
        
        endyear = QtGui.QPushButton(u'年')
        layout.addWidget(endyear,0,0)
        self.endYearEdit = QtGui.QLineEdit()
        layout.addWidget(self.endYearEdit,1,0)
        
        endmonth = QtGui.QPushButton(u'月')
        layout.addWidget(endmonth,0,1)
        self.endMonthEdit = QtGui.QLineEdit()
        layout.addWidget(self.endMonthEdit,1,1)
        
        endday = QtGui.QPushButton(u'日')
        layout.addWidget(endday,0,2)
        self.endDayEdit = QtGui.QLineEdit()
        layout.addWidget(self.endDayEdit,1,2)
        
        endhour = QtGui.QPushButton(u'时')
        layout.addWidget(endhour,2,0)
        self.endHourEdit = QtGui.QLineEdit()
        layout.addWidget(self.endHourEdit,3,0)
        
        endminute = QtGui.QPushButton(u'分')
        layout.addWidget(endminute,2,1)
        self.endMinuteEdit = QtGui.QLineEdit()
        layout.addWidget(self.endMinuteEdit,3,1)
        
        endsecond = QtGui.QPushButton(u'秒')
        layout.addWidget(endsecond,2,2)
        self.endSecondEdit = QtGui.QLineEdit()
        layout.addWidget(self.endSecondEdit,3,2)
        
        endconfirm = QtGui.QPushButton(u'确定')
        layout.addWidget(endconfirm,4,0)
        
        endemptyset = QtGui.QPushButton(u'默认设置')
        layout.addWidget(endemptyset,4,1,1,2)
        
        endconfirm.clicked.connect(self.pushEndTimeConfirm)
        endemptyset.clicked.connect(self.pushEndTimeEmpty)
        
        customQDialog.setLayout(layout)
        customQDialog.exec_()



    def firstParaTimeEditFun(self):
    	print ("This is first time edit")
        customQDialog = QtGui.QDialog()
        customQDialog.setWindowTitle(u'编辑pool开始时间窗口')
        layout = QtGui.QGridLayout()
        
        firstyear = QtGui.QPushButton(u'年')
        layout.addWidget(firstyear,0,0)
        self.firstYearEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstYearEdit,1,0)
        
        firstmonth = QtGui.QPushButton(u'月')
        layout.addWidget(firstmonth,0,1)
        self.firstMonthEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstMonthEdit,1,1)
        
        firstday = QtGui.QPushButton(u'日')
        layout.addWidget(firstday,0,2)
        self.firstDayEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstDayEdit,1,2)
        
        firsthour = QtGui.QPushButton(u'时')
        layout.addWidget(firsthour,2,0)
        self.firstHourEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstHourEdit,3,0)
        
        firstminute = QtGui.QPushButton(u'分')
        layout.addWidget(firstminute,2,1)
        self.firstMinuteEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstMinuteEdit,3,1)
        
        firstsecond = QtGui.QPushButton(u'秒')
        layout.addWidget(firstsecond,2,2)
        self.firstSecondEdit = QtGui.QLineEdit()
        layout.addWidget(self.firstSecondEdit,3,2)
        
        firstconfirm = QtGui.QPushButton(u'确定')
        layout.addWidget(firstconfirm,4,0)
        
        firstemptyset = QtGui.QPushButton(u'默认设置')
        layout.addWidget(firstemptyset,4,1,1,2)
        
        firstconfirm.clicked.connect(self.pushFirstTimeConfirm)
        firstemptyset.clicked.connect(self.pushFirstTimeEmpty)
        
        customQDialog.setLayout(layout)
        customQDialog.exec_()

    def secondParaTimeEditFun(self):
    	print ("This is second time edit")
        customQDialog = QtGui.QDialog()
        customQDialog.setWindowTitle(u'编辑pool结束窗口')
        layout = QtGui.QGridLayout()
        
        secondyear = QtGui.QPushButton(u'年')
        layout.addWidget(secondyear,0,0)
        self.secondYearEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondYearEdit,1,0)
        
        secondmonth = QtGui.QPushButton(u'月')
        layout.addWidget(secondmonth,0,1)
        self.secondMonthEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondMonthEdit,1,1)
        
        secondday = QtGui.QPushButton(u'日')
        layout.addWidget(secondday,0,2)
        self.secondDayEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondDayEdit,1,2)
        
        secondhour = QtGui.QPushButton(u'时')
        layout.addWidget(secondhour,2,0)
        self.secondHourEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondHourEdit,3,0)
        
        secondminute = QtGui.QPushButton(u'分')
        layout.addWidget(secondminute,2,1)
        self.secondMinuteEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondMinuteEdit,3,1)
        
        secondsecond = QtGui.QPushButton(u'秒')
        layout.addWidget(secondsecond,2,2)
        self.secondSecondEdit = QtGui.QLineEdit()
        layout.addWidget(self.secondSecondEdit,3,2)
        
        secondconfirm = QtGui.QPushButton(u'确定')
        layout.addWidget(secondconfirm,4,0)
        
        secondemptyset = QtGui.QPushButton(u'默认设置')
        layout.addWidget(secondemptyset,4,1,1,2)
        
        secondconfirm.clicked.connect(self.pushSecondTimeConfirm)
        secondemptyset.clicked.connect(self.pushSecondTimeEmpty)
        
        customQDialog.setLayout(layout)
        customQDialog.exec_()
    
    """--------------------------确认开始时间设置--------------------------"""
    def pushStartTimeConfirm(self):
        self.startYear = int(self.startYearEdit.text())
        self.startMonth = int(self.startMonthEdit.text()) 
        self.startDay = int(self.startDayEdit.text())     
        self.startHour = int(self.startHourEdit.text())     
        self.startMinute = int(self.startMinuteEdit.text())    
        self.startSecond = int(self.startSecondEdit.text())    
        self.startTimeString = str(self.startYear)+'-'+str(self.startMonth)+'-'+str(self.startDay)+' '+str(self.startHour)+':'+str(self.startMinute)+':'+str(self.startSecond)
        self.startTimeEdit.setText(self.startTimeString)
    
    """--------------------------默认开始时间设置--------------------------"""
    def pushStartTimeEmpty(self):
        self.startYearEdit.setText('2016')
        self.startYear = 2016
        self.startMonthEdit.setText('12')
        self.startMonth = 12
        self.startDayEdit.setText('22')
        self.startDay = 22
        self.startHourEdit.setText('9')
        self.startHour = 9
        self.startMinuteEdit.setText('30')
        self.startMinute = 30
        self.startSecondEdit.setText('00')
        self.startSecond = 00
    
    """--------------------------确定结束时间设置--------------------------"""
    def pushEndTimeConfirm(self):
        self.endYear = int(self.endYearEdit.text())
        self.endMonth = int(self.endMonthEdit.text()) 
        self.endDay = int(self.endDayEdit.text())     
        self.endHour = int(self.endHourEdit.text())     
        self.endMinute = int(self.endMinuteEdit.text())    
        self.endSecond = int(self.endSecondEdit.text())    
        self.endTimeString = str(self.endYear)+'-'+str(self.endMonth)+'-'+str(self.endDay)+' '+str(self.endHour)+':'+str(self.endMinute)+':'+str(self.endSecond)
        self.endTimeEdit.setText(self.endTimeString)
    
    """--------------------------默认结束时间设置--------------------------"""
    def pushEndTimeEmpty(self):
        self.endYearEdit.setText('2016')
        self.endYear = 2016
        self.endMonthEdit.setText('12')
        self.endMonth = 12
        self.endDayEdit.setText('23')
        self.endDay = 23
        self.endHourEdit.setText('15')
        self.endHour = 15
        self.endMinuteEdit.setText('00')
        self.endMinute = 0   
        self.endSecondEdit.setText('00')
        self.endSecond = 0


    """--------------------------确定开始时间设置--------------------------"""
    def pushFirstTimeConfirm(self):
        self.firstYear = int(self.firstYearEdit.text())
        self.firstMonth = int(self.firstMonthEdit.text()) 
        self.firstDay = int(self.firstDayEdit.text())     
        self.firstHour = int(self.firstHourEdit.text())     
        self.firstMinute = int(self.firstMinuteEdit.text())    
        self.firstSecond = int(self.firstSecondEdit.text())    
        self.firstTimeString = str(self.firstYear)+'-'+str(self.firstMonth)+'-'+str(self.firstDay)+' '+str(self.firstHour)+':'+str(self.firstMinute)+':'+str(self.firstSecond)
        self.timeParaOneEdit.setText(self.firstTimeString)
        self.firstTime = datetime.datetime.strptime(self.firstTimeString, "%Y-%m-%d %H:%M:%S")
        self.firstTimeEdit.setText(self.firstTimeString)
    
    """--------------------------默认开始时间设置--------------------------"""
    def pushFirstTimeEmpty(self):
        self.firstYearEdit.setText('2016')
        self.firstYear = 2016
        self.firstMonthEdit.setText('12')
        self.firstMonth = 12
        self.firstDayEdit.setText('22')
        self.firstDay = 22
        self.firstHourEdit.setText('9')
        self.firstHour = 9
        self.firstMinuteEdit.setText('30')
        self.firstMinute = 30
        self.firstSecondEdit.setText('00')
        self.firstSecond = 0

    """--------------------------确定结束时间设置--------------------------"""
    def pushSecondTimeConfirm(self):
        self.secondYear = int(self.secondYearEdit.text())
        self.secondMonth = int(self.secondMonthEdit.text()) 
        self.secondDay = int(self.secondDayEdit.text())     
        self.secondHour = int(self.secondHourEdit.text())     
        self.secondMinute = int(self.secondMinuteEdit.text())    
        self.secondSecond = int(self.secondSecondEdit.text())    
        self.secondTimeString = str(self.secondYear)+'-'+str(self.secondMonth)+'-'+str(self.secondDay)+' '+str(self.secondHour)+':'+str(self.secondMinute)+':'+str(self.secondSecond)
        self.timeParaTwoEdit.setText(self.secondTimeString)
        self.secondTime = datetime.datetime.strptime(self.secondTimeString, "%Y-%m-%d %H:%M:%S")
        self.secondTimeEdit.setText(self.secondTimeString)
    
    """--------------------------清空结束时间设置--------------------------"""
    def pushSecondTimeEmpty(self):
        self.secondYearEdit.setText('2016')
        self.secondYear = 2016
        self.secondMonthEdit.setText('12')
        self.secondMonth = 12
        self.secondDayEdit.setText('23')
        self.secondDay = 23
        self.secondHourEdit.setText('15')
        self.secondHour = 15
        self.secondMinuteEdit.setText('00')
        self.secondMinute = 0   
        self.secondSecondEdit.setText('00')
        self.secondSecond = 0

    
        
    def pushOutputUpdate(self):
        print ("Output Data Update")
     
    """--------------------------按下刷新图片1--------------------------"""
    def pushPictureOne(self):
        print ("Picture One Update")
        pictureString = self.pictureOneOrderEdit.text()
        self.pictureOneUpdate.setText(u'累积图orderId:'+ pictureString)
        self.pictureTwoUpdate.setText(u"刷新分时图")
        repoAT = repoForAT('algotrading', '12345678', None, False)
        repoMonitor = tradingRecordSaver('algotrading', '12345678', None, False)
        repoHistory = repo(False, True, None, "algotrading", '12345678', None, False)
        chart = chartCreater(repoHistory, repoAT, repoMonitor)
        chart.get_chart(int(pictureString))
        self.pictureOneLabel.setPixmap(QtGui.QPixmap('../tradePercentage.jpg').scaled(self.pictureOneLabel.size()))
        self.layout.addWidget(self.pictureOneLabel,11,6, 20,3)
     
    """--------------------------按下刷新图片2--------------------------"""
    def pushPictureTwo(self):
        print ("Picture Two Update")
        pictureString = self.pictureOneOrderEdit.text()
        self.pictureTwoUpdate.setText(u'分时图orderId:'+ pictureString)
        self.pictureOneUpdate.setText(u"刷新累积图")
        repoAT = repoForAT('algotrading', '12345678', None, False)
        repoMonitor = tradingRecordSaver('algotrading', '12345678', None, False)
        repoHistory = repo(False, True, None, "algotrading", '12345678', None, False)
        chart = chartCreater(repoHistory, repoAT, repoMonitor)
        chart.get_bar(int(pictureString))
        self.pictureOneLabel.setPixmap(QtGui.QPixmap('../tradePercentage.jpg').scaled(self.pictureOneLabel.size()))
        self.layout.addWidget(self.pictureTwoLabel,11,6, 20,3)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



class HistoryPoolProcess(multiprocessing.Process):
        def __init__(self, startTime, endTime, findDays, isOpenLog):
            multiprocessing.Process.__init__(self)
            self.startTime = startTime
            self.endTime = endTime
            self.isOpenLog = isOpenLog
            self.findDays = findDays

        def run(self):
            print "into history pool"
            isOpenLog = self.isOpenLog
            startTime = self.startTime
            endTime = self.endTime
            findLastDays = self.findDays

            # 初始化algotrading的repo
            rat = repoForAT("algotrading", "12345678", None, isOpenLog = isOpenLog)

            # 初始化pool
            poolDataMarketGetter = marketDataGetter(isOpenLog = isOpenLog)
            poolDataRepoGetter = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
            poolRecordSaver = tradingRecordSaver("algotrading", "12345678", None, isOpenLog = isOpenLog)
            poolRealTime = poolFromSinaApi(poolDataMarketGetter, True, poolRecordSaver, isOpenLog = isOpenLog)
            poolHistory = poolFromSinaApi(poolDataRepoGetter, False, poolRecordSaver, isOpenLog = isOpenLog)
            
            # 初始化quantAnalysisDict
            repoForQuantAnalysis = repo(isSqlite = False, isMysql = True, file_path = "", user = "algotrading", password = "12345678", ip = None, isOpenLog = isOpenLog)
            quantAnalysisDict = {}
            quantAnalysisDict[clientOrder.TWAP] = TWAPQuantAnalysis(isOpenLog = isOpenLog)
            quantAnalysisDict[clientOrder.VWAP] = VWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
            quantAnalysisDict[clientOrder.LINEARVWAP] = LinearVWAPQuantAnalysis(repoForQuantAnalysis, isOpenLog = isOpenLog)
         

            algoTradingEngine = algoTrading( rat, poolHistory, quantAnalysisDict, findLastDays, isOpenLog = isOpenLog)

            print "init succ"

            index = 0
            while(startTime < endTime):
                algoTradingEngine.set_time(startTime)
                startTime = startTime + datetime.timedelta(minutes = 1)
                algoTradingEngine.init_orders()
                algoTradingEngine.refresh()
                algoTradingEngine.trade_request()
                algoTradingEngine.complete_orders()
                index = index + 1
                if index%60 == 0:
                    print "now time:" + str(startTime)


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = TestWindow()
    mainWindow.show()
    sys.exit(app.exec_())
