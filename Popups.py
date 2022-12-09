# Pyqt UI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

newpPop_ui = uic.loadUiType("./UI/AddNewPat.ui")[0]
class NewpPop(QMainWindow, newpPop_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


simpleinputUi = uic.loadUiType("./UI/SimpleInput.ui")[0]
class SimpleinputPop(QMainWindow, simpleinputUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


EditUi = uic.loadUiType("./UI/EditPopup.ui")[0]
class ChartinputPop(QMainWindow, EditUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)