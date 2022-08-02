import time
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import threading
from datetime import datetime
from pynput.mouse import Controller


# These may need editing
SCREEN_BLANK_COMMAND = "xset dpms force off"
def notify(title, message="...",t=5): os.system(f"notify-send \"{title}\" \"{message}\"")
DIRECTORY = "./"
######
def screenBlankFunc(): os.system(SCREEN_BLANK_COMMAND)

SEPERATOR = "<SEP>"
NOTIFY_TIME = 5

def screenBlank(timeperiod):
    if MainWindow.breaksOnOff.isChecked():
        for _ in range(timeperiod*4):# so the screen has not time to recover
            os.system(SCREEN_BLANK_COMMAND) # 
            time.sleep(0.25)
        mouse = Controller()
        mouse.move(1, -1)
    else:
        os.system(SCREEN_BLANK_COMMAND)
        time.sleep(0.5)
        mouse = Controller()
        mouse.move(1, -1)


def loadFromFile():
    with open("targets.txt","r") as f:
        lines = f.readlines()
        for l in lines:
            a, b, c = l.split(SEPERATOR)
            TARGETS[0].append(a)
            TARGETS[1].append(b)
            TARGETS[2].append(c)
def saveToFile():
    with open("targets.txt","w") as f:
        for i in range(len(TARGETS[0])):
            f.write(f"{TARGETS[0][i]}{SEPERATOR}{TARGETS[1][i]}{SEPERATOR}{TARGETS[2][i]}\n")
            
        


def notifyTimings():
    while 1:
        now = datetime.now()

        currentTime = now.strftime("%H:%M")
        while currentTime in TARGETS[1]:
            i = TARGETS[1].index(currentTime)
            notify(TARGETS[0][i],TARGETS[2][i])
            TARGETS[0].pop(i); TARGETS[1].pop(i); TARGETS[2].pop(i)
        time.sleep(60)
        
class breaks:
    def __init__(self) -> None:
        with open(".breaks.txt","r") as f:
            self.breakInterval, self.shortBreak, self.longBreak, self.longBreakFrquency = f.readline().split(SEPERATOR)
            self.breakInterval = int(self.breakInterval)
            self.shortBreak = int(self.shortBreak)
            self.longBreak = int(self.longBreak)
            self.longBreakFrquency = int(self.longBreakFrquency)
        self.breaksThread = threading.Thread(target=self.breaks, args=(),daemon=True) # daemon measn it ends with program
        self.breaksThread.start()
    def getTimmings(self): return self.shortBreak, self.longBreak, self.breakInterval, self.longBreakFrquency
    def setTimmings(self,shortBreak,longBreak,breakInterval,longBreakFrquency):
        self.shortBreak = shortBreak
        self.longBreak = longBreak
        self.breakInterval = breakInterval
        self.longBreakFrquency = longBreakFrquency
        with open(".breaks.txt","w") as f:
            f.write(f"{self.breakInterval}{SEPERATOR}{self.shortBreak}{SEPERATOR}{self.longBreak}{SEPERATOR}{self.longBreakFrquency}")
    def reset(self): self.breaksIndexCounter = 0
    def breaks(self):
        self.running=True
        while self.running:
            self.breaksIndexCounter = 0
            while self.breaksIndexCounter<self.longBreakFrquency:
                self.breaksIndexCounter += 1
                time.sleep(self.breakInterval)
                notify("Short Break","Look away")
                time.sleep(NOTIFY_TIME)
                screenBlank(self.shortBreak)
                time.sleep(1)
                notify("Short Break Ended")
                MainWindow.setBreaksProgress(int(round(100*(self.breaksIndexCounter/self.longBreakFrquency))))
            MainWindow.setBreaksProgress(100)
            time.sleep(self.breakInterval)
            notify("Long Break","Leave the computer")
            time.sleep(NOTIFY_TIME)
            screenBlank(self.longBreak)
            time.sleep(1)
            notify("Long Break Ended")
            MainWindow.setBreaksProgress(0)
    def __del__(self):
        self.running=False
        self.breaksThread.join()
    

