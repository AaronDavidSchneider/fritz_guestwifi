# Fritzbox Guestwifi Switch
## Custom component for use with Home Assistant

Fork of https://github.com/mammuth/ha-fritzbox-tools

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
