import cv2 as cv
import numpy as np
import time

def intersection(img):
    height,width,channels=img.shape
    ppt = np.array([
        [width/20,height/20*19],
        [width/20*19,height/20*19],
        [width/20*19,height/20],
        [width/20,height/20]
        ], np.int32)
    ppt = ppt.reshape((-1, 1, 2))
    cv.fillPoly(img, [ppt], (255, 255, 255), 8)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, th = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(th, 1, cv.CHAIN_APPROX_SIMPLE)
    if len(contours)>2:
        return True
    else:
        return False
#opening camera
cap=cv.VideoCapture('line.mp4')
if not cap.isOpened():
    print("Camera cannot be opened")
#height&widht of captured video
(height,width)=(640,480)
ret = cap.set(cv.CAP_PROP_FRAME_WIDTH, height)
ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT, width)
#ret = cap.set(cv.CAP_PROP_FPS,10)

while(cap.isOpened()):
    #capture video frame by frame
    ret, frame= cap.read()
    frame=~frame
    #ret gives bool
    if not ret:
        print("Can't receive frame.EXİTİNG...")
    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    _, th = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(th, 1, cv.CHAIN_APPROX_SIMPLE)
    clrth=cv.cvtColor(th,cv.COLOR_GRAY2BGR)
    cv.drawContours(clrth, contours, -1, (0, 255, 0), 2)

    (x, y), (MA, ma), angle = cv.fitEllipse(max(contours, key=cv.contourArea))


    if len(contours)>0:
        c = max(contours, key=cv.contourArea)
        M = cv.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv.line(clrth, (cx, 0), (cx, 480), (255, 0, 0), 1)
        cv.line(clrth, (0, cy), (640, cy), (255, 0, 0), 1)

        #print('error on x axis:'+str((cx-320)/320)+'(-1,1)')
    if intersection(frame):
        print('intersection')
    #display frame
    cv.line(clrth,(320,230),(320,250),(0,0,255),3)
    cv.putText(frame,'Angle:'+str(angle),(10,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv.LINE_4)
    cv.imshow('Normal',~frame)
    cv.imshow('Contours', clrth)
    cv.imshow('asds', th)

    #press 'ESC' to quit
    if cv.waitKey(1) == 27:
        break


cap.release()
cv.destroyAllWindows()