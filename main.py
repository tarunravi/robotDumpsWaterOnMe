import cv2
import os
from time import sleep
cascPath = '/home/pi/Desktop/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
font = cv2.FONT_HERSHEY_SIMPLEX

def findFaces(video_capture):
    """
    Method identifies the cordinates/size of any faces in frame. 
    """
    face = False
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE)
    
    for (x,y,w,h) in faces:
        area = w*h
        face = True
        
    if face:
        return face, frame, area, (x,y,w,h)
    
    elif not face:
        return face, frame, 0, (0,0,0,0)
    
    else:
        return frame

def display():
    video_capture = cv2.VideoCapture(0)
    currentX=1900
    currentY=0
    for i in range(1):
        avgXData=[]
        avgYData=[]
        i=0
        while i!=3:
            face, frame, area, (x,y,w,h) = findFaces(video_capture)
            #os.system('pigs s 4 ' + str((2420/500) * x))
            print(x,y)
            if face:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                avgXData.append(x)
                avgYData.append(y)
            else:
                i-=1;
            cv2.imshow('Video', frame)
            i+=1;
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        avgXData.sort()
        avgX=int(avgXData[1])
        avgY=int(avgYData[1])
        print("avg: "+str(avgX))
        if avgX>225:
            print("hi")
            dist = avgX-225
            distFact = int(dist*((2420-550)/500))
            currentX+=distFact
            print("dist"+str(currentX))
            if currentX>2420:
                currentX=2420
            os.system('pigs s 4 ' + str(currentX))
          
                   
        if avgX<225:
            dist = 225-avgX
            distFact = int(dist*((2420-550)/500))
            currentX-=distFact
            print("dist"+str(currentX))
            if currentX<560:
                currentX=560
            os.system('pigs s 4 ' + str(currentX))
            
                
        print(avgX, avgY)
        #print("j "+str(int((avgXData*1489)/225)))
        #os.system('pigs s 4 ' + str(int((avgXData*1489)/225)) )
        
    video_capture.release()

while True:
    os.system('pigs s 4 1900')
    display()

