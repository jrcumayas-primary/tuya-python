from flask import Flask, jsonify
from tuya_connector import TuyaOpenAPI

from dotenv import load_dotenv
import os

app = Flask(__name__)

# Root endpoint
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/em/status')
def electric_meter_status():
    openapi = TuyaOpenAPI(os.getenv('API_ENDPOINT'), os.getenv('ACCESS_ID'), os.getenv('ACCESS_KEY'))
    openapi.connect()

    response = openapi.get(f"/v1.0/iot-03/devices/{os.getenv('ELECTRIC_METER_ID')}/status")
    
    return jsonify(message=response)

@app.route('/api/em/switch/<value>')
def switch_electric_meter(value):
    openapi = TuyaOpenAPI(os.getenv('API_ENDPOINT'), os.getenv('ACCESS_ID'), os.getenv('ACCESS_KEY'))
    openapi.connect()

    switch_value = True if (value == "true" or value == "True") else False
    commands = {'commands': [{'code': 'switch', 'value': switch_value}]}
    response = openapi.post(f"/v1.0/iot-03/devices/{os.getenv('ELECTRIC_METER_ID')}/commands", commands)
    
    return jsonify(message=response)

# Run the server
if __name__ == '__main__':
    app.run(debug=True)