import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox
from PyQt5.QtCore import QSize, QRect

firstValue = 0



class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 140))
        self.setWindowTitle("Combobox example")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Create combobox and add items.
        self.comboBox = QComboBox(centralWidget)
        self.comboBox.setGeometry(QRect(40, 40, 491, 31))
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem('printscreen', 1)
        self.comboBox.addItem("alt-tab", 2)
        self.comboBox.addItem("scrolling up", 3)
        self.comboBox.addItem("scrolling down", 4)

        self.comboBox.activated.connect(self.handleActivated)

    def handleActivated(self, index):
        print(self.comboBox.itemText(index))
        print(self.comboBox.itemData(index))
        firstValue = self.comboBox.itemData((index))
        print("the value of the first window is:", firstValue)

        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )
