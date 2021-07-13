# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from machine import freq
freq(240000000)
from wifi import ap
ap()
from save import save,load
save('update','True')