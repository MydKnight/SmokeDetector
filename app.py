from flask import Flask, Response, render_template, session, request
import time, json, serial, csv, datetime, random

app = Flask(__name__)

@app.route('/')
def overview():
    return render_template('index.html')

@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    def read_sensor_data():
        # Create CSV file to store data from this session 
        with open ('./logs/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + 'log.csv', mode='w') as logger:
            log_writer = csv.writer(logger, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Add Headers to CSV
            log_writer.writerow(['Observation 1', 'Observation 2', 'Observation 3', 'Observation 4', 'Observation 5', 'Observation 6', 'Observation 7', 'Observation 8', 'Observation 9', 'Observation 10'])
            
            with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
                while True:
                    line = ser.readline()
                    # First observation might be empty, if so, return
                    line = line.decode('utf-8')
                    if len(line) < 10:
                        print ("Line too short: " + line)
                        return

                    # Parse csv into JS array
                    observations = line.split(',')

                    # Write data to CSV file (May need to do extra work to get new rows)
                    log_writer.writerow([observations[0], observations[1], observations[2], observations[3], observations[4], observations[5], observations[6], observations[7], observations[8], observations[9]])

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

    return Response(read_sensor_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')