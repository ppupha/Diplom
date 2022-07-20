import sys
from os import environ
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QDialog
from numpy import random as nr
from itertools import *
import datetime
from PetriNet import *



def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"
    
 

 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        self.neeđUpateLight = False
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi("sh.ui", self)

        self.light1 = SimpleLight('Light1')
        self.light2 = SimpleLight('Light2')

        self.lights = [light1, light2]

        self.light1.onLightTrans.setLabel('l1')
        self.light1.offLightTrans.setLabel('l2')

        self.light2.onLightTrans.setLabel('notl1')
        self.light2.offLightTrans.setLabel('notl2')

        self.btn_light1.setStyleSheet("background-color : lightgrey")
        self.btn_light2.setStyleSheet("background-color : lightgrey")
        self.btn_meetingMode.setStyleSheet("background-color : lightgrey")

        self.btn_light1.clicked.connect(self.btn_light1Clicked)
        self.btn_light2.clicked.connect(self.light2Clicked)
        self.incLight1.clicked.connect(self.incLight1Clicked)
        self.decLight1.clicked.connect(self.decLight1Clicked)
        self.btn_meetingMode.clicked.connect(self.btn_meetingModeClicked)

        self.globalTime = datetime.datetime.now()
        self.timeSpeed = 1
        
        #self.calcTimer()
        
    def calcTimer(self,):
        self.timer = QTimer()
        self.deltaT = 100
        self.timer.timeout.connect(self.auto_update)
        self.timer.start(self.deltaT)

    def initSync(self):
        self.light1.onLightTrans.setLabel('l1')
        self.light1.offLightTrans.setLabel('l2')

        self.light2.onLightTrans.setLabel('notl1')
        self.light2.offLightTrans.setLabel('notl2')


    def showTime(self):
        print(self.globalTime.strftime('%c'))


    def incLight1Clicked(self):
        self.light1.PN.showStatus()
        self.light1.incBright(count = 5)
        self.neeđUpateLight = True
        self.light1.PN.showStatus()

    def decLight1Clicked(self):
        self.light1.decBright(count = 5)
        self.neeđUpateLight = True

    def auto_update(self, ):
        #for i in range(self.timeSpeed):
        for i in range(1):
            self.globalTime += datetime.timedelta(seconds=3600)
            #self.showTime()
            print()
            if (self.globalTime.hour == 17):
                #self.light1.turnOn()
                #self.light2.turnOn()
                #self.neeđUpateLight = True
                print('Turn on Lights')
            if (self.globalTime.hour == 2):
                #self.light1.turnOff()
                #self.light2.turnOn()
                #self.neeđUpateLight = True
                print("turn off light")
            if (self.neeđUpateLight):
                print("Updating")
                self.update_light()
        
    def btn_light1Clicked(self,):
        self.neeđUpateLight = True
        self.light1.PN.showStatus()
        if self.btn_light1.isChecked():
            self.light1.turnOn()
        else:
            self.light1.turnOff()
        self.light1.PN.showStatus()
            
    def light2Clicked(self,):
        self.neeđUpateLight = True
        if self.btn_light2.isChecked():
            self.light2.turnOn()
        else:
            self.light2.turnOff()

    def btn_meetingModeClicked(self):
        if (self.btn_meetingMode.isChecked()):
            print("Meeting Mode Start")
        else:
            print("Meting Mode End")

    def update_light(self):
        self.light1.PN.showStatus()
        self.light2.PN.showStatus()
        if self.light1.isOn():
            self.btn_light1.setStyleSheet("background-color : lightblue")
        else:
            self.btn_light1.setStyleSheet("background-color : lightgrey")
        self.labelLight1.setText(self.light1.showStatus())
        if self.light2.isOn():
            self.btn_light2.setStyleSheet("background-color : lightblue")
        else:
            self.btn_light2.setStyleSheet("background-color : lightgrey")
        
        self.neeđUpateLight = False
        


def qt_app():
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
    