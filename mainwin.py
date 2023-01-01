import sys
import pickle as pkl

# Pyqt UI
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QColor

from backend import refine_patdata, now_timestamp, strip_multyline, text_linebreak
from Popups import NewpPop, SimpleinputPop, ChartinputPop
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
        self.side_patlist = []

        self.todolist = []
        self.dclist = []

        self.AddPatB.clicked.connect(self.Addpatient)
        self.DashBoardTable.doubleClicked.connect(self.activate_patient)
        self.SideDashBoardTable.doubleClicked.connect(self.activate_patient_side)
        self.DCDashBoardTable.doubleClicked.connect(self.reactivate_patient)

        self.spinBox.valueChanged.connect(self.linebreak_mdf)
        self.width = 25
        self.LoadB.clicked.connect(self.load_data)
        self.SaveB.clicked.connect(self.save_data)
        self.AutoSaveB.clicked.connect(self.autosave)

        self.CCB.clicked.connect(self.changecc)
        self.DxB.clicked.connect(self.changedx)
        self.PastMedicalB.clicked.connect(self.add_pmhx)
        self.ChartB.clicked.connect(self.addchart)
        self.TodoB.clicked.connect(self.addtodo)
        self.upB.clicked.connect(self.up)
        self.downB.clicked.connect(self.down)
        self.DischargeB.clicked.connect(self.discharge)
        self.ReadingB.clicked.connect(self.ask_reading)
        self.PlaceB.clicked.connect(self.set_place)
        
        self.Pat_Todo.itemDoubleClicked.connect(self.todo_clear)
        self.ChartView.itemDoubleClicked.connect(self.chart_clear)
        
        self.cnt = 0

    def refresh(self):
        self.refresh_main()
        self.refresh_pat()
        self.autosave()

    def refresh_main(self):
        self.TodoTable.clear()
        self.make_todo()
        for i in range(len(self.todolist)):
            this = QListWidgetItem(self.todolist[i][0])
            this.setBackground(self.todolist[i][1])
            self.TodoTable.addItem(this)

        self._update_table(self.DashBoardTable, self.patlist, main = True)
        self._update_table(self.SideDashBoardTable, self.side_patlist)
        self._update_table(self.DCDashBoardTable, self.dclist)

    def refresh_pat(self):
        if self.ActivePatient is None:
            return

        self.PData.setPlainText("{} {} ({}/{})\nCC : {}\nDx. : {}\nMemo : {}".format(
            self.ActivePatient.pnum, self.ActivePatient.name, self.ActivePatient.sex, self.ActivePatient.age,
            self.ActivePatient.datas["CC"], self.ActivePatient.datas["Dx"], self.ActivePatient.getMemo()
        ))

        self.Pat_Todo.clear()
        this_todo = self.ActivePatient.datas["Todos"]
        for i in range(len(this_todo)):
            this = QListWidgetItem(this_todo[i][0])
            this.setBackground(this_todo[i][1])
            self.Pat_Todo.addItem(this)

        self.ChartView.clear()
        for c in self.ActivePatient.get_chart():
            # self.ChartView.addItem(QListWidgetItem(str(c)))
            self.ChartView.addItem(QListWidgetItem(text_linebreak(str(c), width = self.width)))


    def make_todo(self):
        self.todolist = []
        for pat in self.patlist:
            self.todolist += pat.get_todos()

    def _update_table(self, board, table, main = False):
        board.setRowCount(0)
        board.setRowCount(len(table))
        board.setColumnCount(9)

        for i in range(len(table)):
            pat = table[i]
            board.setItem(i, 0,QTableWidgetItem(str(pat.name)))
            board.setItem(i, 1,QTableWidgetItem(str(pat.pnum)))
            board.setItem(i, 2,QTableWidgetItem(str("{}/{}".format(pat.sex, pat.age))))
            board.setItem(i, 3,QTableWidgetItem(str(pat.place)))
            board.setItem(i, 4,QTableWidgetItem(str(pat.datas['CC']))) 
            board.setItem(i, 5,QTableWidgetItem(str(pat.datas['Dx']))) 
            if main:
                color = (GREEN if pat.datas["Init"]=="I" else LIGHTGREEN) if pat.isInitDone() else RED
                wdg = QTableWidgetItem()
                wdg.setBackground(color)
                board.setItem(i, 6, wdg) #초진

                board.setItem(i, 7,QTableWidgetItem(str())) #lab
                board.setItem(i, 8,QTableWidgetItem(str())) #영상

        board.resizeRowsToContents()
        board.resizeColumnsToContents()

    def autosave(self):
        self.cnt +=1
        print(self.cnt)
        if self.cnt == 20:
            self.cnt = 0
            with open("./datas/temp.pkl", 'wb') as f:
                pkl.dump([self.patlist, self.side_patlist, self.todolist, self.dclist], f)

    def save_data(self):
        path = QFileDialog.getSaveFileName(self, 'Open file', './datas/')
        print(path)
        with open(path[0], 'wb') as f:
            pkl.dump([self.patlist, self.side_patlist, self.todolist, self.dclist], f)


    def load_data(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', './datas/')
        print(path)
        try:
            with open(path[0], 'rb') as f:
                all = pkl.load(f)
        except FileNotFoundError:
            return
        if len(all) == 1:
            print("LOAD : len == 1")
            self.patlist = all
        if len(all) == 3:
            print("LOAD : len == 3")
            print(all[0], all[1], all[2])
            self.patlist, self.side_patlist, self.todolist = all
        if len(all) == 4:
            print("LOAD : len == 4")
            print(all[0], all[1], all[2], all[3])
            self.patlist, self.side_patlist, self.todolist, self.dclist = all
        self.refresh()


    def Addpatient(self):
        self.pop = NewpPop()
        self.pop.show()
        self.pop.pushButton.clicked.connect(self._addnewpat)

    def _addnewpat_brm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        try:
            pnum, pname, sex, age = refine_patdata(raw.replace("`", ""))
        except ValueError:
            self.pop.close()
            self.refresh()
            return
        if raw.startswith("`"):
            raw = raw.replace("`", "")
            self.side_patlist.insert(0, Patient(pname, pnum, sex, age))
        else:
            self.patlist.insert(0, Patient(pname, pnum, sex, age))
        self.pop.close()
        self.refresh()
        
    def _addnewpat(self):
        n, num, s, a = self.pop.Name.toPlainText(), self.pop.Pnum.toPlainText(), self.pop.Sex.currentText(), self.pop.Age.toPlainText()
        n, num, a = n.strip(), num.strip(), a.strip()
        if "" in [n, num, s, a]:
            self.pop.close()
            self.refresh()
            return
        if n.startswith("`"):
            raw = raw.replace("`", "")
            self.side_patlist.insert(0, Patient(n, num, s, a))
        else:
            self.patlist.insert(0, Patient(n, num, s, a))
        self.pop.close()
        self.refresh()
        return
        

    def activate_patient(self):
        r, c = self.DashBoardTable.currentIndex().row(), self.DashBoardTable.currentIndex().column()
        self.ActivePatient = self.patlist[int(r)]
        self.refresh()

    def activate_patient_side(self):
        r, c = self.SideDashBoardTable.currentIndex().row(), self.SideDashBoardTable.currentIndex().column()
        self.ActivePatient = self.side_patlist[int(r)]
        self.refresh()

    def reactivate_patient(self):
        r, c = self.DCDashBoardTable.currentIndex().row(), self.DCDashBoardTable.currentIndex().column()
        this = self.dclist[int(r)]
        reply = QMessageBox.question(
            self,
            "Message",
            "{}\nReactivate?".format(this),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self.patlist.insert(0, this)

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
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.SaveB.clicked.connect(self.add_todo_confirm)
            self.pop.show()

    def add_todo_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        self.ActivePatient.add_todo([raw, ORANGE])
        self.pop.close()
        self.refresh()

    def add_pmhx(self):
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.SaveB.clicked.connect(self.add_pmhx_confirm)
            self.pop.show()

    def add_pmhx_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        raw = strip_multyline(raw)
        self.ActivePatient.add_chart(raw)
        self.pop.close()
        self.refresh()

    def addchart(self):
        if self.ActivePatient is not None:
            self.pop = ChartinputPop()
            if self.ActivePatient.isInitDone():
                self.pop.InitB.setText("초진완료")
            else:
                self.init_state = "I"
                self.pop.InitB.clicked.connect(self.toggle_init)
            self.pop.SaveB.clicked.connect(self.addchart_confirm)
            self.pop.show()
    
    def toggle_init(self):
        if self.init_state == "I":
            self.init_state = "R"
            self.pop.InitB.setText("초진R")
        elif self.init_state == "R":
            self.init_state = "I"
            self.pop.InitB.setText("초진")

    def addchart_confirm(self):
        raw = self.pop.textEdit.toPlainText()
        if self.ActivePatient.isInitDone():
            self.ActivePatient.add_chart(raw)
        else:
            self.ActivePatient.datas["Init"] = self.init_state
            # raw = raw.split("\n")
            # start_idx = 0
            # end_idx = len(raw)
            # for i in range(len(raw)):
            #     if "CC" in raw[i]:
            #         start_idx = i
            #     if ("ROS" in raw[i]) or ("PE" in raw[i]) or ("P/E" in raw[i]) or ("Neurologic Exam" in raw[i]):
            #         end_idx = i
            # if start_idx != 0:
            #     self.ActivePatient.add_chart("\n".join(raw[:start_idx])) 
            # self.ActivePatient.add_chart("\n".join(raw[start_idx:end_idx]))
            # if len(raw[end_idx:]) != 0:
            #     self.ActivePatient.add_chart("\n".join(raw[end_idx:]))
            self.ActivePatient.add_chart(raw) 
        self.pop.close()
        self.refresh()

    def todo_clear(self):
        r= self.Pat_Todo.currentRow()
        this = self.ActivePatient.datas["Todos"][r]

        if this[1] == ORANGE:
            reply = QMessageBox.question(
                self,
                "Message",
                "{}\nDone?".format(this[0]),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )

            if reply == QMessageBox.Yes:
                self.ActivePatient.datas["Todos"][r][1] = LIGHTGREEN

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
                self.ActivePatient.datas["Todos"].pop(r)

            self.refresh()
                
    def chart_clear(self):
        r= self.ChartView.currentRow()
        this = self.ActivePatient.get_chart()[r]

        reply = QMessageBox.question(
            self,
            "Message",
            "{}\nDelete?".format(this),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self.ActivePatient.datas["Charts"].pop(r)

        self.refresh()

    def up(self):
        if self.ActivePatient is None:
            return
        if self.ActivePatient not in self.patlist:
            return

        idx = self.patlist.index(self.ActivePatient)
        if idx != 0:
            self.patlist[idx-1], self.patlist[idx] = self.patlist[idx], self.patlist[idx-1] 
            self.refresh()
                
    def down(self):
        if self.ActivePatient is None:
            return
        if self.ActivePatient not in self.patlist:
            return

        idx = self.patlist.index(self.ActivePatient)
        if idx != len(self.patlist)-1:
            self.patlist[idx+1], self.patlist[idx] = self.patlist[idx], self.patlist[idx+1] 
        self.refresh()

    def consult_img(self):
        return

    def discharge(self):
        reply = QMessageBox.question(
            self,
            "Message",
            "{}\nDelete?".format(self.ActivePatient),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self.patlist.remove(self.ActivePatient)
            self.dclist.append(self.ActivePatient)

        self.refresh()

    def linebreak_mdf(self):
        self.width = self.spinBox.value()
        self.refresh()

    def ask_reading(self):
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.show()
            self.pop.plainTextEdit.setPlainText("{}\
\n\n검사명: \n\nPMHx>\n\n의뢰내용 > \
\n안녕하십니까 선생님, \n\n상환 {} 으로 내원하신 분입니다. \
\n이에 r/o {} 소견 하 상기검사 진행하여 판독의뢰 드리오니 바쁘신 와중에 부디 고진선처 부탁드립니다. 감사합니다.\
\nEM DI 이기언 올림 ".format(
                    self.ActivePatient, self.ActivePatient.datas['CC'], self.ActivePatient.datas['Dx']
            ))
        """
        "CT Abdomen+Pelvis Dynamic (contrast)
        CT Abdomen+Pelvis Pre-Post (contrast)
        CT Abdomen+Pelvis Post (contrast)
        CT Abdomen+Pelvis (noncontrast)
        CT Acute Abdomen(contrast)
        Neck CT Dynamic(contrast)
        Abdominal Aorta CT Angio+3D (contrast)
        Pulmonary artery CT Angio+3D(contrast)
        CT Acute Abdomen (contrast)
        Chest CT (contrast)
        Chest CT (noncontrast)
        Lower Extremities CT Angio+3D(contrast)-Artery
        Brain CT Angio + 3D (contrast)
        Brain CT(noncontrast)
        Neck CT General (contrast)
        CT urolithiasis_initial
        Face Skull bone CT
        Cervical Spine CT (noncontrast)
        Foot+3D CT(noncontrast)"
        "MR Brain + Brain MRA + CE-MRA + Diffusion (contrast)
        MR Brain + MRA Acute Stroke (contrast)
        MR Brain + MRA Acute Stroke (noncontrast)
        MR Brain - Hyperacute Stroke [contrast]
        MR Whole Foot(contrast)
        Meta w/u brain MRI(contrast)"
        """

    def set_place(self):
        if self.ActivePatient is not None:
            self.pop = SimpleinputPop()
            self.pop.show()
            self.pop.plainTextEdit.setPlainText("{}".format(self.ActivePatient.place))
            self.pop.ResetB.clicked.connect(lambda:self.pop.plainTextEdit.setPlainText("Dx. : {}".format(self.ActivePatient.datas['Dx'])))
            self.pop.SaveB.clicked.connect(self.setplace_confirm)

    def setplace_confirm(self):
        raw = self.pop.plainTextEdit.toPlainText()
        self.ActivePatient.place = raw
        self.pop.close()
        self.refresh()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
