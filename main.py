import sys
from MainWidget import MainWidget
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWidget()
    #w.showFullScreen()
    sys.exit(app.exec())