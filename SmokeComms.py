import DmxPy, time
from serial.tools.list_ports import comports

class SmokeComms:
    """Provides functions for turning the smoker on and off
    """
    def __init__(self, port='/dev/ttyUSB1'):
        # Find the usb port that the Serial reader is on.
        if comports:
            com_ports_list = list(comports())
            for usb_port in com_ports_list:        
                if ("DMX USB PRO" in str(usb_port)):
                    portString =str(usb_port)
                    port = portString[0:12]

        self.port = port
        self.dmx = DmxPy.DmxPy(self.port)
        print("Ready")

    def __del__(self):
        self.dmx.blackout()
        self.dmx.render()

    def start_smoke(self, fanChannel=2, pumpChannel=1, intensity=255, fanSpeed=255):
        self.fanChannel = int(fanChannel)
        self.pumpChannel = int(pumpChannel)
        self.intensity = int(intensity)
        self.fanSpeed = int(fanSpeed)
        self.dmx.setChannel(self.pumpChannel ,self.intensity)
        self.dmx.setChannel(self.fanChannel, self.fanSpeed)
        self.dmx.render()

    def stop_smoke(self):
        print("Blacking out smoke")
        self.dmx.blackout()
        self.dmx.render()
