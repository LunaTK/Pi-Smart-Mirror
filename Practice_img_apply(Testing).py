import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if(face_cascade.empty()):
  raise IOError('Unable to load face cascade classifier')

cap = cv2.VideoCapture(0)
scaling_factor = 0.5

# Load our overlay image: hat.png
hat_default = cv2.imread('blonde.png',-1)
 
# Create the mask for the hair
orig_mask = hat_default[:,:,3]
 
# Create the inverted mask for the hat
orig_mask_inv = cv2.bitwise_not(orig_mask)
 
# Convert hat image to BGR
# and save the original image size (used later when re-sizing the image)
hat = hat_default[:,:,0:3]

orighatHeight, origHatWidth = hat.shape[:2]

while True:
  ret, frame = cap.read()
  frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  for(x,y,w,h) in faces:
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    face_w = w
    face_h = h
    face_x1 = x
    face_x2 = face_x1 + face_h
    face_y1 = y
    face_y2 = face_y1 + face_h

    hatWidth = int(face_w + int(face_w * 0.7))
    hatHeight = int(hatWidth * origHatWidth / origHatWidth)
    #cv2.rectangle(frame, (x, y), (x + hatWidth, y + hatWidth), (0, 0, 255), 2)

    hat = hat_default[:,:,0:3]
    hat = cv2.resize(hat, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)

    # setting wig centered wrt recognized face
    x1 = face_x2 - int(face_w/2) - int(hatWidth/2)
    x2 = x1 + hatWidth
    y1 = y - hatHeight- int(face_h*0.5)
    #y1 = y - hatHeight + int(hatHeight*.3)
    y2 = y + int(hatHeight*0.7)
    cropY = 0

    if y1 < 0:
      y1 = 0
      cropY = hat.shape[1] - y2
      hat = hat[cropY:]

    if x2 > frame.shape[1]:
      x2 = frame.shape[1]

    # Check for clipping
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 > frame.shape[0]:
        x2 = w
    if y2 > frame.shape[1]:
        y2 = h

    roi_gray = gray
    roi_color = frame 

    # Re-size the original image and the masks to the hat sizes
    # calcualted above
    mask = cv2.resize(orig_mask, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
    mask = mask[cropY:]
    mask_inv = cv2.resize(orig_mask_inv, (hatWidth,hatHeight), interpolation = cv2.INTER_AREA)
    mask_inv = mask_inv[cropY:]

    y1 = int(y1)
    y2 = int(y2)
    x1 = int(x1)
    x2 = int(x2)
    # take ROI for hat from background equal to size of hat image
    roi = roi_color[y1:y2, x1:int(x1+hatWidth)]
    print(roi.shape)
    # roi_bg contains the original image only where the hat is not
    # in the region that is the size of the hat.
    roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    # roi_fg contains the image of the hat only where the hat is
    roi_fg = cv2.bitwise_and(hat,hat,mask = mask)

    # join the roi_bg and roi_fg
    dst = cv2.add(roi_bg,roi_fg)

    # place the joined image, saved to dst back over the original image
    roi_color[y1:y2, x1:x1+hatWidth] = dst

  cv2.imshow('Hat',frame)
  c = cv2.waitKey(1)
  if c == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
