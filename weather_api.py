from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/weather', methods=["GET"])
def get_weather():
    return jsonify({"First API": "HELLO WORLD!!!!!!"})

if __name__ == '__main__':
    app.run()