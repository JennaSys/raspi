#!/usr/bin/python

# Core code borrowed from
# http://instructables.com/id/Pan-Tilt-face-tracking-with-the-raspberry-pi
# and various other places

from eyepi2 import EyePi
import multiprocessing
from multiprocessing import Process, Queue, Manager
import time
import cv2
import logging


log_format = '%(levelname)s | %(asctime)-15s | %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)


#Scale Factors
scaleX = 0.7
scaleY = 1.0
offsetX = 26
offsetY = -20



#size of the video
cam_width = 320
cam_height = 240

capture = cv2.VideoCapture(0)               # Get ready to start getting images from the webcam
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, cam_width)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, cam_height)

frontalface = cv2.CascadeClassifier("lbpcascade_frontalface.xml")       # frontal face pattern detection

face = [0,0,0,0]    # This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]       # Center of the face: a point calculated from the above variable
            
eyes = EyePi()
eyes.start()

#init servos to center
eyes.look_forward()


class EyePiProxy(multiprocessing.managers.BaseProxy):
	def set_pan(self, pan_pct): 
	    return self._callmethod('set_pan', [pan_pct])
	def set_tilt(self, tilt_pct):
	    return self._callmethod('set_tilt', [tilt_pct])
	def inPanic():	
	    return self._callmethod('inPanic', [])

class EyePiManager(multiprocessing.managers.BaseManager):
    pass
    
manager = EyePiManager()
manager.register('setup_eyepi', eyes, proxytype=EyePiProxy, exposed = ('set_pan', 'set_tilt', 'inPanic'))
manager.start()
eyepi_proxy = manager.setup_eyepi()		


ServoPanCP = Queue()    # Servo zero current position, sent by subprocess and read by main process
ServoTiltCP = Queue()   # Servo one current position, sent by subprocess and read by main process
ServoPanDP = Queue()    # Servo zero desired position, sent by main and read by subprocess
ServoTiltDP = Queue()   # Servo one desired position, sent by main and read by subprocess
ServoPanS = Queue() # Servo zero speed, sent by main and read by subprocess
ServoTiltS = Queue()    # Servo one speed, sent by main and read by subprocess

cv2.cv.NamedWindow("video", cv2.cv.CV_WINDOW_AUTOSIZE)


def P0(eyepi_proxy):   # Process 0 controlls Pan servo
    speed = .1      # Here we set some defaults:
    _ServoPanCP = 1     # by making the current position and desired position unequal,-
    _ServoPanDP = 0     #   we can be sure we know where the servo really is. (or will be soon)

    while True:
        time.sleep(speed)
        if ServoPanCP.empty():          # Constantly update ServoPanCP in case the main process needs-
            ServoPanCP.put(_ServoPanCP)     #   to read it
        if not ServoPanDP.empty():      # Constantly read read ServoPanDP in case the main process-
            _ServoPanDP = ServoPanDP.get()  #   has updated it
        if not ServoPanS.empty():           # Constantly read read ServoPanS in case the main process-
            _ServoPanS = ServoPanS.get()    #   has updated it, the higher the speed value, the shorter-
            speed = .1 / _ServoPanS     #   the wait between loops will be, so the servo moves faster
        if _ServoPanCP == _ServoPanDP:          # if all is good,-
            _ServoPanS = 1              # slow the speed; no need to eat CPU just waiting
        else:                           # if ServoPanCP != ServoPanDP
            _ServoPanCP = _ServoPanDP                       # incriment ServoPanCP down by one
            ServoPanCP.put(_ServoPanCP)                 # move the servo that little bit
            eyepi_proxy.set_pan(_ServoPanCP)

            if not ServoPanCP.empty():              # throw away the old ServoPanCP value,-
                trash = ServoPanCP.get()                #   it's no longer relevent
            

def P1(eyepi_proxy):   # Process 1 controlls Tilt servo using same logic as above
    speed = .1
    _ServoTiltCP = 1
    _ServoTiltDP = 0

    while True:
        time.sleep(speed)
        if ServoTiltCP.empty():
            ServoTiltCP.put(_ServoTiltCP)
        if not ServoTiltDP.empty():
            _ServoTiltDP = ServoTiltDP.get()
        if not ServoTiltS.empty():
            _ServoTiltS = ServoTiltS.get()
            speed = .1 / _ServoTiltS
        if _ServoTiltCP == _ServoTiltDP:
            _ServoTiltS = 1
        else:
            _ServoTiltCP =  _ServoTiltDP
            ServoTiltCP.put(_ServoTiltCP)
            eyepi_proxy.set_tilt(_ServoTiltCP)

            if not ServoTiltCP.empty():
                trash = ServoTiltCP.get()



