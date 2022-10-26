from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from SelectedWidget import SelectedWidget
from UserWidget import UserWidget
from AdminWidget import AdminWidget

import time

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('MainWidget.ui', self)        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.__productNum = 12
        self.__rowNum = 4
        
        self.__selectedWidget = SelectedWidget()
        self.__activateWidget = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimerTimemout)
        self.timer.start(3000)

        self.__initSlot()
        self.widgetShow()


    def __initSlot(self) :
        self.__selectedWidget.UserViewButtonSignal.connect(self.onUserViewButtonSlot)
        self.__selectedWidget.AdminViewButtonSignal.connect(self.onAdminViewButtonSlot)

    def __createActivateWidget(self, widget=None):
        if widget != None:
            if self.__activateWidget == None:
                self.__activateWidget = widget(self.__productNum, self.__rowNum)
                self.__activateWidget.backButtonSignal.connect(self.onBackButtonSlot)
                self.stackedWidget.insertWidget(1, self.__activateWidget)

    def __deleteActivateWidget(self):
        if self.__activateWidget != None:
            self.stackedWidget.removeWidget(self.__activateWidget)
            self.__activateWidget.deleteLater()
            self.__activateWidget = None
            
    def widgetShow(self):
        self.stackedWidget.setCurrentIndex(1)
        self.show()

    @pyqtSlot()
    def onUserViewButtonSlot(self):
        self.__createActivateWidget(UserWidget)
        self.stackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def onAdminViewButtonSlot(self):
        self.__createActivateWidget(AdminWidget)
        self.stackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def onBackButtonSlot(self):
        self.__deleteActivateWidget()
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def onTimerTimemout(self):
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.insertWidget(0, self.__selectedWidget)
        self.stackedWidget.setCurrentIndex(0)
        self.timer.stop()
