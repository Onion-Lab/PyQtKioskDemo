from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

import os

class SetProductDialog(QDialog):
    onSetProductSaveSignal = pyqtSignal(str, str, int)
    def __init__(self,parent):
        QDialog.__init__(self)
        uic.loadUi('SetProductWidget.ui', self)
        
        self.parent = parent
        self.__name = ''
        self.__imagePath = ''
        self.__price = None
        
        self.__initSlot()

    def __initSlot(self):
        self.okayButton.clicked.connect(self.onAcceptButtonClicked)
        self.findButton.clicked.connect(self.onFindButtonClicked)
        self.onSetProductSaveSignal.connect(self.parent.onSetProductSaveSlot)
        
    def getInformation(self):
        return self.__name, self.__imagePath, self.__price

    @pyqtSlot()
    def onAcceptButtonClicked(self):
        self.__name, self.__imagePath, self.__price = self.nameEdit.text(), self.imagePathEdit.text(), self.priceSpinBox.value()
        self.onSetProductSaveSignal.emit(self.__name, self.__imagePath, self.__price)
        self.close()

    @pyqtSlot()
    def onFindButtonClicked(self):
        filePathTuple = QFileDialog.getOpenFileName(self, "Open", ".", "Select image file (*.jpg *.png *.jpeg *.bmp)")
        if filePathTuple[0] != '':
            self.imagePathEdit.setText(os.path.relpath(filePathTuple[0]))

import sys
if __name__ == "__main__":
	app = QApplication([])
	window = SetProductDialog()
	window.show()
	sys.exit(app.exec_())