import RPi.GPIO as GPIO

class Motor:
    def __init__(self, left_motor_pins, right_motor_pins):
        self.left_motor_pin_forward, self.left_motor_pin_backward = left_motor_pins
        self.right_motor_pin_forward, self.right_motor_pin_backward = right_motor_pins
        
        # GPIO 핀 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_motor_pin_forward, GPIO.OUT)
        GPIO.setup(self.left_motor_pin_backward, GPIO.OUT)
        GPIO.setup(self.right_motor_pin_forward, GPIO.OUT)
        GPIO.setup(self.right_motor_pin_backward, GPIO.OUT)
        
        self.left_pwm_forward = GPIO.PWM(self.left_motor_pin_forward, 100)
        self.left_pwm_backward = GPIO.PWM(self.left_motor_pin_backward, 100)
        self.right_pwm_forward = GPIO.PWM(self.right_motor_pin_forward, 100)
        self.right_pwm_backward = GPIO.PWM(self.right_motor_pin_backward, 100)

        self.left_pwm_forward.start(0)
        self.left_pwm_backward.start(0)
        self.right_pwm_forward.start(0)
        self.right_pwm_backward.start(0)

    def move_forward(self, speed):
        self.left_pwm_forward.ChangeDutyCycle(speed)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(speed)
        self.right_pwm_backward.ChangeDutyCycle(0)
    
    def move_backward(self, speed):
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.left_pwm_backward.ChangeDutyCycle(speed)
        self.right_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(speed)

    def turn_left(self, speed):
        # 왼쪽 모터를 천천히 돌리고, 오른쪽 모터는 빠르게 돌림
        self.left_pwm_forward.ChangeDutyCycle(speed / 2)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(speed)
        self.right_pwm_backward.ChangeDutyCycle(0)
    
    def turn_right(self, speed):
        # 오른쪽 모터를 천천히 돌리고, 왼쪽 모터는 빠르게 돌림
        self.left_pwm_forward.ChangeDutyCycle(speed)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(speed / 2)
        self.right_pwm_backward.ChangeDutyCycle(0)
    
    def stop(self):
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(0)
    
    def cleanup(self):
        GPIO.cleanup()
