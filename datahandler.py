import pandas as pd

class Patient():
    def __init__(self, n:str, pnum : str, s:str, a:int, p:str = "-"):
        self.name = n
        self.sex = s
        self.age = a
        self.place = p
        self.pnum = pnum
        self.datas = {
            "CC" : "-",
            "Dx" : "-",
            "Init" : None,
            "Charts" : [],
            "Todos" : [], 
            "Memos" : []
        }

    def __repr__(self) -> str:
        return ("{} {}({}/{})".format(
            self.pnum, self.name, self.sex, self.age
        ))

    def isInitDone(self) -> bool:
        if self.datas["Init"] is None:
            return False
        else:
            return True

    def get_todos(self) -> list:
        tmp = []
        for t in self.datas["Todos"]:
            tmp.append(("{}/n{}".format(self.__repr__(), t[0]), t[1]))
        return tmp

    def add_chart(self, raw):
        self.datas["Charts"].append(raw)

    def get_chart(self):
        return self.datas["Charts"]

    def add_todo(self, raw):
        self.datas["Todos"].append(raw)

    def getMemo(self):
        return self.datas["Memos"]