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
            "Dx" : "-"
        }

    def __repr__(self) -> str:
        return ("{}({}/{})".format(
            self.name, self.sex, self.age
        ))