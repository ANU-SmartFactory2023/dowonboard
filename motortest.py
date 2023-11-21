import RPi.GPIO as GPIO
import time
from motor import ServoMotor

try:    
    servo_motor = ServoMotor(pin=17)

    servo_motor.set_angle(90)  # 90도 각도로 서보 모터 동작    
    time.sleep(1)
    print("motor : 90")
    servo_motor.set_angle(0)
    time.sleep(1)
    print("motor : 0")

except KeyboardInterrupt:
    # 사용자가 프로그램을 강제로 종료할 때
    print("프로그램 종료")
finally:
    # 정리   
    servo_motor.cleanup()
