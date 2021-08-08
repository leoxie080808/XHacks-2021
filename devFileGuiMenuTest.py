import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox
from PyQt5.QtCore import QSize, QRect

# just for testing the value callback
import keyboard
from plyer import notification
import pyautogui as gui
import time

firstValue = 0
secondValue = 0


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
    notification.notify(title="screenshot created", message="screenshot taken!", timeout=10)


class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 140))
        self.setWindowTitle("Combobox example")

        self.centralwidget = QtWidgets.QWidget()

        self.comboTop = QCombobox(self.centralWidget())
        #self.comboTop = QComboBox(centralWidget)
        self.comboTop.setGeometry(QRect(40, 40, 491, 31))
        self.comboTop.setObjectName(("doubleBlink"))
        self.comboTop.addItem('printscreen', 1)
        self.comboTop.addItem("alt-tab", 2)
        self.comboTop.addItem("scrolling up", 3)
        self.comboTop.addItem("scrolling down", 4)


        #this is part of the working one before, with one drop down
        # centralWidget = QWidget(self)
        # self.setCentralWidget(centralWidget)

        #part below we added ourselves
        # lowerWidget = QWidget(self)
        # self.setCentralWidget(lowerWidget)



        # Create combobox and add items.



        self.comboBox = QComboBox(centralWidget)
        self.comboBox.setGeometry(QRect(40, 40, 491, 31))
        self.comboBox.setObjectName(("doubleBlink"))
        self.comboBox.addItem('printscreen', 1)
        self.comboBox.addItem("alt-tab", 2)
        self.comboBox.addItem("scrolling up", 3)
        self.comboBox.addItem("scrolling down", 4)

        # self.comboBox = QComboBox(lowerWidget)
        # self.comboBox.setGeometry(QRect(40, 100, 491, 31))
        # self.comboBox.setObjectName(("tripleBlink"))
        # self.comboBox.addItem('printscreen', 5)
        # self.comboBox.addItem("alt-tab", 6)
        # self.comboBox.addItem("scrolling up", 7)
        # self.comboBox.addItem("scrolling down", 8)

        self.comboBox.activated.connect(self.handleActivated)


    def handleActivated(self, index):
        print(self.comboBox.itemText(index))
        print(self.comboBox.itemData(index))

        firstValue = self.comboBox.itemData((index))
        secondValue = self.comboBox.itemData((index))
        print("the value of the first window is:", firstValue)

        if firstValue == 1:
            printScreen()
        elif firstValue == 2:
            altTab()
        else:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit(app.exec_())
