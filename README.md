# Coffee Roaster Project

## Summary
This project contains the microcontroller code to drive a DIY coffee roaster project.  The main goal was to write code that is easy to understand, maintain, and allows for a degree of configurability for sebsequent versions of the coffee roaster as improvements are made.

## File Organization

### main.py
This file is the main driver of the microcontroller and the User-Interface that controls the roaster and displays current status.  It uses the classes in the utils/ folder to control the components of the coffee roaster and the Kivy UI framework as well.

### coffee.kv
This file is the main UI layout code for the Kivy UI framework used for the main roaster code.  

### config.json
This file contains all of the configuration data for the microcontroller.  It includes GPIO ping specifications as well as timing values and other default settings.

### utils folder
Each component in the coffee roaster that needs controlled by microcontroller becomes a class within this folder.  Any interaction between the components is controlled via the main roaster.py module so no classes reference each other excepting where there is an additional driver file for specific components like the "LCD Panel"

## References

* [Kivy UI Framework](https://kivy.org/doc/stable/)
* [MAX31856 Thermocouple Control](https://learn.adafruit.com/adafruit-max31856-thermocouple-amplifier/python-circuitpython)
* [L298 Motor Controller](https://www.bluetin.io/python/gpio-pwm-raspberry-pi-h-bridge-dc-motor-control/)
* [Project Documentation](https://docs.google.com/document/d/1oHwVflQFp4IHgEQ_DVCQFsYltsm2OGass9z3PHarOX0/edit?usp=sharing)
* [AC Relay Infomation](https://robotdyn.com/relay-module-2-relays-5v.html