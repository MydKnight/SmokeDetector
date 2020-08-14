import serial
from serial.tools.list_ports import comports

if comports:
    com_ports_list = list(comports())
    for port in com_ports_list:
        if ("DMX USB PRO" in port):
            portString =str(port)
            usbPort = portString[0:12]
            print ("Port for DMX Adapter: " + usbPort)
        if ("CP2102" in str(port)):
            portString =str(port)
            usbPort = portString[0:12]
            print ("Port for Reader: " + usbPort)

ser = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    try:
        ser_bytes = ser.readline()
        #decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        decoded_bytes = ser_bytes.decode('utf-8')
        print(decoded_bytes)
    except Exception as e:
        print("Exception: " + str (e))
        break