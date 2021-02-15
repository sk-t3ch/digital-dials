from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

# car connection
import obd

# we only want these measurements so theyre hard coded
measurements = [
                {'name': 'ENGINE_LOAD',      'value': None},
                {'name': 'COOLANT_TEMP',     'value': None},
                {'name': 'INTAKE_PRESSURE',  'value': None},
                {'name': 'RPM',              'value': None},
                {'name': 'INTAKE_TEMP',      'value': None},
                {'name': 'SPEED',            'value': None}
            ]

connection = None

def try_connection():
    """ Use obd to connect to the car """
    print("triying to connect")
    connection = obd.Async(protocol="3", fast=True)
    print("connected")
    for measurement in measurements:
        connection.watch(obd.commands[measurement['name']], callback=new_measurement)
    connection.start()
    print("now watching")
    return connection

def new_measurement(measurement):
    """ Callback for sending measurment to front end """
    measurement_to_update = next((item for item in measurements if item['name'] == measurement.command.name), None)
    measurement_to_update["value"] = measurement.value.m
    socketio.emit('dial_update', measurement_to_update)
    print(measurement.command.name, measurement.value)

@app.route('/')
def index():
    """ Home page """
    return render_template('index.html')

@socketio.on('control')
def control(message):
    """ Socket for controlling stream """
    global connection
    if message["data"] == 'toggle':
        if not connection:
            socketio.emit('status', 'connecting')
            connection = try_connection()
            socketio.emit('status', 'connected')
        else:
            connection.close()
            connection = None
            socketio.emit('status', 'disconnected')

if __name__ == '__main__':
    socketio.run(app)
