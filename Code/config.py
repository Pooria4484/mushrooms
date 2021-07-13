from machine import Pin
heater_valve=Pin(21,Pin.OUT)
heater_fan=Pin(19,Pin.OUT)
mist=Pin(19,Pin.OUT)
fan=Pin(2,Pin.OUT)
cooler_water=Pin(27,Pin.OUT)
cooler_motor=Pin(26,Pin.OUT)
cooler_speed=Pin(25,Pin.OUT)
from machine import SoftI2C,Pin
from oled import SSD1306_I2C
i2c = SoftI2C(scl=Pin(14), sda=Pin(13),freq=400000)
oled=SSD1306_I2C(128, 64, i2c, 0x3c)
import ui
oled.fill(0)
ui=ui.UI(oled)
