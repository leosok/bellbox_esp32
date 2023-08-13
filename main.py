# main.py -- put your code here!

from misc import status_led

import wifimgr

status_led(False)
wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
status_led(True)