class MainWindow(QtWidgets.QMainWindow): 
    """Main Qt Window"""
    def __init__(self, *args, **kwargs):
        #Initinalization scripts
        super().__init__(*args, **kwargs)
        uic.loadUi("MainWindow.ui", self)
        self.setUpTargets()
        self.setWindowTitle("Useful App")
        self.setWindowIcon(QIcon('logo.png'))
        self.loadTimmings()
        self.loadDeadlines()
        self.loadNotes()
        self.addTarget_button.pressed.connect(self.addTarget)
        self.setTimmingsButton.pressed.connect(self.setTimmings)
        self.clearDeadlines_button.pressed.connect(self.clearDeadlines)
        self.addDeadline_button.pressed.connect(self.addDeadlines)
        self.blankNow_button.pressed.connect(screenBlankFunc)
        self.recentLongBreak_button.pressed.connect(self.resetBreaks)
        self.setBreaksProgress(0)
        
        # self.exit=QAction("Exit Application",shortcut=QKeySequence("Ctrl+q"),triggered=lambda:self.exit_app)
        # self.addAction(self.exit)
    
    def setUpTargets(self): loadFromFile()
        
    def clearDeadlines(self):
        DEADLINES = None
        DEADLINES = [[],[],[]]
        with open("deadlines.txt","w") as _: pass
        self.displayDeadlines()
    def resetBreaks(self):
        breaks.reset()

    def loadTimmings(self): 
        a,b,c,d = breaks.getTimmings()
        self.shortBreak_spinBox.setValue(a)
        self.longBreak_spinBox.setValue(b)
        self.breakInterval_spinBox.setValue(c)
        self.longBreakFrquency_spinBox.setValue(d)
    def setTimmings(self):
        breaks.setTimmings(self.shortBreak_spinBox.value(),self.longBreak_spinBox.value(),self.breakInterval_spinBox.value(),self.longBreakFrquency_spinBox.value())

    def setBreaksProgress(self,val):
        self.breaks_progressBar.setValue(val)
    def addTarget(self):
        if(self.targetTitle_input.text().strip()!=""):
            TARGETS[0].append(self.targetTitle_input.text())
            TARGETS[1].append(self.targetTime_input.text())
            TARGETS[2].append(self.targetDescription_input.text() )# note my quiality use of whole word varibles
            s = ""
            for i in range(len(TARGETS[0])):
                s += f"{TARGETS[1][i]} | {TARGETS[0][i]} - {TARGETS[2][i]}\n"
            self.target_text.setText(s)
    def loadDeadlines(self):
        with open("deadlines.txt","r") as f:
            lines = f.readlines()
            for l in lines:
                a, b, c = l.split(SEPERATOR)
                DEADLINES[0].append(a)
                DEADLINES[1].append(b)
                DEADLINES[2].append(c)
        self.displayDeadlines()

    
    def addDeadlines(self):
        if(self.deadlineTitle_input.text().strip()!=""):
            DEADLINES[0].append(self.deadlineTitle_input.text())
            DEADLINES[1].append(self.deadlineDate_input.text())
            DEADLINES[2].append(self.deadlineDescription_input.text() )# note my quiality use of whole word varibles
            with open("deadlines.txt","w") as f:
                for i in range(len(DEADLINES[0])):
                    f.write(f"{DEADLINES[0][i]}{SEPERATOR}{DEADLINES[1][i]}{SEPERATOR}{DEADLINES[2][i]}\n")
            self.displayDeadlines()
        

    def displayDeadlines(self):
        s = ""
        for i in range(len(DEADLINES[0])):
            s += f"{DEADLINES[1][i]} | {DEADLINES[0][i]} - {DEADLINES[2][i].strip()}\n"
        self.deadlines_text.setText(s)

    def loadNotes(self):
        with open("notes.txt","r") as f:
            self.notes_plainText.setPlainText(f.read())
    def saveNotes(self):
        with open("notes.txt","w") as f:
            f.write(self.notes_plainText.toPlainText())
    def closeEvent(self,event):
        saveToFile()
        self.saveNotes()
        return super().closeEvent(event)
        

if __name__=="__main__":
    os.chdir(DIRECTORY)
    breaks = breaks()
    TARGETS = [[],[],[]]#title, time, description
    DEADLINES = [[],[],[]]#title, date, description
    timmingsThread = threading.Thread(target=notifyTimings, args=(),daemon=True)
    timmingsThread.start()
    MainApp = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    ret = MainApp.exec_()
    sys.exit(ret)
