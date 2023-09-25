import micropython
import gc
import select

# Display memory available at startup.
gc.collect()
micropython.mem_info()

from lib.wifi_setup.wifi_setup import WiFiSetup

# You should give every device a unique name (to use as its access point name).
ws = WiFiSetup("Klingelkasten")
sta = ws.connect_or_setup()
del ws
print("WiFi is setup")

# Display memory available once the WiFi setup process is complete.
gc.collect()
micropython.mem_info()

###### Device is connected ########

from lib.slim.slim_server import SlimServer
from lib.slim.fileserver_module import FileserverModule
from lib.slim.web_route_module import HttpMethod, WebRouteModule, RegisteredRoute

poller = select.poll()

def RequestTest(request) :
    
    action_pins = {
        'schlafzimmer': 11,
        'bad': 12,
        'wohnzimmer': 13,
        'entree': 14
    }

    path_action = request.Path.split("/")[-1]
    pin_to_trigger = action_pins.get(path_action)

    if pin_to_trigger:
        print(f"Pin found for {path_action}: {pin_to_trigger}")
        request.Response.ReturnOkJSON({
            'message': f"Pin found for {path_action}: {pin_to_trigger}"
        })
    else:
        print(f"Pin NOT found for {path_action}")
        request.ReturnNotFound()


slim_server = SlimServer(poller)

slim_server.add_module(WebRouteModule([
        RegisteredRoute(HttpMethod.GET, "/api/schlafzimmer", RequestTest),
        RegisteredRoute(HttpMethod.GET, "/api/bad", RequestTest),
        RegisteredRoute(HttpMethod.GET, "/api/wohnzimmer", RequestTest),
        RegisteredRoute(HttpMethod.GET, "/api/entree", RequestTest),
    ]))

slim_server.add_module(FileserverModule({"html": "text/html", 'css': "text/css"}))


while True:
    for (s, event) in poller.ipoll(0):
        slim_server.pump(s, event)
    slim_server.pump_expire()