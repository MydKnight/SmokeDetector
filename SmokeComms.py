import DmxPy, time

class SmokeComms:
    """Provides functions for turning the smoker on and off
    """
    def __init__(self, port='/dev/ttyUSB1'):
        self.port = port
        self.dmx = DmxPy.DmxPy(self.port)
        print("Ready")

    def __del__(self):
        self.dmx.blackout()
        self.dmx.render()

    def start_smoke(self, timeInterval=0):
        print("Setting Channel")
        self.dmx.setChannel(1,255)
        self.dmx.setChannel(2,255)
        self.dmx.render()
        print("rendered channel")

    def stop_smoke(self):
        print("Blacking out smoke")
        self.dmx.blackout()
        self.dmx.render()
