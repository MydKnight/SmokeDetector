from flask import Flask, Response, render_template, session, request
import time, json, serial

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
        with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
            while True:
                line = ser.readline()
                yield f"data:{line}\n\n"
                time.sleep(2)

    return Response(read_sensor_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')