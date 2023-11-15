import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
trig_pin = 23
echo_pin = 24

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

def get_distance():
    # 초음파 발신cd
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    # 초음파 수신
    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()

    # 초음파의 이동 시간을 거리로 변환
    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 34300 / 2  # 음속: 343m/s (소리의 속도)

    return distance

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            distance = get_distance()
            print(f"Distance: {distance:.2f} cm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        cleanup()
