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


from lib.microdot_asyncio import Microdot, send_file
from machine import Pin
import uasyncio as asyncio

app = Microdot()


async def trigger_pin(pin_num: int, sleep_time_ms=200):
    """
    Triggers a Pin for 
    """
    pin = Pin(pin_num, Pin.OUT)
    pin.on()
    await asyncio.sleep_ms(sleep_time_ms)
    pin.off()


@app.route('/api/<action>')
async def trigger_pin_web(request, action) :
    
    action_pins:dict[str, tuple[int,int]] = {
        'wohnzimmer': (16, 200),
        'schlafzimmer': (35, 200),
        'bad': (33, 200),
        'entree': (39, 200),
        'klingel': (37, 125), 
    }

    pin_data = action_pins.get(action, None)
    if pin_data:
        print(f"Pin found for {action}: {pin_data}")
        pin_to_trigger, sleep_time_ms = pin_data
        await trigger_pin(pin_num=pin_to_trigger, sleep_time_ms=sleep_time_ms)
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
