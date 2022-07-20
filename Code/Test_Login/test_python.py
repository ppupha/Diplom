class Base:
    def __init__(self, name):
        self.name = name

class A:
    def __init__(self, name):
        self.value = Base(name)
    def test(self):
        print(self.value.name)

def func(A):
    A.name = '123'


import datetime
import matplotlib.pyplot as plt

day = datetime.datetime.strptime('21/12/2021 12:00:00', '%d/%m/%Y %H:%M:%S')
date = day.date() +datetime.timedelta(days=1)
time = datetime.datetime.strptime('13:00:00', '%H:%M:%S').time()
res = datetime.datetime.combine(date, time)
print(res)
print(day)