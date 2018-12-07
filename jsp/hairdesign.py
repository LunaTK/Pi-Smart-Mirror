import numpy as np
import cv2
from matplotlib import pyplot as plt
import dlib
import math
import statistics
import os
import time
import recogcustomer as rc
#from picamera import PiCamera

from PyQt5.QtGui import *


def position(img):
    detector = cv2.CascadeClassifier(
        "Face_Land/lbpcascade_frontalface_improved.xml")
    # predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    predictor = dlib.shape_predictor(
        "Face_Land/shape_predictor_68_face_landmarks.dat")
    gray = 0
    if (len(img[0][0]) == 3):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif (len(img[0][0]) == 4):
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    rects = detector.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in rects:
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    shape = predictor(gray, rect)
    posX = []
    posY = []
    return (posX, posY, shape)


class hairror:
    def __init__(self, dir, hair_type):
        self.width = 400
        self.height = 600
        self.orig_img = cv2.imread(dir, -1)
        self.orig_img = cv2.resize(self.orig_img, (self.width, self.height))
        self.orig_hair_seg = hairSegment(self.orig_img, 10, self.width, self.height, hair_type)
        (self.pX, self.pY, self.shape) = position(self.orig_img)
        self.shape = face_type(self.pX, self.pY, self.orig_img, self.shape)
        (self.x, self.y, self.sx, self.sy) = getXYSize(self.pX, self.pY, self.orig_img, self.shape)
        #self.wigList = (cv2.imread("wigs/sample2.png", cv2.IMREAD_UNCHANGED), cv2.imread("wigs/sample3.png", cv2.IMREAD_UNCHANGED), cv2.imread("wigs/sample5.png", cv2.IMREAD_UNCHANGED))
        #dir = rc.pwd_wig()
        #print(dir)
        self.wig_dirs = rc.call_known_list("/home/pi/Desktop/hd/wigs")
        self.dir_size = len(self.wig_dirs)
        print(self.wig_dirs)
        self.wigList = []
        for i in range( 0, self.dir_size) :
            #tmp = np.zeros( (self.width, self.height, 4), np.uint8 )
            print("wig.dir : ", self.wig_dirs[i])
            tmp = cv2.imread("wigs/"+self.wig_dirs[i], cv2.IMREAD_UNCHANGED)
            self.wigList.append(tmp)
            print(self.wigList[i].shape)
        #print(self.wigList[0].shape)
        print(len(self.wigList))
        self.wig_seg = self.orig_hair_seg
        self.wi = -1
        #print(self.wig_seg)
        self.hair_color = (0, 0, 0)
        self.hair_color_flag = False
        self.result_noColorChange = self.orig_img
        self.result = self.orig_img

    def changeColor(self, new_color):
        self.hair_color = new_color
        if self.wi == -1:
            self.result_noColorChange = paint2(self.orig_img, self.orig_hair_seg, self.hair_color, self.width, self.height)
            self.result = self.result_noColorChange
        else:
            self.result = paint2(self.result_noColorChange, self.wig_seg, self.hair_color, self.width, self.height)

    def changeWig(self, wi):
        self.wi = wi
        (self.result_noColorChange, self.wig_seg) = putWig(self.orig_img, self.wigList[self.wi], self.x, self.y, self.sx, self.sy, self.width, self.height)
        if self.hair_color_flag == True:
            self.changeColor(self.hair_color)
        else:
            self.result = self.result_noColorChange

    def returnQImage(self):
        h, w, c = self.result.shape
        bytesPerLine = 3*w
        tmp = cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB)
        qImg = QImage(tmp.data, w, h, bytesPerLine, QImage.Format_RGB888)
        return qImg


