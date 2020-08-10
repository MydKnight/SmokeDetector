import datetime, time, csv, os, glob

class CSVWriter:
    """Generates a CSV file and provides methods for updating it to other classes. 
    """
    def __init__(self):
        # If there is a current log file, get that for writing. 
        if glob.glob('./logs/*.csv'):
            logs = glob.glob('./logs/*.csv') 
            self.filename = max(logs, key=os.path.getctime)
        # else create one
        else:
            self.filename = './logs/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + 'log.csv' 
            with open(self.filename, 'w', newline='') as logs:
                log_writer = csv.writer(logs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
                log_writer.writerow(['Observation 1', 'Observation 2', 'Observation 3', 'Observation 4', 'Observation 5', 'Observation 6', 'Observation 7', 'Observation 8', 'Observation 9', 'Observation 10', 'OpMode', 'P-Value', 'I-Value', 'D-Value', 'SetPoint', 'SelectedObs', 'Domain', 'SampleInterval', 'ControlValue'])
            #self.log_file = open (self.filename, mode='w')
            #self.log_writer = csv.writer(self.log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Add Headers to CSV
            #self.log_writer.writerow(['Observation 1', 'Observation 2', 'Observation 3', 'Observation 4', 'Observation 5', 'Observation 6', 'Observation 7', 'Observation 8', 'Observation 9', 'Observation 10', 'OpMode', 'P-Value', 'I-Value', 'D-Value', 'SetPoint', 'SelectedObs', 'Domain', 'SampleInterval', 'ControlValue'])
            # When a new log is created, many of the default values will be read from a config file. Read this file and store them as values to write to the columns
            
    def __del__(self):
        pass
        # self.log_file.close()

    def startNewLog(self):
        pass

    def newObservation(self, data):
        """Records a new row (observation) to the CSV file. 

        Args:
            data (string): This string is a comma separated list of values we want to write to the current session log
        """
        # Should add error handling here to parse that the data is valid
        with open(self.filename, 'a', newline='') as logs:
            data[-1] = data[-1].rstrip()
            print(data)
            log_writer = csv.writer(logs, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            log_writer.writerow(data)

