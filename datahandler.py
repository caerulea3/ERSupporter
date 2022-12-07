import pandas as pd

class Patient():
    def __init__(self, n:str, s:str, a:int, p:str):
        self.name = n
        self.sex = s
        self.age = a
        self.place = p

