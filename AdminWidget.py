from itertools import product
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from ProductButton import ProductButton
from SetProductDialog import SetProductDialog

import os
import json

global gProductInfoFilePath
gProductInfoFilePath = 'productsinformation.json'

class AdminWidget(QWidget):
    backButtonSignal = pyqtSignal()

    def __init__(self, productNum, rowNum):
        super().__init__()
        uic.loadUi('AdminWidget.ui', self)
    
        global gProductInfoFilePath
        self.__initSlot()
        self.__addProduct = SetProductDialog(self)
        

        self.__productNum = productNum
        self.__selectedProductNum = 0
        self.__rowNum = rowNum
        self.__productList = []
        self.__productDict = dict()

        if os.path.isfile(gProductInfoFilePath):
            self.__productDict = json.load(open(gProductInfoFilePath, 'r', encoding='utf-8'))
        else:
            for idx in range(self.__productNum):
                self.__productDict[idx] = ['', '', None]

        for idx in range(self.__productNum):
            self.__productList.append(ProductButton(idx, self.__productDict[str(idx)][0], self.__productDict[str(idx)][1], self.__productDict[str(idx)][2]))
            self.__productList[idx].productClickedSignal.connect(self.onProductClickedSlot)
            self.productLayout.addWidget(self.__productList[idx], idx//self.__rowNum, idx%self.__rowNum)

        self.revenueTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.revenueTable.verticalHeader().setVisible(False)
        self.revenueTable.setColumnWidth(0, 40)
        self.revenueTable.setColumnWidth(1, 120)
        self.revenueTable.setColumnWidth(2, 40)
        self.revenueTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    def __initSlot(self) :
        self.backButton.clicked.connect(self.onBackButtonClicked)
        self.loadButton.clicked.connect(self.onLoadButtonClicked)
        self.clearButton.clicked.connect(self.onClearButtonClicked)

    def __clearWidget(self):
        self.revenueTable.clearContents()
        self.revenueTable.setRowCount(0)
        self.revenueEdit.clear()
        self.dateLabel.clear()

    @pyqtSlot()
    def onBackButtonClicked(self):
        self.backButtonSignal.emit()

    @pyqtSlot()
    def onLoadButtonClicked(self):
        filePathTuple = QFileDialog.getOpenFileName(self, "Open", "revenue_list", "Select file (*.json)")
        if filePathTuple[0] != '':
            if os.path.isfile(filePathTuple[0]):
                self.dateLabel.setText(os.path.basename(filePathTuple[0]).replace('.json', '') + ' 매출')
                loadRevenue = json.load(open(filePathTuple[0], 'r', encoding='utf-8'))
                totalRevenue = 0
                rowCount = 0
                for idx in range(len(loadRevenue)):
                    orderNumberStr = str(idx+1)
                    totalRevenue += loadRevenue[str(idx+1)]['total']
                    orderList = loadRevenue[str(idx+1)]['order_list']
                    for orderIdx in range(len(orderList)):
                        self.revenueTable.insertRow(rowCount)
                        self.revenueTable.setItem(rowCount, 0, QTableWidgetItem(orderNumberStr))
                        self.revenueTable.setItem(rowCount, 1, QTableWidgetItem(orderList[orderIdx]['menu']))
                        self.revenueTable.setItem(rowCount, 2, QTableWidgetItem(str(orderList[orderIdx]['pcs'])))
                        self.revenueTable.setItem(rowCount, 3, QTableWidgetItem(format(orderList[orderIdx]['price'], ',')))
                        rowCount += 1
                    
                self.revenueEdit.setText(format(totalRevenue, ',') + '')

    @pyqtSlot()
    def onClearButtonClicked(self):
        self.__clearWidget()

    @pyqtSlot(int)
    def onProductClickedSlot(self, productNum):
        self.__selectedProductNum = productNum
        self.__addProduct.show()
        #name, imagePath, price = self.__addProduct.getInformation()
        print("text")

    @pyqtSlot(str,str,int)
    def onSetProductSaveSlot(self,name, imagePath, price) :
        self.__productList[self.__selectedProductNum].setInformation(name, imagePath, price)
        self.__productDict[str(self.__selectedProductNum)][0], self.__productDict[str(self.__selectedProductNum)][1], self.__productDict[str(self.__selectedProductNum)][2] = self.__productList[self.__selectedProductNum].getInformation()
        global gProductInfoFilePath
        with open(gProductInfoFilePath, 'w', encoding='utf-8') as fp:
            json.dump(self.__productDict, fp, sort_keys=False, indent=4, separators=(',', ':'))
    