from rtttl.rtttl import RTTTL
from rtttl import songs
import time

# Raspberry Pi Pico RTTTL example
# scruss - 2021-02: sorry, not sorry ...
from time import sleep_ms
from machine import Pin, PWM


def play_tone(freq, msec, duty=0.5, pwm_pin:PWM=None):
    # print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        pwm_pin.freq(int(freq))       # Set frequency
        pwm_pin.duty_u16(int(duty * 65535))   # Set duty cycle based on given value
    sleep_ms(int(0.9 * msec))     # Play for a number of msec
    pwm_pin.duty_u16(0)               # Stop playing for gap between notes
    sleep_ms(int(0.1 * msec))     # Pause for a number of msec


def play_tune(tune:RTTTL, speaker_pin=37, duty=0.05):
    pwm_pin = PWM(Pin(speaker_pin, Pin.OUT)) # in case Pin was already used before
    pwm_pin.deinit() # resetting the Pin
    pwm_pin = PWM(Pin(speaker_pin, Pin.OUT))

    try:
        for freq, msec in tune.notes():
            play_tone(freq, msec, duty, pwm_pin)
    except AttributeError:
        pass
    finally:
        pwm_pin.deinit()
    

