import sys
import pickle as pkl

# Pyqt UI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QFont, QColor

from backend import refine_patdata, now_timestamp
from Popups import NewpPop, SimpleinputPop
from datahandler import Patient

RED =  QColor(204,51,0)
ORANGE = QColor(255,204,0)
LIGHTGREEN = QColor(153,204,51)
GREEN = QColor(51,153,0)


# UI파일 연결
form_class = uic.loadUiType("./UI/Mainwin.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
# class WindowClass(DirtyMainwin, form_class):
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.patlist = []
        self.ActivePatient = None

        self.todolist = []
        self.TodoTable.itemDoubleClicked.connect(self.todo_clear)

        self.AddPatB.clicked.connect(self.Addpatient)
        self.DashBoardTable.doubleClicked.connect(self.activate_patient)

        self.LoadB.clicked.connect(self.load_data)
        self.SaveB.clicked.connect(self.save_data)
        self.CCB.clicked.connect(self.changecc)
        self.DxB.clicked.connect(self.changedx)
        self.AddTodoB.clicked.connect(self.addtodo)
        
        self.autosave()

    def refresh(self):
        if self.ActivePatient is not None:
            self.PData.setPlainText("{} {} ({}/{})\nCC : {}\nDx. : {}".format(
                self.ActivePatient.pnum, self.ActivePatient.name, self.ActivePatient.sex, self.ActivePatient.age,
                self.ActivePatient.datas["CC"], self.ActivePatient.datas["Dx"]
            ))

        self.TodoTable.clear()
        for i in range(len(self.todolist)):
            this = QListWidgetItem(self.todolist[i][0])
            this.setBackground(self.todolist[i][1])
            self.TodoTable.addItem(this)
        
        self.DashBoardTable.setRowCount(0)
        self.DashBoardTable.setRowCount(len(self.patlist))
        self.DashBoardTable.setColumnCount(9)

        for i in range(len(self.patlist)):
            pat = self.patlist[i]
            self.DashBoardTable.setItem(i, 0,QTableWidgetItem(str(pat.name)))
            self.DashBoardTable.setItem(i, 1,QTableWidgetItem(str(pat.pnum)))
            self.DashBoardTable.setItem(i, 2,QTableWidgetItem(str("{}/{}".format(pat.sex, pat.age))))
            self.DashBoardTable.setItem(i, 3,QTableWidgetItem(str(pat.place)))
            self.DashBoardTable.setItem(i, 4,QTableWidgetItem(str(pat.datas['CC']))) 
            self.DashBoardTable.setItem(i, 5,QTableWidgetItem(str(pat.datas['Dx']))) 
            self.DashBoardTable.setItem(i, 6,QTableWidgetItem(str())) #초진
            self.DashBoardTable.setItem(i, 7,QTableWidgetItem(str())) #lab
            self.DashBoardTable.setItem(i, 8,QTableWidgetItem(str())) #영상

        self.DashBoardTable.resizeRowsToContents()
        self.DashBoardTable.resizeColumnsToContents()

    def autosave(self):
        with open("./datas/"+now_timestamp(dividor="_")+".pkl", 'wb') as f:
            pkl.dump(self.patlist, f)

    def save_data(self):
        self.pop = SimpleinputPop()
        self.pop.SaveB.clicked.connect(self.save_confirm)
        self.pop.show()

    def save_confirm(self):
        path = self.pop.plainTextEdit.toPlainText()
        with open("./datas/"+path+".pkl", 'wb') as f:
            pkl.dump(self.patlist, f)

    def load_data(self):
        self.pop = SimpleinputPop()
        self.pop.SaveB.clicked.connect(self.load_confirm)
        self.pop.show()

    def load_confirm(self):
        path = self.pop.plainTextEdit.toPlainText()
        with open("./datas/"+path, 'rb') as f:
            self.patlist = pkl.load(f)
        self.pop.close()
        self.refresh()

    def Addpatient(self):
        self.pop = NewpPop()
        self.pop.show()
        self.pop.pushButton.clicked.connect(self._addnewpat)

    def _addnewpat(self):
        raw = self.pop.plainTextEdit.toPlainText()
        pnum, pname, sex, age = refine_patdata(raw)
        self.patlist.append(Patient(pname, pnum, sex, age))
        self.pop.close()
        self.refresh()

    def activate_patient(self):
        r, c = self.DashBoardTable.currentIndex().row(), self.DashBoardTable.currentIndex().column()
        self.ActivePatient = self.patlist[int(r)]
        self.refresh()

    def changecc(self):
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.show()
            self.pop.plainTextEdit.setPlainText("CC : {}".format(self.ActivePatient.datas['CC']))
            self.pop.ResetB.clicked.connect(lambda:self.pop.plainTextEdit.setPlainText("CC : {}".format(self.ActivePatient.datas['CC'])))
            self.pop.SaveB.clicked.connect(self.changecc_confirm)

    def changecc_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        raw = raw.replace("CC : ", "")
        self.ActivePatient.datas["CC"] = raw
        self.pop.close()
        self.refresh()

    def changedx(self):
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.show()
            self.pop.plainTextEdit.setPlainText("Dx. : {}".format(self.ActivePatient.datas['Dx']))
            self.pop.ResetB.clicked.connect(lambda:self.pop.plainTextEdit.setPlainText("Dx. : {}".format(self.ActivePatient.datas['Dx'])))
            self.pop.SaveB.clicked.connect(self.changedx_confirm)

    def changedx_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        raw = raw.replace("Dx. : ", "")
        self.ActivePatient.datas["Dx"] = raw
        self.pop.close()
        self.refresh()

    def addtodo(self):
        self.pop = SimpleinputPop()
        self.pop.SaveB.clicked.connect(self.add_todo_confirm)
        self.pop.show()

    def add_todo_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        self.todolist.append([raw, ORANGE])
        self.pop.close()
        self.refresh()

    def todo_clear(self):
        r= self.TodoTable.currentRow()
        this = self.todolist[r]

        if this[1] == ORANGE:
            reply = QMessageBox.question(
                self,
                "Message",
                "{}\nDone?".format(this[0]),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )

            if reply == QMessageBox.Yes:
                self.todolist[r][1] = LIGHTGREEN

            self.refresh()
            return
            
        if this[1] == LIGHTGREEN:
            reply = QMessageBox.question(
                self,
                "Message",
                "{}\nDelete?".format(this[0]),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )

            if reply == QMessageBox.Yes:
                self.todolist.pop(r)

            self.refresh()
                


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
