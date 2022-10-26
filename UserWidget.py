from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from ProductButton import ProductButton
from OrderDialog import OrderDialog

import os
import json
import datetime

global gProductInfoFilePath
gProductInfoFilePath = 'productsinformation.json'

class UserWidget(QWidget):
    backButtonSignal = pyqtSignal()

    def __init__(self, productNum, rowNum):
        super().__init__()
        uic.loadUi('UserWidget.ui', self)

        self.__initSlot()
        
        self.__productNum = productNum
        self.__rowNum = rowNum
        self.productList = []
        self.__productDict = dict()
        self.__addedMenuDict = None

        self.__orderStatus = True
        self.__date = ''
        self.__orderNumber = 0

        if os.path.isfile(gProductInfoFilePath):
            self.__productDict = json.load(open(gProductInfoFilePath, 'r', encoding='utf-8'))
        else:
            for idx in range(self.__productNum):
                self.__productDict[idx] = ['', '', None]
                
        for idx in range(self.__productNum):
            tmpWidget = None
            if self.__productDict[str(idx)][2] == None:
                tempLabel = QLabel('')
                tempLabel.setFixedSize(128, 143)
                tmpWidget = tempLabel
            else:
                self.productList.append(ProductButton(idx, self.__productDict[str(idx)][0], self.__productDict[str(idx)][1], self.__productDict[str(idx)][2]))
                self.productList[idx].productClickedSignal.connect(self.onProductClickedSlot)
                tmpWidget = self.productList[idx]
            self.productLayout.addWidget(tmpWidget, idx//self.__rowNum, idx%self.__rowNum)
    
        self.orderTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.orderTable.verticalHeader().setVisible(False)
        self.orderTable.setColumnWidth(0, 140)
        self.orderTable.setColumnWidth(1, 40)
        self.orderTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
    def __del__(self):
        pass

    def __initSlot(self):
        self.backButton.clicked.connect(self.onBackButtonClicked)
        self.orderButton.clicked.connect(self.onOrderButtonClicked)
        self.clearButton.clicked.connect(self.onClearButtonClicked)

    def __clearWidget(self):
        self.orderTable.clearContents()
        self.orderTable.setRowCount(0)
        self.totalEdit.clear()
        
    @pyqtSlot()
    def onBackButtonClicked(self):
        self.backButtonSignal.emit()

    @pyqtSlot()
    def onOrderButtonClicked(self):
        currentRowCount = self.orderTable.rowCount()
        if currentRowCount > 0:
            if self.__orderStatus:
                # recommend
                orderPopup = OrderDialog(self)
                orderPopup.acceptSignal.connect(self.onAcceptSlot)
                orderPopup.exec()
                self.__orderStatus = False
            else:
                # save revenue
                self.__orderStatus = True
                currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
                if currentDate != self.__date:
                    self.__date = currentDate
                    self.__orderNumber = 0
                self.__orderNumber += 1

                # load
                loadRevenue = dict()
                fileName = 'revenue_list/{}.json'.format(self.__date)
                if os.path.isfile(fileName):
                    loadRevenue = json.load(open(fileName, 'r', encoding='utf-8'))
                    self.__orderNumber = len(loadRevenue) + 1

                # save
                orderList = list()
                loadRevenue[self.__orderNumber] = dict()

                loadRevenue[self.__orderNumber]['total'] = int(self.totalEdit.text().replace(',', ''))
                for idx in range(currentRowCount):
                    orderList.append({'menu': self.orderTable.item(idx, 0).text(), 'pcs':int(self.orderTable.item(idx, 1).text()), 'price':int(self.orderTable.item(idx, 2).text().replace(',', ''))})
                loadRevenue[self.__orderNumber]['order_list'] = orderList

                with open(fileName, 'w', encoding='utf-8') as fp:
                    json.dump(loadRevenue, fp, sort_keys=False, indent=4, separators=(',', ':'))

                self.__clearWidget()
                msg = QMessageBox()
                msg.setWindowTitle('Complete')
                msg.setText('결제가 완료 되었습니다.')
                msg.exec()
        

    @pyqtSlot()
    def onClearButtonClicked(self):
        self.__orderStatus = True
        self.__clearWidget()

    @pyqtSlot(int)
    def onProductClickedSlot(self, productNum):
        self.__orderStatus = True
        name, _, price = self.productList[productNum].getInformation()
        if price != None:
            itemList = self.orderTable.findItems(name, Qt.MatchFlag.MatchFixedString | Qt.MatchFlag.MatchCaseSensitive)
            if len(itemList) > 0:
                rowCount = itemList[0].row()
                pcs = int(self.orderTable.item(rowCount, 1).text()) + 1
                self.orderTable.setItem(rowCount, 1, QTableWidgetItem(str(pcs)))
            else:
                rowCount = self.orderTable.rowCount()
                self.orderTable.insertRow(rowCount)
                self.orderTable.setItem(rowCount, 0, QTableWidgetItem(name))
                self.orderTable.setItem(rowCount, 1, QTableWidgetItem(str(1)))
                self.orderTable.setItem(rowCount, 2, QTableWidgetItem(format(price, ',')))
            currentRowCount = self.orderTable.rowCount()
            totalPrice = 0
            for idx in range(currentRowCount):
                totalPrice += int(self.orderTable.item(idx, 1).text()) * int(self.orderTable.item(idx, 2).text().replace(',', ''))
            self.totalEdit.setText(format(totalPrice, ','))
            
    @pyqtSlot(dict)
    def onAcceptSlot(self, addedMenu):
        self.__addedMenuDict = addedMenu
        dictCount = len(self.__addedMenuDict)
        if dictCount > 0:
            currentRowCount = self.orderTable.rowCount()
            totalPrice = int(self.totalEdit.text().replace(',', ''))
            for idx in range(currentRowCount):
                name = self.orderTable.item(idx, 0).text()
                if name in self.__addedMenuDict:
                    pcs = int(self.orderTable.item(idx, 1).text()) + self.__addedMenuDict[name]['pcs']
                    self.orderTable.setItem(idx, 1, QTableWidgetItem(str(pcs)))
                    totalPrice += self.__addedMenuDict[name]['pcs'] * self.__addedMenuDict[name]['price']
                    del self.__addedMenuDict[name]

            for key, value in self.__addedMenuDict.items():
                self.orderTable.insertRow(currentRowCount)
                self.orderTable.setItem(currentRowCount, 0, QTableWidgetItem(key))
                self.orderTable.setItem(currentRowCount, 1, QTableWidgetItem(str(value['pcs'])))
                self.orderTable.setItem(currentRowCount, 2, QTableWidgetItem(format(value['price'], ',')))
                currentRowCount += 1
                totalPrice += value['pcs'] * value['price']

            self.totalEdit.setText(format(totalPrice, ','))
            
                
import sys
if __name__ == "__main__":
	app = QApplication([])
	window = UserWidget(12, 4)
	window.show()
	sys.exit(app.exec_())