import serial, argparse, time

class DmxPy:
    def __init__(self, serialPort, baudRate=57600, defaultLevel=255,dmxSize=512,levels=255):
        self.defaultLevel = defaultLevel
        self.levels = levels
        self.dmxSize = dmxSize
        try:
            self.serial = serial.Serial(serialPort, baudrate=baudRate)
        except:
            print('Error: could not open Serial Port:', serialPort)
            exit(1)
        if self.defaultLevel<0 or self.defaultLevel>self.levels:
            print('Light level must be 0-%d, not:'%self.levels, self.defaultLevel)
            exit(1)
        self.dmxData = [0] + [self.defaultLevel] * self.dmxSize

    def setChannel(self, chan, level):
        chan = self.dmxSize if chan > self.dmxSize else 1 if chan < 1 else chan # clip 1-self.dmxSize
        level = self.levels if level > self.levels else 0 if level < 0 else level # clip 0-255
        self.dmxData[chan] = level

    def blackout(self):
        self.dmxData = [0] + [0] * self.dmxSize

    def whiteout(self):
        self.dmxData = [0] + [self.defaultLevel] * self.dmxSize

    def render(self):
        dmxOpen = [0x7E]
        dmxClose = [0xE7]
        dmxIntensity = [6, (self.dmxSize+1) & 0xFF, (self.dmxSize+1)>>8 & 0xFF]
        self.serial.write(bytearray(dmxOpen + dmxIntensity+ self.dmxData + dmxClose))

def main():
    parser = argparse.ArgumentParser(description='Control Enttec DMX USB Pro')
    parser.add_argument('-r', '--rate', type=int, default=57600, help='baud rate for USB communication (default: 57600)')
    parser.add_argument('-p', '--port', type=str, required=True, help='Serial(COM) port, e.g., /dev/ttyUSB1 or COM3')
    parser.add_argument('-l', '--level', type=int, default=255, help='default level [0-255] of unspecified channels (default: 255)')
    parser.add_argument('-s', '--size', type=int, default=512, help='DMX Size (default: 512)')
    parser.add_argument('-b', '--blackout', action='store_true', help='Turn off all lights (level=0)')
    parser.add_argument('-w', '--whiteout', action='store_true', help='Turn on all lights at level')
    parser.add_argument('-d', '--demo', action='store_true', help='Play demo light pattern')
    args = parser.parse_args()

    dmx = DmxPy(args.port,baudRate=args.rate,defaultLevel=args.level,dmxSize=args.size)
    if not args.blackout and not args.whiteout and not args.demo:
        print('Select an action: [b]lackout, [w]hiteout, or [d]emo')
        parser.print_usage()
        exit(1)

    if args.blackout:
        dmx.blackout()
        dmx.render()
    elif args.whiteout:
        dmx.whiteout()
        dmx.render()
    elif args.demo:
        dmx.setChannel(1, 100)
        dmx.setChannel(2, 50)
        dmx.render()
        time.sleep(5)
        dmx.setChannel(3, 100)
        dmx.render()
        time.sleep(5)
        dmx.blackout()
        dmx.render()
        time.sleep(5)
        dmx.whiteout()
        dmx.render()