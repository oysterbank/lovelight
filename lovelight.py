from contextlib import contextmanager
from phue import Bridge

__author__ = "Kris Laratta"
__copyright__ = "Copyright (C) 2020 Kris Laratta"
__credits__ = ["Kris Laratta", ]
__license__ = "GPL"
__version__ = "0.3.0"
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

    @property
    def groups(self):
        groups = []
        bridge = self.bridge
        hue_groups = bridge.get_group()
        for k in hue_groups.keys():
            group_name = hue_groups[k]["name"]
            group = Group(group_name, self.bridge)
            groups.append(group)
        return groups

    def all_on(self):
        for l in self.lights:
            l.light.on = True

    def all_off(self):
        for l in self.lights:
            l.light.on = False

    @contextmanager
    def graceful_stop(
        self,
        light,
        end_state,
        brightness=None,
        transition_time=None
    ):
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

    @property
    def hue(self):
        return self.light.hue

    @property
    def saturation(self):
        return self.light.saturation

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

    def color(self, hue, saturation):
        self.light.hue = hue
        self.light.saturation = saturation


class Group():
    def __init__(self, name, bridge):
        self.bridge = bridge
        self.group = self.bridge.get_group(name)

    @property
    def name(self):
        return self.group['name']

    @property
    def lights(self):
        lights = []
        light_ids = self.group['lights']

        ll = Lovelight(self.bridge.ip)
        all_lights = ll.lights

        for light in all_lights:
            if str(light.id) in light_ids:
                lights.append(light)

        return lights
