import board
import busio
import digitalio
import adafruit_max31856

class ThermocoupleController:

    my_spi = None
    my_cs = None
    my_thermocouple = None

    def __init__ (self):
        self.my_spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.my_cs = digitalio.DigitalInOut(board.D5)
        self.my_cs.direction = digitalio.Direction.OUTPUT
        self.my_thermocouple = adafruit_max31856.MAX31856(self.my_spi, self.my_cs)

    def read_temp_f(self):
        return self.read_temp_c() * (9/5) + 32

    def read_temp_c(self):
        return self.my_thermocouple.temperature 