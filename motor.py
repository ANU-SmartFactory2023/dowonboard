import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self, enable_pin, input1_pin, input2_pin):
        # DC 모터 초기화
        self.enable_pin = enable_pin
        self.input1_pin = input1_pin
        self.input2_pin = input2_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.input1_pin, GPIO.OUT)
        GPIO.setup(self.input2_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.enable_pin, 1000)  # 주파수 1000Hz로 PWM 설정
        self.pwm.start(0)  # 초기 듀티 사이클은 0으로 설정

    def set_speed(self, speed):
        # 속도 설정
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        duty_cycle = speed * 1.1 + 10
        self.pwm.ChangeDutyCycle(duty_cycle)

    def forward(self):
        # 정방향 회전
        GPIO.output(self.input1_pin, GPIO.HIGH)
        GPIO.output(self.input2_pin, GPIO.LOW)

    def backward(self):
        # 역방향 회전
        GPIO.output(self.input1_pin, GPIO.LOW)
        GPIO.output(self.input2_pin, GPIO.HIGH)

    def stop(self):
        # 정지
        GPIO.output(self.input1_pin, GPIO.LOW)
        GPIO.output(self.input2_pin, GPIO.LOW)

    def cleanup(self):
        # 정리
        self.pwm.stop()
        GPIO.cleanup()

class ServoMotor:
    def __init__(self, pin):
        # 서보 모터 초기화
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, 50)  # 주파수 50Hz로 PWM 설정
        self.pwm.start(0)  # 초기 듀티 사이클은 0으로 설정

    def set_angle(self, angle):
        # 각도 설정
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        duty_cycle = (angle / 18.0) + 2.5
        self.pwm.ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        # 정리
        self.pwm.stop()
        GPIO.cleanup()
