from machine import SoftI2C,Pin,ADC,RTC,Timer,WDT
from oled import SSD1306_I2C
heater_valve=Pin(21,Pin.OUT)
heater_fan=Pin(19,Pin.OUT)
mist=Pin(18,Pin.OUT)
fan=Pin(2,Pin.OUT)
cooler_water=Pin(27,Pin.OUT)
cooler_motor=Pin(26,Pin.OUT)
cooler_speed=Pin(25,Pin.OUT)
buzz=Pin(12,Pin.OUT)
i2c = SoftI2C(scl=Pin(14), sda=Pin(13),freq=400000)
oled=SSD1306_I2C(128, 64, i2c, 0x3c)
rtc=RTC()
up=Pin(39,Pin.IN)
ok=Pin(34,Pin.IN)
down=Pin(15,Pin.IN)
menu=Pin(5,Pin.IN)
