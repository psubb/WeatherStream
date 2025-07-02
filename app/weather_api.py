import time
from kafka import KafkaProducer, errors
from flask import Flask, jsonify
import json
import redis
from weather_client import get_weather_data, get_api_key


app = Flask(__name__)

redis_client = redis.Redis(host="host.docker.internal", port=6379, db=0)

# lazy initialized Kafka producer
_producer = None

def get_producer():
    """
    Return a singleton Kafka producer, retrying if brokers arent ready.
    """
    global _producer
    if _producer is None:
        for attempt in range(10):
            try:
                _producer = KafkaProducer(
                    bootstrap_servers='kafka:9092',
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                print(f"[KAFKA] connected on attempt {attempt + 1}")
                break
            except errors.NoBrokersAvailable:
                print(f"[KAFKA] broker not available, retry {attempt + 1}/10")
                # Retry after waiting one second
                time.sleep(1)
        # If after retrying 10 times and still no producer.
        if _producer is None:
            print("[KAFKA] failed to connect after 10 retries; proceeding without producer")
    
    return _producer


def publish_weather_update(location, data):
    """
    Send the filtered weather JSON to 'weather-updates' Kafka topic
    """
    print(f"[PUBLISH CALLED] for {location}")
    producer = get_producer()
    if not producer:
        print("[PUBLISH] skipping because no producer")
        # if never connected, skip the publishing
        return

    payload = {"location": location, "data": data}
    print(f"[PUBLISH] -> weather-updates: {payload}")
    try:
        producer.send("weather-updates", value=payload)
        producer.flush()
    except Exception as e:
        print(f"[KAFKA] publish failed: {e}")


@app.route('/weather-api/<string:location>', methods=["GET"])
def get_weather(location):
    api_key = get_api_key()
    print(f"[DEBUG] api_key={api_key!r}")
    
    # Attempt to retrieve cached data
    cached_data = redis_client.get(location)
    if cached_data:  # if cached, return
        print(f"[CACHE HIT] {location}")
        return jsonify(json.loads(cached_data))
    
    # If not cached, call API
    print(f"[CACHE MISS] {location}")
    weather_info = get_weather_data(location, api_key)
    print(f"[DEBUG] weather_info={weather_info!r}")
    
    if weather_info:
       redis_client.setex(location, 86400, json.dumps(weather_info))
       publish_weather_update(location, weather_info)
    else:
        print("[DEBUG] Skipping publish because weather_info is None or falsy")
    
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0')