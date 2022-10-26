from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

class ProductButton(QPushButton):
    productClickedSignal = pyqtSignal(int)

    def __init__(self, productNum, name='', imagePath='', price=None):
        super(QPushButton, self).__init__()

        self.__productNum = productNum

        self.setFixedSize(128, 143)
        self.setContentsMargins(0, 0, 0, 0)

        self.productButton = QVBoxLayout(self)
        self.productButton.setSpacing(1)

        # set name Label
        self.nameLabel = QLabel(self)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(QFont('Consolas', 10))
        self.nameLabel.setStyleSheet("background-color : white")
        self.nameLabel.setMaximumHeight(20)
        
        # set image label
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setFont(QFont('Consolas', 10))
        self.imageLabel.setStyleSheet("background-color : white")
        self.imageLabel.setFixedHeight(68)

        # set price label
        self.priceLabel = QLabel(self)
        self.priceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priceLabel.setFont(QFont('Consolas', 10))
        self.priceLabel.setStyleSheet("background-color : white")
        self.priceLabel.setMaximumHeight(20)

        self.productButton.addWidget(self.nameLabel)
        self.productButton.addWidget(self.imageLabel)
        self.productButton.addWidget(self.priceLabel)
        
        self.setInformation(name, imagePath, price)
        
        self.__initSlot()

    def __initSlot(self):
        self.clicked.connect(self.onClickedSlot)

    def __setName(self):
        self.nameLabel.setText(self.__name)

    def __setImage(self):
        try:
            if self.__imagePath == '':
                self.imageLabel.clear()
                self.imageLabel.setText('No Image')
            else:
                pixmap = QPixmap(self.__imagePath)
                self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.AspectRatioMode.IgnoreAspectRatio))
        except:
            self.imageLabel.clear()
            self.imageLabel.setText('No Image')
    
    def __setPrice(self):
        if  self.__price == None:
            self.priceLabel.setText('-')
        else:
            self.priceLabel.setText(format(self.__price, ',') + ' ￦')

    def setInformation(self, name='', imagePath='', price=None):
        self.__name = name
        self.__imagePath = imagePath
        self.__price = price
        self.__setName()
        self.__setImage()
        self.__setPrice()

    def getInformation(self):
        return self.__name, self.__imagePath, self.__price

    @pyqtSlot()
    def onClickedSlot(self):
        self.productClickedSignal.emit(self.__productNum)

    