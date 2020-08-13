import serial

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