def getXYSize(posX, posY, img, t):
    #print(posX, posY)
    # 15-3=Distance between ear
    width = posX[14] - posX[4] - 5
    x = posX[30]
    y = 0
    if (t == 1):
        height = 2 * (posY[9] - posY[30])
        y = posY[30]
    elif (t == 2):
        height = 2 * (posY[9] - (((posY[31] - posY[30]) * 1 / 3) + posY[30])) - 75
        y = (((posY[31] - posY[30]) * 1 / 3) + posY[30])
    elif (t == 3):
        height = 2 * (posY[9] - (((posY[31] - posY[30]) * 2 / 3) + posY[30])) - 75
        y = (((posY[31] - posY[30]) * 2 / 3) + posY[30])
    elif (t == 4):
        height = 2 * (posY[9] - posY[31])
        y = (posY[9] - posY[31])
    size_x = width / len(img[0])
    size_y = height / len(img)
    mid_list = [0] * 4
    mid_list[0] = int(x)
    mid_list[1] = int(y)
    mid_list[2] = size_x
    mid_list[3] = size_y
    size_x *= 255
    size_x = int(size_x)
    size_x /= 255
    size_y *= 255
    size_y = int(size_x)
    size_y /= 255
    print("width, height", mid_list[0] , mid_list[1] )
    print("size_x and size_y", size_x, size_y)
    return mid_list


def face_type(posX, posY, img, shape):
    coords = np.zeros((shape.num_parts, 2), dtype="int")
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)
        for (i, (x, y)) in enumerate(coords):
            # cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
            if (-1 < i and i < 60):
                posX.insert(i + 1, x)
                posY.insert(i + 1, y)
                # cv2.putText(img, str(i + 1), (x - 10, y - 10),
                # cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # location of right eye 37-42
    h_right = 0
    w_right = 0
    for i in range(37, 43):
        h_right = posY[i] + h_right
        w_right = posX[i] + w_right

    h_right = h_right / 6
    w_right = w_right / 6
    #    print("h_right : ", h_right , "w_right : ", w_right)
    # location of left eye 43-48
    h_left = 0
    w_left = 0
    for i in range(43, 49):
        h_left = posY[i] + h_left
        w_left = posX[i] + w_left
    h_left = h_left / 6
    w_left = w_left / 6
    #print("h_left : ", h_left , "w_left : ", w_left)
    # slope
    slope = abs((h_left - h_right) / (w_left - w_right))
    # middle of face 28-31
    mid = 0
    for i in range(28, 32):
        mid = posX[i] + mid
    mid = mid / 4
    # face landmark 1-17, 9 is virtual mid
    v_mid = posX[9]
    lr_ratio = 0
    # (1, 8) = (2, 7) = (3, 6) = (4, 5)
    slopeL = [0, 0, 0, 0]
    slopeR = [0, 0, 0, 0]
    slopeL[0] = abs((posY[1] - posY[8]) / (posX[1] - posX[8]))
    slopeR[0] = abs((posY[17] - posY[10]) / (posX[17] - posX[10]))
    slopeL[1] = abs((posY[2] - posY[7]) / (posX[2] - posX[7]))
    slopeR[1] = abs((posY[16] - posY[11]) / (posX[16] - posX[11]))
    slopeL[2] = abs((posY[3] - posY[6]) / (posX[3] - posX[6]))
    slopeR[2] = abs((posY[15] - posY[12]) / (posX[15] - posX[12]))
    slopeL[3] = abs((posY[4] - posY[5]) / (posX[4] - posX[5]))
    slopeR[3] = abs((posY[14] - posY[13]) / (posX[14] - posX[13]))
    devL = statistics.stdev(slopeL)
    devR = statistics.stdev(slopeR)
    print(devL, devR)
    # 계산
    devAve = (devL + devR) / 2
    if (devAve < 0.2):
        face_type = 1
    elif (devAve > 0.2 and devAve < 0.4):
        face_type = 2
    elif (devAve > 0.4 and devAve < 0.85):
        face_type = 3
    else:
        face_type = 4

    return face_type


