import RPi.GPIO as GPIO 

class RelayController:

    POWER_CONTROL_PIN = 0
    IS_ON = False

    def __init__(self, control_pin):
        
        self.POWER_CONTROL_PIN = control_pin

        GPIO.setup(self.POWER_CONTROL_PIN, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.POWER_CONTROL_PIN, GPIO.HIGH) 
        self.IS_ON = True

    def power_off(self):
        GPIO.output(self.POWER_CONTROL_PIN, GPIO.LOW) 
        self.IS_ON = False