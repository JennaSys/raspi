from RPIO import PWM
import time

pPan = 23
pTilt = 24

pan_minL = 1100
pan_maxL = 2300
tilt_minL = 800
tilt_maxL = 2000
pan_minR = 800
pan_maxR = 1800
tilt_minR = 600
tilt_maxR = 2300

pan_centerL = 1700
tilt_centerL = 1400
pan_centerR = 1300
tilt_centerR = 160
pan_center = ((pan_max - pan_min) / 2) + pan_min
tilt_center = ((tilt_max - tilt_min) / 2) + tilt_min

servo = PWM.Servo()

servo.set_servo(pPan, pan_center)
servo.set_servo(pTilt, tilt_center)
time.sleep(2)

servo.set_servo(pPan, pan_min)
time.sleep(2)

servo.set_servo(pPan, pan_max)
time.sleep(2)

servo.set_servo(pPan, pan_center)
servo.set_servo(pTilt, tilt_min)
time.sleep(2)

servo.set_servo(pTilt, tilt_max)
time.sleep(2)

servo.set_servo(pTilt, tilt_center)
time.sleep(2)

servo.stop_servo(pPan)
servo.stop_servo(pTilt)

PWM.cleanup()
