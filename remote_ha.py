import sys
import requests
import json

from remote.remote import SiriRemote, RemoteListener

EVENT_API_URL = "http://homeassistant.local:8123/api/events/"
HA_TOKEN = "your_token"

HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(HA_TOKEN)}
remote = "remote"

def fire_event(event_type, payload):
    payload_str = json.dumps(payload)
    requests.post(EVENT_API_URL + event_type, headers=HEADERS, data=payload_str)
    

class Callback(RemoteListener):
    def event_battery(self, percent: int):
        print("Battery", percent)
        fire_event("siriremote_battery", {"remote": remote, "percent": percent})

    def event_power(self, charging: bool):
        print("Power", charging)
        fire_event("siriremote_charging", {"remote": remote, "charging": charging})

    def event_button(self, button: int):
        print("Button", button)
        if button > 0:
            fire_event("siriremote_button", {"remote": remote, "button": button})

    def event_touchpad(self, data, pressed: bool):
        print("Touch", data, pressed)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        mac = sys.argv[1]
        if len(sys.argv) > 2:
            remote = sys.argv[2]
        SiriRemote(mac, Callback())
    else:
        print("Usage: python remote_ha.py <remote MAC address> [remote name]")