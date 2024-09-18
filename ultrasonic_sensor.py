import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        # GPIO 핀 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
    
    def get_distance(self):
        """초음파 센서를 이용한 거리 측정"""
        # 트리거 핀에 신호 보내기
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)  # 10us 동안 신호 전송
        GPIO.output(self.trig_pin, False)
        
        # Echo 핀에서 신호 수신 시간 측정
        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        # 시간 차이로부터 거리 계산 (소리 속도: 34300 cm/s)
        elapsed_time = stop_time - start_time
        distance = (elapsed_time * 34300) / 2  # 왕복 거리이므로 2로 나눔

        return distance
    
    def cleanup(self):
        GPIO.cleanup()
