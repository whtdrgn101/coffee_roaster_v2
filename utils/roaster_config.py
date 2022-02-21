import json

class RoasterConfig:

    MOTOR_FORWARD_PIN = 0
    MOTOR_REVERSE_PIN = 0
    MOTOR_PWM_PIN = 0
    BLOWER_RELAY_PIN = 0
    HEATING_ELEMENT_PIN = 0
    COOL_TIME_SEC = 0

    def __init__(self, config_file):
        #load file
        with open(config_file) as f:
            config = json.load(f)

        #parse file
        self.MOTOR_FORWARD_PIN = config["MOTOR_FORWARD_PIN"]
        self.MOTOR_REVERSE_PIN = config["MOTOR_REVERSE_PIN"]
        self.MOTOR_PWM_PIN = config["MOTOR_PWM_PIN"]
        self.BLOWER_RELAY_PIN = config["BLOWER_RELAY_PIN"]
        self.HEATING_ELEMENT_PIN = config["HEATING_ELEMENT_PIN"]
        self.COOL_TIME_SEC = float(config["COOL_TIME_SEC"])
