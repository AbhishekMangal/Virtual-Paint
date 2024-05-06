import cv2
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3,1500)
cap.set(4,1580)
cap.set(10, 100)
#Find Colours


# Colours in form of list for hue
myColors = [[102,255,12,179, 255,247],
            [0 ,87,137,179,255 ,255],
            [4,60,141,179,255,255],
            [153,70,67,179,255,255 ]]
myColorValues = [[102,51,0],   #BGR
                 [51,153,255],


                 [53,255,51],
                 [255,51,255]]

myPoints = [] # x, y ,colorID
def FindColour(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y =  getContouers(mask)
        cv2.circle(imgResult, (x,y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y ,count])
        count +=1
        # cv2.imshow(str(color[0]), mask)
    return newPoints
def getContouers(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w, h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)  #find area
        # print(area)
        if area>5000:
            # cv2.drawContours(imgResult, cnt , -1, (255, 255 ,0), 3) # clour the shapes edges
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(approx) # gives the corner point of each shapes

            # print(len(approx))
            # objectCor = len(approx)
            x, y, w,h= cv2.boundingRect(approx)
    return x+w//2,y

def DrawOnCanvas(myPoints , myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints =  FindColour(img, myColors, myColorValues);
    if len(newPoints)!=0:
        for newP in newPoints: #getiing as list
            myPoints.append(newP)
    if len(myPoints)!=0:
        DrawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Video" , imgResult)
    if(cv2.waitKey((1)) & 0xFF == ord('q')):
        break



