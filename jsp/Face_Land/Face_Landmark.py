import cv2
import dlib
import numpy as np
import math
import statistics

def face_land():
    detector = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")
    #predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    img = cv2.imread("tg.jpg",-1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in rects:
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    shape = predictor(gray, rect)
    posX = []
    posY = []
    coords = np.zeros((shape.num_parts, 2), dtype="int")
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)

        for (i, (x, y)) in enumerate(coords):
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
            if(-1<i and i<60):
                posX.insert(i+1,x)
                posY.insert(i+1,y)
                cv2.putText(img, str(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                
#    for i in range(1,49):
#        print("index : ", i , "position : ", posX[i], posY[i])

#location of right eye 37-42
    h_right=0
    w_right=0
    for i in range(37, 43):
        h_right=posY[i]+h_right
        w_right=posX[i]+w_right

    h_right=h_right/6
    w_right=w_right/6
#    print("h_right : ", h_right , "w_right : ", w_right)
#location of left eye 43-48
    h_left=0
    w_left=0
    for i in range(43, 49):
        h_left=posY[i]+h_left
        w_left=posX[i]+w_left

    h_left=h_left/6
    w_left=w_left/6
#    print("h_left : ", h_left , "w_left : ", w_left)    
#slope
    slope=abs((h_left-h_right)/(w_left-w_right))
    print("slope is : ", slope)
#middle of face 28-31
    mid=0
    for i in range(28, 32):
        mid=posX[i]+mid
        
    mid=mid/4
    print("mid is : ", mid)
#face landmark 1-17, 9 is virtual mid

    v_mid=posX[9]
    lr_ratio=0
    
#왼쪽으로 기울어짐
    if (abs(mid-posX[1])>abs(mid-posX[17])):
        for i in range (1, 9):
            lr_ratio=(abs(mid-posX[9-i])-abs(mid-posX[9+i]))/(mid-posX[9-i])+lr_ratio

#오른쪽으로.기울어짐
    else:
        for i in range (1, 9):
            lr_ratio=(abs(mid-posX[9+i])-abs(mid-posX[9-i]))/(mid-posX[9+i])+lr_ratio

#사진속 좌우 얼굴 비율
    lr_ratio=abs(lr_ratio/8)
    print("lr_ratio : ", lr_ratio)

#(1, 8) = (2, 7) = (3, 6) = (4, 5)

    slopeL=[0,0,0,0]
    slopeR=[0,0,0,0]

    slopeL[0]=abs((posY[1]-posY[8])/(posX[1]-posX[8]))
    slopeR[0]=abs((posY[17]-posY[10])/(posX[17]-posX[10]))

    slopeL[1]=abs((posY[2]-posY[7])/(posX[2]-posX[7]))
    slopeR[1]=abs((posY[16]-posY[11])/(posX[16]-posX[11]))

    slopeL[2]=abs((posY[3]-posY[6])/(posX[3]-posX[6]))
    slopeR[2]=abs((posY[15]-posY[12])/(posX[15]-posX[12]))

    slopeL[3]=abs((posY[4]-posY[5])/(posX[4]-posX[5]))
    slopeR[3]=abs((posY[14]-posY[13])/(posX[14]-posX[13]))

    devL=statistics.stdev(slopeL)
    devR=statistics.stdev(slopeR)

    print("Standard Deviation of slopeL is ", devL)
    print("Standard Deviation of slopeR is ", devR )

#높이에 따른 얼굴 높이 비율
#1, 17 눈 위치
#mid 3 4, mid 15 14 코 위치
#5 13 입술 아래 위치
#49 55 입술 양쪽, 60 56 바로 밑 


#계산
    devAve=(devL+devR)/2
    if (devAve<0.2):
        face_type=1
    elif (devAve>0.2 and devAve<0.4):
        face_type=2
    elif (devAve>0.4 and devAve<0.85):
        face_type=3
    else:
        face_type=4

#얼굴형
    if (face_type==1):
        print("Your face shape is : V Line")
    elif (face_type==2):
        print("Your face shape is : Circle")
    elif (face_type==3):
        print("Your face shape is : Oval")
    else:
        print("Your face shape is : Square")
        
#end    
    cv2.imshow('face_landmark', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

face_land()
