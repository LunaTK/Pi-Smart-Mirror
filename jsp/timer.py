
import sys
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QLCDNumber
from PyQt5 import QtCore, QtWidgets, QtGui


class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)
        self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(500, 230)
        self.move(0, 0)
        self.setStyleSheet("background-color: rgb(0,0,0);\n"
                           "color: rgb(255,255,255);")

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.display(text)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    clock = DigitalClock()
    
    clock.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    clock.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    clock.show()
    sys.exit(app.exec_())
