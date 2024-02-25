from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS class
from wolframclient.evaluation import WolframCloudSession

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

def call(x, y):
    """ Call the API using function input parameter values.
    If the API was deployed with an export formats set to JSON or WXF, the result is often a native Python type.
    """
    with WolframCloudSession() as session:
        api_response = session.call('https://www.wolframcloud.com/obj/50f8f05b-e343-4156-97c8-f30f63eda474', {'x' : x, 'y' : y})
        return api_response.get()

@app.route('/submit-coordinates', methods=['POST', 'OPTIONS'])
def get_result():
    x = 39.842286020743394
    y = -103.9746093750000
    result = call(x, y)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)