from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app = Flask(__name__)
CORS(app)

@app.route('/submit-coordinates', methods=['POST'])
def submit_coordinates():
    data = request.json  # This will contain the coordinates
    print(data)  # Process or store the data as needed
    return jsonify({"status": "success", "message": "Coordinates received"}), 200