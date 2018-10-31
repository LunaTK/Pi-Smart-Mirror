import numpy as np
import cv2

def faceDetect():
    #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    frame = cv2.imread("sample.jpg",-1)
    print(frame.shape)
    # 1 : color. transparentX, default, 0: grayscale -1: unchanged
    # (y,x,color)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Hue Saturation Value
        # test = face_cascade.load('haarcascade_frontalface_default.xml')
        # print(test) #->true


    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # scalefactor = 1.3 : Since some faces may be closer to the camera,
        #  they would appear bigger than faces in the back.
        # this will compensates for that
        # minNeighbors = 5 : how many objects are detected near the current
        # minSize=(30,30) : the size of each window
    lower_dark = np.array([0,0,0])
    upper_dark = np.array([180,255,30])

    # color to go on
    #lower to brighter
    #upper to darker

    #frame[np.where((frame == [0, 0, 0]).all(axis=2))] = [0, 33, 166]
    #cv2.imshow("try", frame)

    mask = cv2.inRange(hsv, lower_dark, upper_dark)
    res2 = cv2.bitwise_not(frame, frame, mask=mask)
    print(mask[40][110])
    img = cv2.imread('sample.jpg', 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    color = (0, 0, 255)
    limit1, limit2 = faceDetectCode()
    for y in range(0, limit2):
        x_min = 0
        x_max = limit1
        '''
        for x in range (0,getX(img)) :
            if mask[y][x] == 255 :
                for rgb in range(0, 3):
                    img[y][x][rgb] = 255-((255-gray[y][x])*(255-color[rgb])/255)
        '''
        if y < limit2/4 :
            for x_max in range(limit1, 0, -1) :
                if mask[y][x_max] == 255 :
                    break
            for x_min in range(0, getX(img)):
                if mask[y][x_min] == 255 :
                    break
            for x in range (x_min, x_max) :
                for rgb in range(0, 3):
                    img[y][x][rgb] = gray[y][x] * (color[rgb]) / 255
                    #img[y][x][rgb] = 255-((255-gray[y][x])*(255-color[rgb])/255)
        else :
            for x in range(0, getX(img)):
                if mask[y][x] == 255:
                    for rgb in range(0, 3):
                        img[y][x][rgb] = gray[y][x] * (color[rgb]) / 255
                        #img[y][x][rgb] = 255 - ((255 - gray[y][x]) * (255 - color[rgb]) / 255)

    cv2.imshow('result',img)
    # cv2.imshow('image', frame)
    cv2.imshow('mask', mask)
    # filtered -> black non filtered -> white
    #cv2.imshow('filtered result', res2)

def getX(img) :
    return len(img[0])
def getY(img) :
    return len(img)


def faceDetectCode():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    frame = cv2.imread("sample.jpg", -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 2, 0, (30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3, 4, 0)
        # face -> x, y(location)&& w, h
        #cv2.putText(frame, 'Detected Face', (x - 5, y - 5), font, 0.9, (255, 255, 0))
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
    '''
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    '''
    # cv2.imshow('face',frame)
    return x+w, y+h


image = np.zeros((256,512,3), np.uint8)
for i in range(0,getY(image)):
    for bgr in range(0,3) :
        image[i][i][bgr] += 250
img = cv2.imread('sample.jpg',1)
color = (255,0,0)

faceDetect()
#cv2.imwrite('sample.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()