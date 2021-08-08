import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox
from PyQt5.QtCore import QSize, QRect

#just for testing the value callback
import keyboard
from plyer import notification
import pyautogui as gui
import time

firstValue = 0
secondValue = 0
doubleState = 0
tripleState = 0


def altTab():
    gui.keyDown('alt')
    time.sleep(.23)
    gui.press('tab')
    time.sleep(.23)
    gui.keyUp('alt')


def scrollingDown():
    print("scrolling down")
    gui.scroll(2)

def printScreen():
    gui.press("printscreen")
    notification.notify(title = "screenshot created", message = "screenshot taken!", timeout = 10)

class firstWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 140))
        self.setWindowTitle("double blink setting")

        centralWidget = QWidget(self)
        lowerWideget = QWidget(self)

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

        doubleState = firstValue
        print("the value of the first window is:", doubleState)

        # if firstValue == 1:
        #     return 1
        # elif firstValue == 2:
        #     return 2
        # else:
        #     pass

class secondWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 140))
        self.setWindowTitle("triple blink setting")

        centralWidget = QWidget(self)
        lowerWideget = QWidget(self)

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
        secondValue = self.comboBox.itemData((index))

        tripleState = secondValue
        print("the value of the second window is:", tripleState)



app = QtWidgets.QApplication(sys.argv)
mainWin = firstWindow()
mainWin.show()
anotherWin = secondWindow()
anotherWin.show()

print("the double value is ", doubleState)
print("the triple value is ", tripleState)

sys.exit( app.exec_() )

