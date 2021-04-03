import cv2
import numpy as np
framewidth = 1024
framehight = 640
cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,framehight)
cap.set(10,150)


mycolors = [[110,50,50,130,255,255],[0,50,50,10,255,255],[57,76,0,100,255,255]]
mycolorsValues = [[255,0,0],[0,0,255],[0,255,0]]
mypoints =  []# == [x ,y , colorId ]

def findcolor(img,mycolors,mycolorsValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    Newpoints = []
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getcontours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorsValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            Newpoints.append([x,y,count])
        count += 1
       # cv2.imshow(str(color[0]),mask)
    return Newpoints


def getcontours(img):
    contours,hierarcy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in  contours:
        area = cv2.contourArea(cnt)
        
        if area>500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x , y,w,h =cv2.boundingRect(approx)
    return x+w//2,y
def drawoncanvas(mypoints,mycolorsValues):
    for points in mypoints:
        cv2.circle(imgResult,(points[0],points[1]),10,mycolorsValues[points[2]],cv2.FILLED)



while True:
    success, img = cap.read()
    imgResult = img.copy()
    Newpoints = findcolor(img,mycolors,mycolorsValues)
    if len(Newpoints)!=0:
        for new in Newpoints:
            mypoints.append(new)
    if len(mypoints)!=0:
        drawoncanvas(mypoints,mycolorsValues)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break