Process(target=P0, args=(eyepi_proxy)).start() # Start the subprocesses
Process(target=P1, args=(eyepi_proxy)).start() #
time.sleep(1)               # Wait for them to start

#====================================================================================================

def pan(position, speed):       # To move right, we are provided a distance to move and a speed to move.
    global _ServoPanCP          # We Global it so  everyone is on the same page about where the servo is...
    if not ServoPanCP.empty():      # Read it's current position given by the subprocess(if it's avalible)-
        _ServoPanCP = ServoPanCP.get()  #   and set the main process global variable.
    _ServoPanDP = position              # The desired position is the current position + the distance to move.
    if _ServoPanDP > 100:       # But if you are told to move further than the servo is built go...
        _ServoPanDP = 100       # Only move AS far as the servo is built to go.
    elif _ServoPanDP < -100:
        _ServoPanDP = -100
    ServoPanDP.put(_ServoPanDP)         # Send the new desired position to the subprocess
    ServoPanS.put(speed)            # Send the new speed to the subprocess
    return;


def tilt(position, speed):          # Same logic as above
    global _ServoTiltCP
    if not ServoTiltCP.empty():
        _ServoTiltCP = ServoTiltCP.get()
    _ServoTiltDP = position
    if _ServoTiltDP > 100:
        _ServoTiltDP = 100
    elif _ServoTiltDP < -100:
        _ServoTiltDP = -100
    ServoTiltDP.put(_ServoTiltDP)
    ServoTiltS.put(speed)
    return;



#============================================================================================================

try:
    currPan = 0
    currTilt = 0
    while True:

        faceFound = False   # This variable is set to true if, on THIS loop a face has already been found

        aframe = capture.grab() # there seems to be an issue in OpenCV or V4L or my webcam-
        aframe = capture.grab() #   driver, I'm not sure which, but if you wait too long,
        aframe = capture.grab() #   the webcam consistantly gets exactly five frames behind-
        aframe = capture.grab() #   realtime. So we just grab a frame five times to ensure-
        aframe = capture.read()[1]  #   we have the most up-to-date image.
        fface = frontalface.detectMultiScale(aframe, 1.1, 2, 0, (40,40))
        if fface != ():         # if we found a frontal face...
            for f in fface:     # f in fface is an array with a rectangle representing a face
                faceFound = True
                face = f


        if not faceFound:       # if no face was found...-
            face = [0,0,0,0]    # so that it doesn't think the face is still where it was last loop
            
            #reset eyes
            currPan = 0
            currTilt = 0
            face_x = 0
            face_y = 0
            if not eyes.inPanic():
                eyes.look_forward()
    
        x,y,w,h = face        
        Cface = [(w/2+x),(h/2+y)]   # we are given an x,y corner point and a width and height, we need the center
        
        print str(Cface[0]) + "," + str(Cface[1])
           

        cv2.cv.Rectangle(cv2.cv.fromarray(aframe), (x,y), (x+w, y+h), cv2.cv.RGB(255, 0, 0), 3, 8, 0)
        cv2.imshow("video", aframe)
        cv2.waitKey(1)

        if faceFound:
            #calc pan
            face_x = -int(((Cface[0] - (cam_width / 2.0)) / (cam_width / 2.0)) * 100)
            face_x = int((face_x + offsetX) * scaleX)
            if abs(face_x - currPan) < 4:
                pass
            elif abs(face_x - currPan) < 10:
                pan(face_x, 1)
            elif abs(face_x - currPan) < 30:
                pan(face_x, 2)
            else:
                pan(face_x, 6)
            currPan = face_x
            
            #calc tilt
            face_y = int(((Cface[1] - (cam_height / 2.0)) / (cam_height / 2.0)) * 100)
            face_y = int((face_y + offsetY) * scaleY)
            if abs(face_y - currTilt) < 4:
                pass
            elif abs(face_y - currTilt) < 10:
                tilt(face_y, 1)
            elif abs(face_y - currTilt) < 30:
                tilt(face_y, 2)
            else:
                tilt(face_y, 6)
            currTilt = face_y

            print 'Pan: {0}   Tilt: {1}'.format(face_x, face_y)

except KeyboardInterrupt:
    pass
    
finally:
    eyes.stop()
    capture.release()
    cv2.cv.DestroyWindow("video")