def storeWig(dir, img, x, y, portionX, portionY):
    img[0][0][3] = x
    img[0][1][3] = y
    img[1][0][3] = int(portionX * 255)
    img[1][1][3] = int(portionY * 255)
    print(cv2.imwrite(dir, img, (cv2.IMWRITE_PNG_COMPRESSION,
                                 cv2.IMWRITE_PAM_FORMAT_RGB_ALPHA)))
    return


def loadWig(dir):
    res = cv2.imread(dir, cv2.IMREAD_UNCHANGED)
    return res


def getWigInfo(wigImg):
    x = wigImg[0][0][3]
    y = wigImg[0][1][3]
    sx = wigImg[1][0][3] / 255
    sy = wigImg[1][1][3] / 255
    print("wsx,wsy",sx,sy)
    return (x, y, sx, sy)


def putWig(img, wigimg, base_x, base_y, size_x, size_y, imgWidth, imgHeight):
    print("sx,sy",size_x,size_y)
    (wbase_x, wbase_y, wsize_x, wsize_y) = getWigInfo(wigimg)
    # len(wigimg[0])*size_x/wsize_x
    wwidth = int(len(wigimg[0]) * size_x / wsize_x)
    wheight = int(len(wigimg) * size_y / wsize_y)
    resizedWig = cv2.resize(wigimg, (wwidth, wheight), interpolation = cv2.INTER_AREA)
    wbase_x = int(wbase_x * size_x / wsize_x)
    wbase_y = int(wbase_y * size_y / wsize_y)
    print("bx,by ", base_x, base_y)
    print("wbx,wby ", wbase_x, wbase_y)
    if (wbase_x > base_x):
        xstart = wbase_x - base_x
        txstart = 0
    else:
        xstart = 0
        txstart = base_x - wbase_x
    if (wbase_y > base_y):
        ystart = wbase_y - base_y
        tystart = 0
    else:
        ystart = 0
        tystart = base_y - wbase_y
    nW = imgWidth - txstart
    nH = imgHeight - tystart
    xend = min(len(resizedWig[0]), xstart + nW)
    yend = min(len(resizedWig), ystart + nH)
    txend = txstart + xend - xstart
    tyend = tystart + yend - ystart
    print(xstart, xend, ystart, yend)
    print(txstart, txend, tystart, tyend)
    matchedWig = np.zeros((imgHeight, imgWidth, 4), np.uint8)
    print("tys,tye,txs,txe ", tystart, tyend, txstart, txend)
    print("yst,ye,xs,xe ", ystart, yend, xstart, xend)
    matchedWig[tystart:tyend,
               txstart:txend] = resizedWig[ystart:yend, xstart:xend]

    wigMask = matchedWig[:, :, 3]
    wigMaskInv = cv2.bitwise_not(wigMask)
    result = matchedWig[:, :, 0:3]
    result = cv2.bitwise_and(result, result, mask=wigMask)
    newImg = cv2.bitwise_and(img, img, mask=wigMaskInv)
    return cv2.add(result, newImg), wigMask

# def getXYSize(img) :
#    return (100,125,0.29 ,0.36)


def getHair(img, seg):
    result = cv2.bitwise_and(img,img,seg)
    b,g,r = cv2.split(result)
    bgra = cv2.merge((b,g,r,seg))
    return bgra


