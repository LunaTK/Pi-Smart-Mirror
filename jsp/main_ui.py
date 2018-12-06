import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from PyQt5 import QtTest
import gif_test
import recogcustomer as rc
import hairdesign as hd
import cv2

# testss


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Position & Size
        self.setGeometry(0, 700, 1016, 1560)
        self.setWindowTitle('mirror')
        # Set window background color
        self.setAutoFillBackground(True)
        self.setStyleSheet("QWidget{background: #000;}")
        #self.setWindowFlags(Qt.FramelessWindowHint)
# Color list for dye

        self.c1 = QPushButton("", self)
        self.c1.resize(40, 40)
        self.c1.move(240, 0)
        self.c1.setStyleSheet("QPushButton{border: none;}")

        self.c2 = QPushButton("", self)
        self.c2.resize(40, 40)
        self.c2.move(290, 0)
        self.c2.setStyleSheet("QPushButton{border: none;}")
        self.c3 = QPushButton("", self)
        self.c3.resize(40, 40)
        self.c3.move(340, 0)
        self.c3.setStyleSheet("QPushButton{border: none;}")
        #self.c1.setStyleSheet("QPushButton{image:url(colors/brown.png); border: none;}")
        self.c1.clicked.connect(partial(self.color_choose, (30,30,255)))
        #self.c2.setStyleSheet("QPushButton{image:url(colors/red.png); border: none;}")
        self.c2.clicked.connect(partial(self.color_choose, (255,30,30)))
        #self.c3.setStyleSheet("QPushButton{image:url(colors/yellow.png); border: none;}")
        self.c3.clicked.connect(partial(self.color_choose, (30,255,255)))
####### Set Img variable ############
        self.path = ""
        self.hair = 0
        self.tag = False
        self.username_tv = ''#shir c++ code - -?

# Set Img Poistion & label
        self.pic = QLabel(self)
        self.pic.setGeometry(125, 100, 400, 600)
        #pixmap = QPixmap("black.png")
        # self.pic.setPixmap(pixmap)

# Set Text Position & label
        self.text_label = QLabel("", self)
        self.text_label.setGeometry(100, 500, 700, 20)
        self.text_label.setStyleSheet(
            "background:#000; color:rgb(255,255,255)")

############## btn1 ##################
        self.btn1 = QPushButton("    ", self)
        self.btn1.resize(180, 180)
        self.btn1.move(10, 700)
        self.btn1.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/user.png); border: none;}
      QPushButton:hover{image:url(icons/user_grey.png);border: none;}
   ''')
        self.btn1.clicked.connect(self.face_recog)

############## btn2 ##################
        self.btn2 = QPushButton("    ", self)
        self.btn2.resize(180, 180)
        self.btn2.move(220, 700)
        self.btn2.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/dye.png); border: none;}
      QPushButton:hover{image:url(icons/dye_grey.png);border: none;}
   ''')
        self.btn2.clicked.connect(self.show_colors)

############## btn3 ##################
        self.btn3 = QPushButton("    ", self)
        self.btn3.resize(180, 180)
        self.btn3.move(430, 700)
        self.btn3.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/hair.png); border: none;}
      QPushButton:hover{image:url(icons/hair_grey.png);border: none;}
   ''')
     # show new hair image
        self.btn3.clicked.connect(self.button3)

############## btn4 ##################
        self.btn4 = QPushButton("    ", self)
        self.btn4.resize(180, 180)
        self.btn4.move(640, 700)
        self.btn4.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/question.png); border: none;}
      QPushButton:hover{image:url(icons/question_grey.png);border: none;}
   ''')
        self.btn4.clicked.connect(self.temp)
############## btn5 ##################
        self.btn5 = QPushButton("    ", self)
        self.btn5.resize(180, 180)
        self.btn5.move(850, 700)
        self.btn5.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/video.png); border: none;}
      QPushButton:hover{image:url(icons/video_grey.png);border: none;}
   ''')

######### back  #######
        self.back = QPushButton("", self)
        self.back.resize(60, 60)
        self.back.move(940, 1470)
        self.back.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/back.png); border: none;}
      QPushButton:hover{image:url(icons/back_grey.png);border: none;}
   ''')
        ##self.btn1.clicked.connect(self.delete_img) #?lets erase this for testing

######### setting ############
        self.setting = QPushButton("", self)
        self.setting.resize(60, 60)
        self.setting.move(940, 150)
        self.setting.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/settings.png); border: none;}
      QPushButton:hover{image:url(icons/setting_grey.png);border: none;}
   ''')
       # do hair segmentation

        self.setting.clicked.connect(self.make_wig)
#wait

######### camera ############
        self.camera = QPushButton("", self)
        self.camera.resize(60, 60)
        self.camera.move(940, 50)
        self.camera.setStyleSheet(
            '''
      QWidget{background-image:url()}
      QPushButton{image:url(icons/camera.png); border: none;}
      QPushButton:hover{image:url(icons/camera_grey.png);border: none;}
   ''')
       # do camera work and ...
        self.camera.clicked.connect(rc.piCap)


######### movement ########
    def make_wig(self) :
        hd.makeWig(self.hair.width, self.hair.height)
        self.hair.dir_size += 1

    def temp(self) :
        self.hair.wi += 1
        self.hair.wi %= self.hair.dir_size
        print(self.hair.wi)

    def btn_clicked(self):
        print("clicked!")
#       print(self.btn1.text())

    def show_img(self, imgname):
        print("Hello, Welcome to Our JSP Salon")
        print(self.username_tv)
        self.pic.setPixmap(QPixmap(imgname))

    def delete_img(self):
        self.pic.clear()

    def set_text(self):
        self.text_label.setText("Hello, Welcome to Our JSP Salon\n>>Customer Information<<\nName: "+self.username_tv)
        #self.text_label.setText("")
        #self.text_label.setText("Name: "+self.username_tv)
        QtTest.QTest.qWait(7000)
        self.text_label.clear()

    def show_colors(self):
        if self.tag == False:
            print("?")
            return
        self.c1.setStyleSheet("QPushButton{image:url(colors/brown.png); border: none;}")
        self.c1.setEnabled(True)
        #self.c1.clicked.connect(partial(self.color_choose, (30,30,255)))
        self.c2.setStyleSheet("QPushButton{image:url(colors/red.png); border: none;}")
        self.c2.setEnabled(True)
        #self.c2.clicked.connect(partial(self.color_choose, (255,30,30)))
        self.c3.setStyleSheet("QPushButton{image:url(colors/yellow.png); border: none;}")
        self.c3.setEnabled(True)
        #self.c3.clicked.connect(partial(self.color_choose, (30,255,255)))

    def button3(self):
        if self.tag == False:
            return
        self.hair.changeWig(self.hair.wi)
        self.showResult()

    def showResult(self) :
        self.pic.clear()
        self.pic.setPixmap(QPixmap(self.hair.returnQImage()))

    def color_choose(self, color):
        self.c1.setStyleSheet("border:none;")
        self.c1.setEnabled(False)
        self.c2.setStyleSheet("border:none;")
        self.c2.setEnabled(False)
        self.c3.setStyleSheet("border:none;")
        self.c3.setEnabled(False)

        self.hair.changeColor(color)
        self.showResult()
        # Do dye with "color"
        print("You choose : ", color)

    def face_recog(self):
        userId, userName, current, self.tag = rc.recognitionCustomer()
        self.username_tv = userName
        self.path = current
        print(self.tag)
        if self.tag:
            self.hair = hd.hairror(self.path, "long")
        self.show_img(self.path)
        self.set_text()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()  # loop -> event appear -> method
