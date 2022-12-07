import sys
import datetime

# Pyqt UI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QFont


# UI파일 연결
form_class = uic.loadUiType("./UI/DrMainWin.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
# class WindowClass(DirtyMainwin, form_class):
class WindowClass(QMainWindow, form_class):
    def __init__(self, msg):
        super().__init__()
        self.setupUi(self)

        self.AddPatB.clicked.connect(self.Addpatient)


    def Addpatient(self):
        

