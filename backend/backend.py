import json
from urllib.error import URLError
from urllib.request import urlopen

from flask import Flask, jsonify

app = Flask(__name__)
MPS_SOURCE_URL = "https://users.metropolia.fi/~peterh/mps.json"



@app.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "Hello, World! We have a flask API running."})


def fetch_mps():
    with urlopen(MPS_SOURCE_URL, timeout=10) as response:
        data = json.load(response)

    if not isinstance(data, list) or not all(isinstance(member, dict) for member in data):
        raise ValueError("The MP source returned an invalid data format")

    return data


def source_error():
    return jsonify({"error": "Could not fetch MP data from the source"}), 502


@app.route('/api/mps', methods=['GET'])
def list_mps():
    try:
        return jsonify(fetch_mps())
    except (OSError, URLError, TimeoutError, ValueError):
        return source_error()


@app.route('/api/mps/<int:person_number>', methods=['GET'])
def get_mp(person_number):
    try:
        members = fetch_mps()
    except (OSError, URLError, TimeoutError, ValueError):
        return source_error()

    member = next(
        (member for member in members if member.get("personNumber") == person_number),
        None,
    )
    if member is None:
        return jsonify({"error": "MP not found"}), 404

    return jsonify(member)

if __name__ == '__main__':
    app.run(debug=True)
