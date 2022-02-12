from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from utils import MotorController, RelayController, RoasterConfig, ThermocoupleController
import RPi.GPIO as GPIO

class RootWidget(BoxLayout):
    target_temp = 300
    recorded_temp = 0
    init_hardware = False
    motor_on = False
    heating_element_on = False
    running = False
    running_event = None
    heating = None
    drive_motor = None
    therm = None
    config = None 
        
    #Event Handlers
    def _handle_temp_up_l_button_click(self):
        self.adjust_temp(5)
    
    def _handle_temp_up_button_click(self):
        self.adjust_temp(1)

    def _handle_temp_down_button_click(self):
        self.adjust_temp(-1)

    def _handle_temp_down_l_button_click(self):
        self.adjust_temp(-5)
    
    def _handle_start_roaster_button_click(self):
        self.start_roaster()
    
    def _handle_stop_roaster_button_click(self):
        self.stop_roaster()

    #Class Methods
    def _update_ui_state(self):
        self.ids.target_temp_label.text = str(self.target_temp)
        self.ids.start_roaster_button.disabled = self.running
        self.ids.stop_roaster_button.disabled = not self.running
        self.ids.temp_down_large_button.disabled = not self.running
        self.ids.temp_down_small_button.disabled = not self.running
        self.ids.temp_up_large_button.disabled = not self.running
        self.ids.temp_up_small_button.disabled = not self.running
        self.ids.roaster_state_label.text = f"Heating Element: {self.heating.IS_ON} | Motor Running: {self.drive_motor.IS_MOVING}"
    
    def start_roaster(self):
         # Init hardware first time
        if self.init_hardware == False:
            self.init()
        self.running = True
        self.running_event = Clock.schedule_interval(self.run_roaster, 1/30)
        self._update_ui_state()
        
    def stop_roaster(self):
        self.running = False
        self.running_event.cancel()
        self.heating.power_off()
        self.drive_motor.stop_motor()

        self._update_ui_state()      

    def adjust_temp(self, delta: int):
        self.target_temp = self.target_temp + delta
        self._update_ui_state()
    
    def run_roaster(self, dt):

        # TEMP & HEATING STATE
        #self.recorded_temp = therm.read_temp_f()

        if self.recorded_temp > self.target_temp and self.heating.IS_ON == True:
            self.heating.power_off()
        elif self.recorded_temp < self.target_temp and self.heating.IS_ON == False:
            self.heating.power_on()

        # MOTOR STATE
        if self.drive_motor.IS_MOVING == False:
            self.drive_motor.drive_motor()

        self._update_ui_state()

    def init(self):
        self.init_hardware = True
        self.config = RoasterConfig('config.json')
        self.heating = RelayController(self.config.HEATING_ELEMENT_PIN)
        self.drive_motor = MotorController("drive_motor", self.config.MOTOR_FORWARD_PIN, self.config.MOTOR_REVERSE_PIN, self.config.MOTOR_PWM_PIN, self.config.MOTOR_SPEED)
        self.blower_motor = RelayController(self.config.BLOWER_RELAY_PIN)
        #self.therm = ThermocoupleController()

class CoffeeApp(App):
    
    def build(self):
        Window.size = (1200,768)
        self.title = "Coffee Roaster Control Interface"
        return RootWidget()      

if __name__ == "__main__":
    CoffeeApp().run()
    GPIO.cleanup()