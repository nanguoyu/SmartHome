import RPi.GPIO as GPIO
from flask import Response, Flask, jsonify, redirect, render_template, url_for
import json
from flask_bootstrap import Bootstrap

from fuckAll import Peins

peins = Peins()

app = Flask(__name__)
Bootstrap(app)

weatherINFO = ""

# from E
from EmbPi.CamMoudle.fuckCam import capturePhoto
from EmbPi.Dht11Moudle.fuckdht11 import read_dht11_dat, destroy, TemperatureHumidity
from EmbPi.LightMoudle.fucklight import turnOnLight, turnOffLight
from EmbPi.HSenorMoudle.fuckHSenor import AlarmMoudle
from weather import weatherPrint


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    fuckWeatherInfo = weatherPrint()
    # MTemperatureHumidity = TemperatureHumidity()
    MTemperatureHumidity = peins._TemperatureHumidity()
    global weatherINFO
    weatherINFO = MTemperatureHumidity
    return render_template('/dashboard.html', fuckWeatherInfo=fuckWeatherInfo.decode('utf8'),
                           MTemperatureHumidity=MTemperatureHumidity)


@app.route('/index', methods=['GET', 'POST'])
def index():
    fuckWeatherInfo = weatherPrint()
    # MTemperatureHumidity = TemperatureHumidity()
    if weatherINFO == "":
        MTemperatureHumidity = peins._TemperatureHumidity()
    else:
        MTemperatureHumidity = weatherINFO
    return render_template('/dashboard.html', fuckWeatherInfo=fuckWeatherInfo.decode('utf8'),
                           MTemperatureHumidity=MTemperatureHumidity)


@app.route('/TemperatureAndHumidity', methods=['GET', 'POST'])
def TemperatureAndHumidity():
    global temperature, humidity
    try:

        result = read_dht11_dat()
        if result:
            humidity, celsius = result
            temperature = celsius
            print("Humidity: %s%%,  Temperature: %s C`" % (humidity, temperature))
            temperature = str(temperature)
            humidity = str(humidity)
    except KeyboardInterrupt:
        destroy()
    return 'temperature:' + str(temperature) + ' humidity:' + str(humidity)


@app.route('/turnOff', methods=['GET', 'POST'])
def turnOff():
    # try:
    #     turnOffLight()
    # except KeyboardInterrupt:
    #     RPi.GPIO.cleanup()
    peins._turnOffLight()
    return redirect(url_for('index'))


@app.route('/turnOn', methods=['GET', 'POST'])
def turnOn():
    # try:
    #     turnOnLight()
    # except KeyboardInterrupt:
    #     RPi.GPIO.cleanup()
    peins._turnOnLight()
    return redirect(url_for('index'))


@app.route('/Cam', methods=['GET', 'POST'])
def Cam():
    capturePhoto()
    image = file("/home/pi/SmartHome/Web/static/1.jpg")
    resp = Response(image, mimetype="image/jpeg")
    return resp


@app.route('/CamCapure', methods=['GET', 'POST'])
def CamCapure():
    capturePhoto()
    return redirect(url_for('index'))


@app.route('/Alarm', methods=['GET', 'POST'])
def Alarm():
    try:
        AlarmMoudle()
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10086)
