# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 21:21:11 2016

@author: user
"""


# -*- coding: utf-8 -*-

import sys
import pandas as pd
from PyQt4 import QtGui
from PyQt4 import QtCore



class TestWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(TestWindow, self).__init__(parent)
        self.setWindowTitle(u'算法交易')


        self.type = QtGui.QPushButton(u'操作类型')
        self.typeEdit = QtGui.QComboBox()
        self.typeEdit.addItem("BUY")
        self.typeEdit.addItem("SELL")
        
        self.algorithm = QtGui.QPushButton(u'算法选择')
        self.algorithmEdit = QtGui.QComboBox()
        self.algorithmEdit.addItem("TWAP")
        self.algorithmEdit.addItem("VWAP")
        self.algorithmEdit.addItem("Other")
        
        self.volumn = QtGui.QPushButton(u'交易数量')
        self.volumnEdit = QtGui.QSpinBox()
        self.volumnEdit.setRange(0,10000)
        

        self.stock = QtGui.QPushButton(u'股票ID')
        self.stockEdit = QtGui.QComboBox()
        self.stockEdit.addItem("100000")
        self.stockEdit.addItem("100006")
        self.stockEdit.addItem("Other")
        
        self.number = QtGui.QPushButton(u'股票数量')
        self.numberEdit = QtGui.QSpinBox()
        self.numberEdit.setRange(0,10000)
        
        self.price = QtGui.QPushButton(u'股票价格')
        self.priceEdit = QtGui.QLineEdit()


        self.textEdit1 = QtGui.QTextEdit()
        self.textEdit2 = QtGui.QTextEdit()
        self.textEdit3 = QtGui.QTextEdit()
        
        self.pictureLabel = QtGui.QLabel()
        self.pictureLabel.setPixmap(QtGui.QPixmap('C:\\Users\\user\\Desktop\\kline.png'))
        self.pictureTitleLabel = QtGui.QLabel(u'k线图更新')
        
        self.tableLabel = QtGui.QTableWidget()
        self.tableLabel.setColumnCount(2)
        self.tableLabel.setRowCount(10)
        """self.tableLabel."""
        self.tableLabel.setItem(0,0, QtGui.QTableWidgetItem(u'股票ID'))
        self.tableLabel.setItem(1,0, QtGui.QTableWidgetItem(u'股票数量'))
        self.tableLabel.setItem(2,0, QtGui.QTableWidgetItem(u'股票价格'))
        self.tableLabel.setItem(3,0, QtGui.QTableWidgetItem(u'操作类型'))
        self.tableLabel.setItem(4,0, QtGui.QTableWidgetItem(u'算法选择'))
        self.tableLabel.setItem(5,0, QtGui.QTableWidgetItem(u'交易数量'))
        
        layout = QtGui.QGridLayout()

        layout.addWidget(self.stock,0,0)
        layout.addWidget(self.stockEdit,0,1)
        layout.addWidget(self.number,0,2)
        layout.addWidget(self.numberEdit,0,3)
        layout.addWidget(self.price,0,4)
        layout.addWidget(self.priceEdit,0,5)
        layout.addWidget(self.pictureTitleLabel,0,6)
        
        layout.addWidget(self.textEdit1,1,0, 10,2)
        layout.addWidget(self.textEdit2,1,2, 5,2)
        layout.addWidget(self.textEdit3,6,2, 5,2)
        layout.addWidget(self.tableLabel,1,4, 10,2)
        layout.addWidget(self.pictureLabel,1,6, 10,2)
        
        layout.addWidget(self.type,11,0)
        layout.addWidget(self.typeEdit,11,1)
        layout.addWidget(self.algorithm,11,2)
        layout.addWidget(self.algorithmEdit,11,3)
        layout.addWidget(self.volumn,11,4)
        layout.addWidget(self.volumnEdit,11,5)

        self.setLayout(layout)

        self.stock.clicked.connect(self.pushStock)
        self.number.clicked.connect(self.pushNumber)
        self.price.clicked.connect(self.pushPrice)
        self.type.clicked.connect(self.pushType)
        self.algorithm.clicked.connect(self.pushAlgorithm)
        self.volumn.clicked.connect(self.pushVolumn)

        self.show()

    def pushStock(self):
        stockIDString = self.stockEdit.currentIndex()
        if(stockIDString == 0):
            self.tableLabel.setItem(0,1, QtGui.QTableWidgetItem(u'100000'))
        if(stockIDString == 1):
            self.tableLabel.setItem(0,1, QtGui.QTableWidgetItem(u'100006'))
     
    def pushNumber(self):
        numberString = self.numberEdit.text()
        self.tableLabel.setItem(1,1, QtGui.QTableWidgetItem(numberString))
        
    def pushPrice(self):
        priceString = self.priceEdit.text()
        self.tableLabel.setItem(2,1, QtGui.QTableWidgetItem(priceString))

    def pushType(self):
        typeString = self.typeEdit.currentText()
        print(typeString)
        self.tableLabel.setItem(3,1, QtGui.QTableWidgetItem(typeString))

    def pushAlgorithm(self):
        algorithmString = self.algorithmEdit.currentText()
        self.tableLabel.setItem(4,1, QtGui.QTableWidgetItem(algorithmString))

    def pushVolumn(self):
        volumnString = self.volumnEdit.text()
        self.tableLabel.setItem(5,1, QtGui.QTableWidgetItem(volumnString))


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = TestWindow()
    mainWindow.show()
    sys.exit(app.exec_())