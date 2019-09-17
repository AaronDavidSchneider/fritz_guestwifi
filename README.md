# Fritzbox Guestwifi Switch
## Custom component for use with Home Assistant

Fork of https://github.com/mammuth/ha-fritzbox-tools

### Features:
* turn on/off Guest Wifi in Home Assistant
* senses external on/off of Guest Wifi

### Installation:
put folder `fritz_guestwifi` (with files `__init__.py` and `switch.py`) to the `custom_components` folder in the `config` directory of your home assistant installation. Create `custom_components` if nescessary.

### Example Configuration:
```
switch:
  - platform: fritz_guestwifi
    host: "192.168.178.1"                 # ip adress of fritzbox
    username: "pi"                        # username of fritzboxuser
    password: !secret fritzbox_password   # password of fritzboxuser (string or secret)
    scan_interval: 5                      # (optional) update interval
```

The fritzbox needs a few seconds to turn on the guest wifi. As home assistant pulls the new state of the guest wifi directly after a switch toggle, the switch goes back to its earlier position. I therefore set `scan_interval` to a reasonably low time to get the state pulled quickly.

I use this switch together with the automatic disable setting in the fritzbox. It turns of the guest wifi if no one was connected for X minutes.

### Example Automation:
```
automation:
  - id: guestwifi_qr_notify
    alias: send credentials of Guest Wifi to phone
    trigger:
      platform: state
      entity_id: switch.guestwifi
      to: "on"
    action:
    - service: notify.ios_aarons_iphone
      data:
        message: !secret guestwifi_password
        title: "Guest Wifi --> on!"
        data:
          attachment:
            url: "/local/QR-Guestwifi.png"
            content-type: png
            hide-thumbnail: false
```
Where I put the QR Code in a `www` folder in my config directory (see e.g. https://community.home-assistant.io/t/help-with-entity-picture-and-file-location/38547/2). 
