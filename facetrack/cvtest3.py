from multiprocessing import Process, Queue
import time
import cv2

#size of the video
width = 320
height = 240

capture = cv2.VideoCapture(0)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

#frontalFace = cv2.CascadeClassifier("face.xml")
frontalFace = cv2.CascadeClassifier("lbp_face.xml")

face = [0,0,0,0]
Cface = [0,0]

cv2.cv.NamedWindow("video", cv2.cv.CV_WINDOW_AUTOSIZE)

try:
    
    while True:
        
        faceFound = False

        if not faceFound:
            aframe = capture.grab()
            aframe = capture.grab()
            aframe = capture.grab()
            aframe = capture.grab()
            aframe = capture.read()[1]

            #fface = frontalFace.detectMultiScale(aframe, 1.3, 4, (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH), (60, 60))
            fface = frontalFace.detectMultiScale(aframe, 1.1, 2, 0, (60, 60))
            if fface != ():
                for f in fface:
                    faceFound = True
                    face = f

        if not faceFound:
            face = [0,0,0,0]                
                    
        x,y,w,h = face
        Cface = [(w/2+x), (h/2+y)]
        print str(Cface[0]) + "," + str(Cface[1])
           
        cv2.cv.Rectangle(cv2.cv.fromarray(aframe), (x,y), (x+w, y+h), cv2.cv.RGB(255, 0, 0), 3, 8, 0)
        cv2.imshow("video", aframe)
        cv2.waitKey(1)
            
 
except KeyboardInterrupt:
    pass

finally:
    capture.release()
    cv2.cv.DestroyWindow("video")
    
    
