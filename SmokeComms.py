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

    def start_smoke(self, intensity=255):
        self.intensity = int(intensity)
        self.dmx.setChannel(1,self.intensity)
        self.dmx.setChannel(2,255)
        self.dmx.render()

    def stop_smoke(self):
        print("Blacking out smoke")
        self.dmx.blackout()
        self.dmx.render()
