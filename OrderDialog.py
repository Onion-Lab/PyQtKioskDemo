from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from ProductButton import ProductButton

import os
import json
import random

global gProductInfoFilePath
gProductInfoFilePath = 'productsinformation.json'

class OrderDialog(QDialog):
    acceptSignal = pyqtSignal(dict)
    def __init__(self, parent):
        QDialog.__init__(self)
        uic.loadUi('OrderDialog.ui', self)
        self.parent = parent
        self.__productDict = dict()
        self.__recommendButton = list()
        self.__addedMenuDict = dict()
        
        self.__initSlot()
        self.recommendTable.verticalHeader().setVisible(False)
        self.recommendTable.setColumnWidth(0, 144)
        self.recommendTable.setColumnWidth(1, 144)
        self.recommendTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        if os.path.isfile(gProductInfoFilePath):
            self.__productDict = json.load(open(gProductInfoFilePath, 'r', encoding='utf-8'))
        
        for idx in range(len(self.__productDict)):
            if self.__productDict[str(idx)][2] is None:
                del self.__productDict[str(idx)]
        
        currentRowCount = parent.orderTable.rowCount()
        for idx in range(currentRowCount):
            self.recommendTable.insertRow(idx)
            for pIdx in range(len(self.__productDict)):
                if parent.orderTable.item(idx, 0).text() == self.__productDict[str(pIdx)][0]:
                    # Add chose menu
                    orderButton = ProductButton(idx, self.__productDict[str(pIdx)][0], self.__productDict[str(pIdx)][1], self.__productDict[str(pIdx)][2])
                    self.__addWidgetInTable(orderButton, idx, 0)
                    break
            # Add recommend menu
            randIdx = random.randrange(0, len(self.__productDict))
            self.__recommendButton.append(ProductButton(idx, self.__productDict[str(randIdx)][0], self.__productDict[str(randIdx)][1], self.__productDict[str(randIdx)][2]))
            self.__recommendButton[idx].productClickedSignal.connect(self.onProductClickedSlot)
            self.__addWidgetInTable(self.__recommendButton[idx], idx, 1)

            # Add pcs widget
            pcsLabel = QLabel('0')
            pcsLabel.setFont(QFont('Consolas', 10))
            self.__addWidgetInTable(pcsLabel, idx, 2)

    def __initSlot(self):
        self.accepted.connect(self.onAcceptButtonClicked)
        
    def __addWidgetInTable(self, widget, row, col):
        self.recommendTable.setCellWidget(row, col, widget)
        self.recommendTable.resizeRowToContents(row)

    @pyqtSlot()
    def onAcceptButtonClicked(self):
        self.acceptSignal.emit(self.__addedMenuDict)

    @pyqtSlot(int)
    def onProductClickedSlot(self, productNum):
        name, _, price = self.__recommendButton[productNum].getInformation()
        if name in self.__addedMenuDict:
            self.__addedMenuDict[name]['pcs'] += 1
        else:
            self.__addedMenuDict[name] = {'pcs': 1, 'price': price}

        if price != None:
            pcs = int(self.recommendTable.cellWidget(productNum, 2).text()) + 1
            self.recommendTable.cellWidget(productNum, 2).setText(str(pcs))