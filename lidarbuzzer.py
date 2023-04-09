from rplidar import RPLidar
import RPi.GPIO as GPIO
from time import sleep
import signal
import sys

lidar = RPLidar('/dev/ttyUSB0')

threshold = 2000 # threshold for notification in mm
buzzer_centers = [
    260,
    285,
    310,
    335,
    0,
    25,
    50,
    75,
    100
]


#--------------------------------start of buzzer set up -----------------------------------#
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)

buzzer1 = 18
buzzer2 = 17
buzzer3 = 27
buzzer4 = 22
buzzer5 = 24
buzzer6 = 12
buzzer7 = 13
buzzer8 = 19

GPIO.setup(buzzer1,GPIO.OUT)
GPIO.setup(buzzer2,GPIO.OUT)
GPIO.setup(buzzer3,GPIO.OUT)
GPIO.setup(buzzer4,GPIO.OUT)
GPIO.setup(buzzer5,GPIO.OUT)
GPIO.setup(buzzer6,GPIO.OUT)
GPIO.setup(buzzer7,GPIO.OUT)
GPIO.setup(buzzer8,GPIO.OUT)
pwm1 = GPIO.PWM(buzzer1, 1)
pwm2 = GPIO.PWM(buzzer2, 1)
pwm3 = GPIO.PWM(buzzer3, 1)
pwm4 = GPIO.PWM(buzzer4, 1)
pwm5 = GPIO.PWM(buzzer5, 1)
pwm6 = GPIO.PWM(buzzer6, 1)
pwm7 = GPIO.PWM(buzzer7, 1)
pwm8 = GPIO.PWM(buzzer8, 1)
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
pwm5.start(0)
pwm6.start(0)
pwm7.start(0)
pwm8.start(0)

allPWM = [pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7, pwm8]
allBuzzers = [buzzer1, buzzer2, buzzer3, buzzer4, buzzer5, buzzer6, buzzer7, buzzer8]
#-------------------------------- end of buzzer set up -----------------------------------#

#frequency of beeps based on distance, and which buzzer to beep.
def beep (n, pwm, buzzer):
        pwm.ChangeFrequency((1/n)*3000)
        pwm.ChangeDutyCycle(50)
        print(buzzer)


#theoretically turns the other buzzers off. (ie only keep the buzzer given in parameter on)
def turnOtherBuzzersOf(pwm):
        for p in allPWM:
                if p != pwm:
                        p.ChangeDutyCycle(0)

        return

def turnAllOff():
        for p in allPWM:
                p.ChangeDutyCycle(0)

def buzzer_powers(data):
    #find the index position that contains the minimum distance

        min = 1000
        min_angle =1000
        t = (0, 0, 0)
        for tuple in data:
                dis = tuple[2]
                angle = tuple[1]
                if dis > 0 and dis < 4000 and (angle < 100 or angle > 260):
                        if dis < min:
                                min = dis
                                min_angle = angle
                                t = tuple
        print(t)
    # buzz the buzzer that the angle is at.
        if min_angle >= 260 and min_angle < 285:
                turnOtherBuzzersOf(pwm1)
                beep(min, pwm1, buzzer1)
        elif min_angle >= 285 and min_angle < 310:
                turnOtherBuzzersOf(pwm2)
                beep(min, pwm2, buzzer2)
        elif min_angle >= 310 and min_angle < 335:
                turnOtherBuzzersOf(pwm3)
                beep(min, pwm3, buzzer3)
        elif min_angle >= 335 and min_angle < 360:
                turnOtherBuzzersOf(pwm4)
                beep(min, pwm4, buzzer4)
        elif min_angle >= 0 and min_angle < 25:
                turnOtherBuzzersOf(pwm5)
                beep(min, pwm5, buzzer5)
        elif min_angle >= 25 and min_angle < 50:
                turnOtherBuzzersOf(pwm6)
                beep(min, pwm6, buzzer6)
        elif min_angle >= 50 and min_angle < 75:
                turnOtherBuzzersOf(pwm7)
                beep(min, pwm7, buzzer7)
        elif min_angle >= 75 and min_angle < 100:
                turnOtherBuzzersOf(pwm8)
                beep(min, pwm8,buzzer8)
        else:
                turnAllOff()

def define_objects():
        return

def signal_handler(sig, frame):
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
#info = lidar.get_info()
#print(info)

#health = lidar.get_health()
#print(health)

for scan in lidar.iter_scans():
        try:

                #if scan[2] > 100 and scan[2] < 260:
                        #continue
                #print(scan[2])  angle
                #print(scan[3]) dist (mm)

                #angle_lst.append(scan[1])
                #dist_lst.append(scan[2])
                buzzer_powers(scan)


        except(RPLidarException):
                lidar.clear_input()
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
