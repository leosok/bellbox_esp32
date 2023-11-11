import micropython
import gc
import select

# Display memory available at startup.
gc.collect()
micropython.mem_info()

from audio_player import play_tune
from audio import bellbox_sounds, rtttl
play_tune(rtttl.RTTTL(bellbox_sounds.beep))

from lib.wifi_setup.wifi_setup import WiFiSetup

# You should give every device a unique name (to use as its access point name).
ws = WiFiSetup("Klingelkasten")
sta = ws.connect_or_setup()
del ws
print("WiFi is setup")

# Display memory available once the WiFi setup process is complete.
gc.collect()
micropython.mem_info()


from lib.microdot import Microdot, send_file
from machine import Pin
from time import sleep

app = Microdot()


def trigger_pin(pin_num: int, sleep_time_sec=0.2):
    """
    Triggers a Pin for 
    """
    pin = Pin(pin_num, Pin.OUT)
    pin.on()
    sleep(sleep_time_sec)
    pin.off()

@app.route('/api/<action>')
def trigger_pin_web(request, action) :
    
    action_pins = {
        'wohnzimmer': 16,
        'schlafzimmer': 35,
        'bad': 33,
        'entree': 39,
        'klingel': 37 
    }

    pin_to_trigger = action_pins.get(action)

    if pin_to_trigger:
        print(f"Pin found for {action}: {pin_to_trigger}")
        trigger_pin(pin_num=pin_to_trigger)
        return{
            'message': f"Pin found for {action}: {pin_to_trigger}"
        }

        #play_tune(rtttl.RTTTL(bellbox_sounds.down_tune))
    else:
        print(f"Pin NOT found for {action}")
        app.abort(404, "Pin not found")

@app.route('/')
def index(request):
    return send_file('www/index.html', max_age=86400)

@app.route('/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('www/' + path, max_age=86400)
    
app.run(port=80, debug=True)
print("microdot stated")
