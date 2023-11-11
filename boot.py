# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# Turn on LED to indicate Power
from machine import Pin, PWM
PWM(Pin(15), freq=1000, duty=300)