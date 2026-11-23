from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "Hello, World! We have a flask API running."})

if __name__ == '__main__':
    app.run(debug=True)
