import RPi.GPIO as GPIO

class Motor:
    def __init__(self, motor_pin_forward, motor_pin_backward):
        self.motor_pin_forward = motor_pin_forward
        self.motor_pin_backward = motor_pin_backward
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin_forward, GPIO.OUT)
        GPIO.setup(self.motor_pin_backward, GPIO.OUT)
        
        self.pwm_forward = GPIO.PWM(self.motor_pin_forward, 100)
        self.pwm_backward = GPIO.PWM(self.motor_pin_backward, 100)
        
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
    
    def move_forward(self, speed):
        self.pwm_forward.ChangeDutyCycle(speed)
        self.pwm_backward.ChangeDutyCycle(0)
        
    def move_backward(self, speed):
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(speed)
        
    def stop(self):
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)
        
    def cleanup(self):
        GPIO.cleanup()
