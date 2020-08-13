import json, serial, random, SerialReader, CSVWriter, ConfigManager, SmokeComms, time, sys
from flask import Flask, Response, render_template, session, request
from simple_pid import PID

app = Flask(__name__)
app.secret_key = "OonFooFoo"
smokeControl = SmokeComms.SmokeComms()
sessionLog = CSVWriter.CSVWriter()
currentConfig = ConfigManager.ConfigManager()

@app.route('/')
def overview():
    return render_template('index.html', button_list = getConfigParams())

@app.route('/calibrate')
def calibrate():
    # Read the current Set Point, and Selected Obs and pass these as parameters to the template
    return render_template('calibrate.html', button_list = getConfigParams())

@app.route('/storeParams/<updateSetting>/<updateValue>', methods=['POST'])
def store_params(updateSetting, updateValue):
   currentConfig.updateConfig(updateSetting, updateValue)
   return "Config Updated"

@app.route('/fireFog/<state>/<flow>', methods=['POST'])
def fire_fog(state=None, flow=255):
    if state == "start":
        smokeControl.start_smoke(flow)
        return "Smoke Started"
    else:
        smokeControl.stop_smoke()
        return "Smoke Stopped"

@app.route('/calculateControlValue')
def calculate_control():
    controlValue = "0"
    pValue = request.args.get('pValue')
    iValue = request.args.get('iValue')
    dValue = request.args.get('dValue')
    setPoint = request.args.get('setPoint')
    currentAverage = request.args.get('currentReading')

    pid = PID(float(pValue), float(iValue), float(dValue), float(setPoint))

    controlValue = pid(float(currentAverage))

    return str(controlValue)

@app.route('/chart-data', defaults={'average': None})
@app.route('/chart-data/<average>')
def chart_data(average):
    """Returns a data stream of readings from the sensor

    Args:
        average (string): Determines if we're returning all five observations or just an average of selected

    Returns:
        Array: Array of values (either all five readings or set point from INI and avg of selected)
    """
    if average == None:
        ser = SerialReader.SerialReader(csvLog = sessionLog)
        return Response(ser.read_sensor_data(currentConfig, averageObservation=False), mimetype='text/event-stream')
    else:
        ser = SerialReader.SerialReader(csvLog = sessionLog)
        return Response(ser.read_sensor_data(currentConfig, averageObservation=True), mimetype='text/event-stream')


def getConfigParams():
    """Reads the current selected particle sizes from ini and returns them as an array of class strings to apply

    Returns:
        array: list of classes to apply to the buttons
    """
    button_list = []
    particle_config = currentConfig.get_setting("selectedsizes")
    particle_settings = list(map(int, str(particle_config)))
    if particle_settings[0] == 0:
        button_list.append("btn particleButton text-center btn-outline-primary")
    else:
        button_list.append("btn particleButton clicked text-center btn-outline-primary")
    if particle_settings[1] == 0:
        button_list.append("btn particleButton text-center btn-outline-primary")
    else:
        button_list.append("btn particleButton clicked text-center btn-outline-primary")
    if particle_settings[2] == 0:
        button_list.append("btn particleButton text-center btn-outline-primary")
    else:
        button_list.append("btn particleButton clicked text-center btn-outline-primary")
    if particle_settings[3] == 0:
        button_list.append("btn particleButton text-center btn-outline-primary")
    else:
        button_list.append("btn particleButton clicked text-center btn-outline-primary")

    button_list.append(particle_settings)
    button_list.append(currentConfig.get_setting('domain'))
    button_list.append(currentConfig.get_setting('pValue'))
    button_list.append(currentConfig.get_setting('iValue'))
    button_list.append(currentConfig.get_setting('dValue'))
    button_list.append(currentConfig.get_setting('controlInterval'))
    button_list.append(currentConfig.get_setting('samplingInterval'))
    button_list.append(currentConfig.get_setting('controlValue'))

    return button_list

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')