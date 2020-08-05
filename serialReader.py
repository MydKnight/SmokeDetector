import serial, time

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    while True:
        line = ser.readline()
        print (line)
        time.sleep(2)