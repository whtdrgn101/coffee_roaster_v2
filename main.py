##########################################################################################################################
# Main UI and driving program for the coffee roaster.  This version replaces the legacy version that relied on a two-row
# LCD panel to display current temp and running state but assumes the hardware presence of an AC relay, DC relay for a 
# blower-motor, a DC Motor controller (variable speed), and a digital thermometer.  
##########################################################################################################################
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
from utils import MotorController, RelayController, RoasterConfig, ThermocoupleController
import RPi.GPIO as GPIO

class RootWidget(TabbedPanel):
    recorded_temp = 0.0
    init_hardware = False
    motor_on = False
    heating_element_on = False
    running = False
    running_event = None
    heating = None
    drive_motor = None
    therm = None
    config = None 
        
    # Event Handlers    
    def _handle_start_roaster_button_click(self):
        self.start_roaster()
    
    def _handle_stop_roaster_button_click(self):
        self.stop_roaster()

    def _handle_cool_down_button_click(self):
        self.cool_roaster()

    #Class Methods
    def get_target_temp(self):
        return self.ids.slider_target_temp.value

    def get_motor_speed(self):
        return self.ids.slider_motor_speed.value / 100

    def _update_ui_state(self):
        self.ids.temp_reading_label.text = f"{self.recorded_temp:0.1f}"
        self.ids.start_roaster_button.disabled = self.running
        self.ids.stop_roaster_button.disabled = not self.running
        self.ids.cool_down_button.disabled = not self.running
        self.ids.roaster_state_label.text = "Heating Element: {0} | Motor Running: {1}".format(['OFF',' ON'][self.heating.IS_ON],['OFF', ' ON'][self.drive_motor.IS_MOVING])
    
    def start_roaster(self):
         # Init hardware first time
        if self.init_hardware == False:
            self.init()
        self.running = True
        self.drive_motor.drive_motor(self.get_motor_speed())
        self.running_event = Clock.schedule_interval(self.run_roaster_callback, 1/15)
        self._update_ui_state()
        
    def stop_roaster(self):
        self.running = False
        self.running_event.cancel()
        self.heating.power_off()
        self.drive_motor.stop_motor()
        self._update_ui_state()

    def cool_roaster(self):
        self.running = False
        self.running_event.cancel()
        self.heating.power_off()
        self.drive_motor.drive_motor(self.get_motor_speed())
        self._update_ui_state()
    
    def run_roaster_callback(self, dt):

        # TEMP & HEATING STATE
        self.recorded_temp = self.therm.read_temp_f()
        t_temp = self.get_target_temp()

        if self.recorded_temp > t_temp and self.heating.IS_ON == True:
            self.heating.power_off()
        elif self.recorded_temp < t_temp and self.heating.IS_ON == False:
            self.heating.power_on()

        # MOTOR STATE
        if self.drive_motor.IS_MOVING == False:
            self.drive_motor.drive_motor()

        self._update_ui_state()

    def init(self):
        self.init_hardware = True
        self.config = RoasterConfig('config.json')
        self.heating = RelayController(self.config.HEATING_ELEMENT_PIN)
        self.drive_motor = MotorController("drive_motor", self.config.MOTOR_FORWARD_PIN, self.config.MOTOR_REVERSE_PIN, self.config.MOTOR_PWM_PIN)
        self.blower_motor = RelayController(self.config.BLOWER_RELAY_PIN)
        self.therm = ThermocoupleController()

class CoffeeApp(App):
    
    WINDOW_HEIGHT = 768
    WINDOW_WIDTH = 1200
    APP_TITLE = "Coffee Roaster Control Interface" 

    def build(self):
        self.title = self.APP_TITLE
        Window.title = self.APP_TITLE
        Window.size = (self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        Window.minimum_height = self.WINDOW_HEIGHT
        Window.minimum_width = self.WINDOW_WIDTH
        return RootWidget()      

if __name__ == "__main__":
    CoffeeApp().run()
    GPIO.cleanup()