from contextlib import contextmanager
from phue import Bridge

__author__ = "Kris Laratta"
__copyright__ = "Copyright (C) 2019 Kris Laratta"
__credits__ = ["Kris Laratta", ]
__license__ = "GPL"
__version__ = "0.0.2"
__maintainer__ = "Kris Laratta"
__email__ = "krislaratta@gmail.com"
__status__ = "Development"


class Lovelight():
    def __init__(self, bridge_ip):
        b = Bridge(bridge_ip)
        b.connect()
        self.bridge = b

    @property
    def lights(self):
        lights = []
        bridge = self.bridge
        hue_lights = bridge.lights
        for l in hue_lights:
            light = Light(l, bridge)
            lights.append(light)
        return lights

    def all_on(self):
        for l in self.lights:
            l.light.on = True

    def all_off(self):
        for l in self.lights:
            l.light.on = False

    @contextmanager
    def graceful_stop(self,
                      light,
                      end_state,
                      brightness=None,
                      transition_time=None):
        """
        Allows the user to define a state for a routine to end on.
        """
        try:
            yield
        finally:
            if end_state == "off":
                light.off()
            elif end_state == "on":
                light.on()
            elif end_state == "dim":
                if brightness and transition_time:
                    light.dim(False, brightness, transition_time)
                elif brightness:
                    light.dim(False, brightness, 50)
                elif transition_time:
                    light.dim(False, 0, transition_time)
                else:
                    light.dim(False, 0, 50)
            else:
                raise NotImplementedError("Not a command.")


class Light():
    def __init__(self, hue_light, bridge):
        self.light = hue_light
        self.bridge = bridge

    @property
    def id(self):
        return self.light.light_id

    @property
    def name(self):
        return self.light.name

    def on(self):
        self.light.on = True

    def off(self):
        self.light.on = False

    def dim(self, end_state, brightness, transition_time):
        self.bridge.set_light(
            self.id,
            {
                "on": end_state,
                "bri": brightness,
                "transitiontime": transition_time
            }
        )
