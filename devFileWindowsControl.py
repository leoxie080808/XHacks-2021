import face_recognition
import cv2
import sys
import pickle
import os
from time import sleep
import imagezmq
import keyboard
from plyer import notification


import pyautogui as gui
import time

from pynput.keyboard import Controller, Key


from time import sleep
import ctypes

def altTab():
    gui.keyDown('alt')
    time.sleep(.23)
    gui.press('tab')
    time.sleep(.23)
    gui.keyUp('alt')


def scrollingDown():
    print("scrolling down")
    gui.scroll(-50)

def scrollingUp():
    print("scrolling up")
    gui.scroll(50)

def printScreen():
    gui.press("printscreen")
    notification.notify(title = "screenshot created", message = "screenshot taken!", timeout = 10)




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

while True:
    if keyboard.is_pressed('q'):
        altTab()
    elif keyboard.is_pressed('w'):
        printScreen()


# Press the green button in the gutter to run the script.
if name == 'main':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
