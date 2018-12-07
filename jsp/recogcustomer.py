#Code for customer face recognition
#By Jukyung Hong
import face_recognition
import os
from os import listdir
from os.path import isfile, join
import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from  PyQt5.QtWidgets import *
from PyQt5 import *
import sys
from picamera import PiCamera
import time

class registerdialog(QtWidgets.QDialog):

    def __init__(self):
        super(registerdialog, self).__init__()

        self.title = 'Register New Customer: '
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.left = 100
        self.top = 60
        self.width = 400
        self.height = 100

        self.name = QtWidgets.QLineEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        #layout.addRow('Password', self.password)
        layout.addWidget(self.button_box)
        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.setMinimumWidth(350)


'''
class cusInfo :
    def __init__(self) :
        self.usernum = -1

#ci = cusInfo()
'''

#class popupreg

def piCap():
    path = pwd()
    path_store = mkdir_newUser(path) + "/current.jpg"
    with PiCamera() as camera:
        camera.resolution = (400,600)
        camera.start_preview()
        time.sleep(4)
        camera.capture(path_store)
        camera.stop_preview()

#Function for saving current path
def pwd():
    pwd = 'pwd > path.txt'
    os.system(pwd)
    path_file = open('path.txt', 'r')
    path = path_file.readline()
    path_file.close()
    return path

def pwd_wig():
    os.system("cd ./wigs/")
    pwd = 'pwd > path_wig.txt'
    os.system(pwd)
    path_file = open('path_wig.txt', 'r')
    path = path_file.readline()
    path_file.close()
    os.system("cd ../")
    return path

#function for make path for known people
def mkdir_newUser(path):
    tmp = path.split('\n')
    plusdir = "/current/"
    chkdir = tmp[0] + plusdir
    if not os.path.isdir(chkdir):
        mkdir = 'mkdir ./current'
        os.system(mkdir)
        print("System: File known created")
    return chkdir

#function for make path for known people
def mkdir(path):
    tmp = path.split('\n')
    plusdir = "/known/"
    chkdir = tmp[0] + plusdir
    if not os.path.isdir(chkdir):
        mkdir = 'mkdir ./known'
        os.system(mkdir)
        print("System: File known created")
    return chkdir
def call_known_list(path):
    files = [f for f in listdir(path) if isfile(join(path,f))]
    files.sort()
    return files

def caluserNum(path):
    num = int(0)
    usernum = ''
    command = 'ls ./known | wc -l > howmanycustomer.txt'
    os.system(command)

    file = open('howmanycustomer.txt','r')
    num = int(file.readline())
    num = int(num/2)+1
    usernum = str(num)
    return usernum

def isFirst(path):
    files = call_known_list(path)
    if not files:
        return False
    else:
        return True
          #
def save_newCusInfo(knownfilepath,customerName,userNo):
    filename = knownfilepath + userNo + ".txt"
    userInfo = open(filename,"w")
    userInfo.write(userNo+"\n")
    userInfo.write(customerName)
    #userInfo.write()
    userInfo.close()

def save_newCusPic(userNo):
    command = 'cp ./current/current.jpg ./known/' + userNo+'.jpg'
    os.system(command)

def read_UserInfo(knownfilepath,customerNum):
    filename = customerNum + ".txt"
    userInfo = open(filename,"r")
    infolist = userInfo.readlines()
    username = infolist[1]
    userInfo.close()
    return username, customer
'''
def register():
    textbox = QlineEdit()
    textbox.move(20,20)
    textbox.resize(280,40)
'''#gogo okok

def get_name():
    msgname11 = registerdialog()
    if msgname11.exec_():
        textsss = msgname11.name.text()
        print(textsss)
    return textsss

def recognitionCustomer():
    customerNumber = ''
    mainpath = pwd()
    knownpath = mkdir(mainpath)
    currentpath = mkdir_newUser(mainpath)
    currentimage= currentpath + "current.jpg"
    files = call_known_list(knownpath)

    if not files:
        print("System initialization begins")
        #piCap()
        return "","","",False
    print(currentimage)
#print(mainpath)
#print(knownpath)
#print(currentpath)
#piCap()
#path for Current User
#print(unknownpath)
    unknown_image = face_recognition.load_image_file(currentimage)
    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("Error Code:00001 No Face Found")
        
        quit()

# Load the jpg files into numpy arrays
    for i in range(0,len(files),1):
        print(files[i])
        filename = files[i]

        tmpfortxt = files[i].split(".")

        if tmpfortxt[1] != 'jpg':
            continue
        image = face_recognition.load_image_file(knownpath+filename)
        try:
            encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            print("First visit")
            newusername = get_name()
            customerNumber = caluserNum(knownpath)
            save_newCusPic(customerNumber)
            print(customerNumber)
            save_newCusInfo(knownpath,newusername,customerNumber)
            print(knownpath+customerNumber+".jpg")

            return customerNumber,newusername,knownpath+customerNumber+".jpg",results[0]

        known = [encoding]
        results = face_recognition.compare_faces(known, unknown_face_encoding)

        if results[0] == True:
            tmp = filename.split('.')
            fn = tmp[0] + '.txt'
            pathforinfo = knownpath + fn

            file = open(pathforinfo,'r')
            info = file.readlines()
            username = info[1]
            print("Welcome back, " + username)
            #print(tmp[0],username, currentpath, results[0])

            return tmp[0], username, currentpath+"current.jpg", results[0]

        elif results[0] == False:
            continue
        else:
            print("ERROR")

    if results[0] == False:
        print("First visit")
        newusername = get_name()
        customerNumber = caluserNum(knownpath)
        save_newCusPic(customerNumber)
        print(customerNumber)
        save_newCusInfo(knownpath,newusername,customerNumber)
        print(knownpath+customerNumber+".jpg")

        return customerNumber,newusername,knownpath+customerNumber+".jpg",results[0]
        #--------------------------------------------------------------------------------------------------------------

