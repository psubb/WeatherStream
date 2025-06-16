from flask import Flask, jsonify
import json
import redis
from weather_client import get_weather_data, get_api_key


app = Flask(__name__)

redis_client = redis.Redis(host="host.docker.internal", port=6379, db=0)

@app.route('/weather-api/<string:location>', methods=["GET"])
def get_weather(location):
    api_key = get_api_key()
    
    # Attempt to retrieve cached data
    cached_data = redis_client.get(location)
    if cached_data:  # if cached, return
        return jsonify(json.loads(cached_data))
    
    # If not cached, call API
    weather_info = get_weather_data(location, api_key)
    if weather_info:
       redis_client.setex(location, 86400, json.dumps(weather_info))
    
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0')