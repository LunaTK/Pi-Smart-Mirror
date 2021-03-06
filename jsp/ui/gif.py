from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon,QFont,QPixmap,QPalette
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QTimer,QPoint
import PyQt5.QtWidgets,PyQt5.QtCore

import time,random,subprocess,sys,json

class cssden(QMainWindow):
    def __init__(self):
        super(cssden, self).__init__()


        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setFixedSize(400,300)
        self.move(500, 0)

            #timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_)
        #self.timer.start(50000)                       # changed timer timeout to 1s

        self.timer2 = QTimer(self)                 # second gif
        self.timer2.timeout.connect(self.timer2_)  # 
        self.timer2.start(500)                     # 

            #gif
        self.moviee = QLabel(self)
        self.movie = QtGui.QMovie("sample.gif")
        self.moviee.setMovie(self.movie)
        self.moviee.setGeometry(0,0,400,300)
        self.movie.start()
        self.show()

                    
    def timer2_(self):                # second gif
        tt = open("mode.json", 'w')   # 
        i = random.randint(0,1)       # 
        if i == 1:                    #
            json.dump('aaa', tt)      #
        elif i == 0:                  #
            json.dump('bbb', tt)      #
        tt.close()                    #
        
    def timer_(self):
        tt = open("mode.json", 'r')
        self.mode = json.load(tt)
        tt.close()
        print (self.mode)
        if self.mode == "sample":
            self.movie = QtGui.QMovie("sample.gif")
            self.moviee.setMovie(self.movie)     # I added
            self.movie.start()                   # those lines
        else:                                          
            self.movie = QtGui.QMovie("sample.gif")
            self.moviee.setMovie(self.movie)     # and here
            self.movie.start()                   # too

        #center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow{background-color: rgb(0,0,0);border: 1px solid black}")

ex = cssden()
sys.exit(app.exec_())
