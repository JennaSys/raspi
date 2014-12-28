from RPIO import PWM
import time

pPan = 23
pTilt = 24

servo_min = 580
servo_max = 2460
servo_center = ((servo_max - servo_min) / 2) + servo_min

servo = PWM.Servo()

servo.set_servo(pPan, servo_center)
servo.set_servo(pTilt, servo_center)
time.sleep(2)

servo.set_servo(pPan, servo_min)
time.sleep(2)

servo.set_servo(pPan, servo_max)
time.sleep(2)

servo.set_servo(pPan, servo_center)
servo.set_servo(pTilt, servo_min)
time.sleep(2)

servo.set_servo(pTilt, servo_max)
time.sleep(2)

servo.set_servo(pTilt, servo_center)
time.sleep(2)

servo.stop_servo(pPan)
servo.stop_servo(pTilt)

PWM.cleanup()



