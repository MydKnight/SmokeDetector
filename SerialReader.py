import serial, datetime, time, json

class SerialReader:
    def __init__(self, csvLog, usbPort='/dev/ttyUSB0', speed=115200, timeout=1):
        self.usbPort = usbPort
        self.speed = speed
        self.timeout = timeout
        self.csvLog = csvLog
        self.ser = serial.Serial(self.usbPort, self.speed, timeout=self.timeout)

    def __del__(self):
        self.ser.close()

    def read_sensor_data(self):
        while True:
            line = self.ser.readline()
            # First observation might be empty, if so, return
            line = line.decode('utf-8')
            if len(line) < 10:
                print ("Line too short: " + line)
                return

            # Parse seral data into JS array
            observations = line.split(',')

            self.csvLog.newObservation([observations[0], observations[1], observations[2], observations[3], observations[4], observations[5], observations[6], observations[7], observations[8], observations[9]])

            # Return the data to the endpoint calling
            json_data = json.dumps(
                {
                    'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    'obs1': float(observations[4]),
                    'obs2': float(observations[5]),
                    'obs3': float(observations[6]),
                    'obs4': float(observations[7]),
                    'obs5': float(observations[8])})
            yield f"data:{json_data}\n\n"
            time.sleep(2)