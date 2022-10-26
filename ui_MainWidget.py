# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 480)
        Form.setMinimumSize(QSize(800, 480))
        Form.setMaximumSize(QSize(800, 480))
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 800, 480))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.LogoStackWidget = QWidget()
        self.LogoStackWidget.setObjectName(u"LogoStackWidget")
        self.label = QLabel(self.LogoStackWidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 800, 480))
        self.label.setPixmap(QPixmap(u"resources/main_image.jpg"))
        self.stackedWidget.addWidget(self.LogoStackWidget)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"kiosk", None))
        self.label.setText("")
    # retranslateUi

