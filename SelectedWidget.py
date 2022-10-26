from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *


class SelectedWidget(QWidget):
    UserViewButtonSignal = pyqtSignal()
    AdminViewButtonSignal = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('SelectedWidget.ui', self)

        self.UserViewButton.clicked.connect(self.UserViewSlot)
        self.AdminViewButton.clicked.connect(self.AdminViewSlot)


    @pyqtSlot()
    def UserViewSlot(self):
        self.UserViewButtonSignal.emit()
        

    @pyqtSlot()
    def AdminViewSlot(self):
        self.AdminViewButtonSignal.emit()

