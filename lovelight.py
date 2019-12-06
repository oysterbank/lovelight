from phue import Bridge

__author__ = "Kris Laratta"
__copyright__ = "Copyright (C) 2019 Kris Laratta"
__credits__ = ["Kris Laratta", ]
__license__ = "GPL"
__version__ = "0.0.1"
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


class Light():
    def __init__(self, hue_light, bridge):
        self.light = hue_light
        self.bridge = bridge

    @property
    def id(self):
        return self.light.light_id

    def dim_off(self, end_state, seconds):
        transition_time = seconds * 10
        self.bridge.set_light(
            self.id,
            {
                "on": end_state,
                "transitiontime": transition_time
            }
        )
