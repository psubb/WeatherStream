from flask import Flask, jsonify
from weather_client import get_weather_data, get_api_key

app = Flask(__name__)

@app.route('/weather-api/<string:location>', methods=["GET"])
def get_weather(location):
    weather_info = get_weather_data(location, get_api_key())
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run()