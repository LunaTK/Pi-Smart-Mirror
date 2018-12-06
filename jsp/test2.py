import sys
import main
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
#import connect
from PyQt5 import QtTest

'''
class AdminWindow(QMainWindow):
    def __init__(self):
        uper().__init__()
        # Set Position & Size
        self.setGeometry(0, 250, 1080, 1670)
        self.setWindowTitle('mirror')
        # Set window background color
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            QWidget{
                background: #000;
            }
        """)
        
        Admin Window
        What we need
            Back ->
            Make Wig ->
        
'''   

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Position & Size
        self.setGeometry(0, 250, 1080, 1670)
        self.setWindowTitle('mirror')
        # Set window background color
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            QWidget{
                background: #000;
            }
        """)
     ######## Set Img Poistion & label
        self.label = QLabel(self)
        self.label.setGeometry(125, 20, 500, 600)
        pixmap = QPixmap("black.png")
        self.label.setPixmap(pixmap)

    ######### Set Text Position & label
        self.text_label = QLabel("",self)
        self.text_label.move(125,700) 
        self.text_label.setStyleSheet("color : rgb(255,255,255)")
        
        self.setWindowFlags(Qt.FramelessWindowHint)
       
 

############## btn1 ##################
        self.btn1 = QPushButton("    ",self)
        self.btn1.resize(128,128)    
        self.btn1.move(29,1400)
        self.btn1.clicked.connect(self.btn_clicked)
        #self.btn1.clicked.connect(partial(self.show_img, "white.png"))
        self.btn1.clicked.connect(partial(self.show_img, "images/sample_2.jpg"))
        self.btn1.setStyleSheet(
   ''' 
      QWidget{background-image:url()}
      QPushButton{image:url(icon/salon.png); border: none;}
      QPushButton:hover{image:url(icon/salon_grey.png);border: none;}
   ''')

############## btn2 ################
        self.btn2 = QPushButton("    ",self)
        self.btn2.resize(128,128)
        self.btn2.move(186,1400)
        self.btn2.clicked.connect(self.btn_clicked)
        self.btn2.clicked.connect(partial(self.show_test))
        self.btn2.setStyleSheet(
   ''' 
      QWidget{background-image:url("icon/hairstyle.png")}
      QPushButton{image:url(icon/hairstyle.png);border: none;}
      QPushButton:hover{image:url(icon/hairstyle_grey.png);border: none;}
   ''')

############# btn3 #####################
        self.btn3 = QPushButton("    ",self)
        self.btn3.move(343,1400)
        self.btn3.resize(128,128)
        self.btn3.clicked.connect(self.btn_clicked)
        self.btn3.clicked.connect(self.set_text)
        self.btn3.clicked.connect(partial(self.show_img, "black.png"))
        self.btn3.setStyleSheet(
   ''' 
      QWidget{background-image:url("icon/hairgel.png")}
      QPushButton{image:url(icon/hairgel.png);border: none;}
      QPushButton:hover{image:url(icon/hairgel_grey.png);border: none;}
   ''')
        
############ for Testing
        
        
    def btn_clicked(self):
        print("clicked!")
#       print(self.btn1.text())

    def show_img(self,imgname):
        print("now img name is",imgname)
        self.label.setPixmap(QPixmap(imgname))
    def show_test(self,file):
        img = main.test()
        self.label.setPixmap(QPixmap(img))
        
    def set_text(self):
        #print("now")
        self.text_label.setText("hi hello nice to meet you")
        QtTest.QTest.qWait(3000)
        #print("now")
        self.text_label.clear()
        result_Image = main.finalImage()
    

app = QApplication(sys.argv)
window = MyWindow()       
window.show()
app.exec_() #loop -> event appear -> mathod