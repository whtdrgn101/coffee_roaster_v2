import RPi.GPIO as GPIO

class MotorController:

    MOTOR_FORWARD = 0
    MOTOR_REVERSE = 0
    MOTOR_PWM = 0
    MOTOR_SPEED = 0.5
    my_name = ""
    IS_MOVING = False
    my_motor_speed = None

    def __init__(self, name, motor_forward_pin, motor_reverse_pin, motor_pwm_pin, motor_speed = 0.5):
    
        self.my_name = name
        self.MOTOR_FORWARD = motor_forward_pin
        self.MOTOR_REVERSE = motor_reverse_pin
        self.MOTOR_PWM = motor_pwm_pin
        self.MOTOR_SPEED = motor_speed

        GPIO.setup(self.MOTOR_FORWARD, GPIO.OUT)
        GPIO.setup(self.MOTOR_REVERSE, GPIO.OUT)
        GPIO.setup(self.MOTOR_PWM, GPIO.OUT)
        self.my_motor_speed = GPIO.PWM(self.MOTOR_PWM, 1000)
        self.my_motor_speed.start(0)

    def drive_motor(self, direction='f'):
        
        self.stop_motor()

        if direction == 'f':
            GPIO.output(self.MOTOR_FORWARD, GPIO.HIGH)
        elif direction == 'r':
            GPIO.output(self.MOTOR_REVERSE, GPIO.HIGH)
        
        self.my_motor_speed.ChangeDutyCycle(self.MOTOR_SPEED)
        
        self.IS_MOVING = True


    def stop_motor(self):
        GPIO.output(self.MOTOR_FORWARD, GPIO.LOW)
        GPIO.output(self.MOTOR_REVERSE, GPIO.LOW)
        self.my_motor_speed.ChangeDutyCycle(0)
        self.IS_MOVING = False