def eraseEye(grayImg):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    faces = face_cascade.detectMultiScale(grayImg, 1.3, 2, 0, (30, 30))
    for (x, y, w, h) in faces:
        roi_gray = grayImg[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            for ery in range(y + ey, y + ey + eh):
                for erx in range(x + ex, x + ex + ew):
                    grayImg[ery][erx] = 255
        return y + h, grayImg
    return 0, grayImg


def hairSegment(img, depth, width, height, hairType):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    twidth = 200
    theight = 250
    result = cv2.resize(result, (twidth, theight), interpolation = cv2.INTER_AREA)
    under, result = eraseEye(result)
    for y in range(0, theight):
        for x in range(0, twidth):
            result[y][x] = (result[y][x] // (255 / 90)) * (255 / 90)
    factor = twidth // 20
    for d in range(0, depth):
        # Bilateral Filtering
        result = cv2.bilateralFilter(
            result, 3 * factor, 2 * factor, 2 * factor)
    for d in range(0, depth // 10):
        # Bilateral Filtering
        result = cv2.bilateralFilter(result, int(
            factor * 0.7), 6 * factor, 6 * factor)
    if hairType == "long":
        under = theight
    for y in range(0, theight):
        for x in range(0, twidth):
            result[y][x] = (result[y][x] // (255 / 3)) * (255 / 3)
            if under < y:
                result[y][x] = 0
            else:
                if result[y][x] == 0:
                    result[y][x] = 255
                else:
                    result[y][x] = 0
    result = cv2.resize(result, (width, height), interpolation = cv2.INTER_LINEAR)
    return result


def paint1(img, seg, color, width, height):
    result = np.zeros((height, width, 3), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for y in range(0, height):
        for x in range(0, width):
            for bgr in range(0, 3):
                if seg[y][x] != 0:
                    result[y][x][bgr] = gray[y][x] * color[bgr] / 255
                else:
                    result[y][x][bgr] = img[y][x][bgr]
    return result


def paint2(img, seg, color, width, height):
    result = np.zeros((height, width, 3), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # alpha = (color[0] + color[1] + color[2]) / 3 / 255
    for y in range(0, height):
        for x in range(0, width):
            if seg[y][x] == 255:
                alpha = gray[y][x] / 255
                if alpha > 0.5:
                    alpha = 1 - alpha
                mask = (1 - alpha) * gray[y][x]
                for bgr in range(0, 3):
                    # result[y][x][bgr] = 255-((255-gray[y][x])*(255-color[bgr])/255)
                    result[y][x][bgr] = mask + alpha * color[bgr]
            else:
                for bgr in range(0, 3):
                    result[y][x][bgr] = img[y][x][bgr]
    return result


def makeWig(width, height):
    dir = "current/current.jpg"
    image = cv2.imread(dir, -1)
    print("successfully read image")
    image = cv2.resize(image, (width, height))
    (posX, posY, shape) = position(image)
    t = face_type(posX, posY, image, shape)
    (x, y, sx, sy) = getXYSize(posX, posY, image, t)
    print(x, y, sx, sy)
    seg = hairSegment(image, 50, width, height, "long")
    hairWig = getHair(image, seg)
    wig_dirs = rc.call_known_list("/home/pi/Desktop/hd/wigs")
    print("successfully got wig from image")
    storeWig("wigs/"+str(len(wig_dirs))+".png", hairWig, x, y, sx, sy)
    print("succesfully stored wig image at wigs/"+str(len(wig_dirs))+".png")


def test():
    width = 400
    height = 600
    hairType = "long"
    dirSrc = "images/sample_4.jpg"
    clientImg = cv2.imread(dirSrc, 1)
    print("read base img")
    # portionx = width / len(clientImg[0])
    # portiony = height / len(clientImg)
    clientImg = cv2.resize(clientImg, (width, height))
    (posX, posY, shape) = position(clientImg)
    #print(posX, posY)
    t = face_type(posX, posY, clientImg, shape)
    (x, y, sx, sy) = getXYSize(posX, posY, clientImg, t)
    print("read wig img")
    dirWig = "wigs/sample_3.png"
    wigImg = loadWig(dirWig)
    result = putWig(clientImg, wigImg, x, y, sx, sy, width, height)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    print("made result image")
    #cv2.imshow("result", result)
    # cv2.waitKey(0)

    h, w, c = result.shape
    bytesPerLine = 3*w
    qImg = QImage(result.data, w, h, bytesPerLine, QImage.Format_RGB888)

    return qImg


# test()
