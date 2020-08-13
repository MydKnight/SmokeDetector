import serial, datetime, time, json

class SerialReader:
    def __init__(self, csvLog, usbPort='/dev/ttyUSB0', speed=115200):
        self.usbPort = usbPort
        self.speed = speed
        self.csvLog = csvLog
        self.ser = serial.Serial(self.usbPort, self.speed)

    def __del__(self):
        self.ser.close()

    def read_sensor_data(self, currentConfig, averageObservation):
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

            # Return the data to the endpoint calling. If averageObservation = False, return all values.
            if averageObservation == False:
                json_data = json.dumps(
                    {
                        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                        'obs1': float(observations[0]),
                        'obs2': float(observations[1]),
                        'obs3': float(observations[2]),
                        'obs4': float(observations[3])})
                yield f"data:{json_data}\n\n"
            # Else, return the set point and the average of selected values
            else:
                # Get the currently selected Observations
                particle_config = currentConfig.get_setting("selectedsizes")
                particle_settings = list(map(int, str(particle_config)))
                particle_sum = 0
                particle_count = 0
                if particle_settings[0] == 1:
                    particle_sum += float(observations[0])
                    particle_count += 1
                if particle_settings[1] == 1:
                    particle_sum += float(observations[1])
                    particle_count += 1
                if particle_settings[2] == 1:
                    particle_sum += float(observations[2])
                    particle_count += 1
                if particle_settings[3] == 1:
                    particle_sum += float(observations[3])
                    particle_count += 1
                
                # Get the Set Point
                set_point = currentConfig.get_setting("setpoint")
                if set_point == "":
                    set_point = 0

                # Return these two as an array
                json_data = json.dumps(
                    {
                        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                        'average': float(particle_sum/particle_count),
                        'setPoint': float(set_point)})
                yield f"data:{json_data}\n\n"
            time.sleep(2)