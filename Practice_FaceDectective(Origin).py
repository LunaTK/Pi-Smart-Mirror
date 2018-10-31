import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX

def faceDetectCode():
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    frame = cv2.imread("sample.jpg", -1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 2, 0,(30,30))

    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3,4,0)
        #face -> x, y(location)&& w, h
        cv2.putText(frame,'Detected Face', (x-5,y-5),font,0.9,(255,255,0))
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = frame[y:y+h, x:x+w]
    '''
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    '''
    #cv2.imshow('face',frame)
       
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return x+w
faceDetectCode()
