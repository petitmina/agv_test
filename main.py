from motor import Motor
from ultrasonic_sensor import UltrasonicSensor  # 초음파 센서 모듈 추가
import time
import RPi.GPIO as GPIO
import cv2
from image_processing import detect_traffic_light, detect_person

class AutonomousCar:
    def __init__(self):
        self.motor = Motor(left_motor_pins=(18, 23), right_motor_pins=(24, 25))
        self.ultrasonic_sensor = UltrasonicSensor(trig_pin=17, echo_pin=27)  # 초음파 센서 초기화
        self.camera = cv2.VideoCapture(0)  # 0번 카메라 사용 (기본 카메라)

    def check_ultrasonic_for_obstacles(self):
        """초음파 센서를 이용해 장애물 감지"""
        distance = self.ultrasonic_sensor.get_distance()
        if distance < 50:  # 50cm 이하에 장애물이 있을 경우
            print(f"Obstacle detected at {distance:.2f} cm!")
            return True  # 장애물 있음
        else:
            print(f"Distance is clear: {distance:.2f} cm")
            return False  # 장애물 없음

    def start(self):
        try:
            while True:
                # 카메라로 이미지 입력받기 (실제 사용 시 카메라 모듈로 대체)
                # image = cv2.imread('input_image.jpg')  # 테스트용 예시 코드
                
                # 카메라에서 프레임(이미지) 받기
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to capture image from camera")
                    break

                # 신호등 및 사람 인식
                traffic_light_status = detect_traffic_light(frame)
                person_detected = detect_person(frame)
                
                # 초음파 센서로 장애물 감지
                obstacle_detected = self.check_ultrasonic_for_obstacles()

                # 신호등 색상, 장애물, 사람 상태에 따른 모터 제어
                if traffic_light_status == "green" and not obstacle_detected and not person_detected:
                    print("Green light and clear path: Moving forward...")
                    self.motor.move_forward(50)  # 전진
                elif traffic_light_status == "yellow":
                    print("Yellow light: Turning left...")
                    self.motor.turn_left(50)  # 좌회전
                elif traffic_light_status == "blue":
                    print("Blue light: Turning right...")
                    self.motor.turn_right(50)  # 우회전
                elif traffic_light_status == "red" or person_detected or obstacle_detected:
                    print("Red light, person detected, or obstacle: Stopping...")
                    self.motor.stop()  # 멈춤
                elif traffic_light_status == "reverse":
                    print("Reverse signal detected: Moving backward...")
                    self.motor.move_backward(50)  # 후진
                else:
                    print("No clear traffic light signal, staying still.")
                    self.motor.stop()  # 대기 (멈춤)

                time.sleep(1)

        except KeyboardInterrupt:
            print("Stopping the car...")
        finally:
            self.camera.release()  # 카메라 해제
            self.ultrasonic_sensor.cleanup()  # GPIO 설정 정리
            self.motor.cleanup()

if __name__ == "__main__":
    car = AutonomousCar()
    car.start()
