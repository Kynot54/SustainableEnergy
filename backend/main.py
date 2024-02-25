import re
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from wolframclient.evaluation import WolframCloudSession
import threading

app = Flask(__name__)
CORS(app)


def call_wolfram_api(x, y, results, index):
    """ Function to call the Wolfram API and store the result """
    with WolframCloudSession() as session:
        api_response = session.call('https://www.wolframcloud.com/obj/50f8f05b-e343-4156-97c8-f30f63eda474',
                                    {'x': x, 'y': y})
        result = api_response.get()

    match = re.search(r'\d+\.\d+', result.decode('utf-8'))
    if match:
        numerical_value = float(match.group())
        results[index] = numerical_value


@app.route('/submit-coordinates', methods=['POST'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def get_result():
    if request.method == 'POST':
        data = request.get_json()
        coordinates = data['coordinates']

        results = [None] * len(coordinates)  # Placeholder for numerical values

        threads = []

        for index, coordinate in enumerate(coordinates):
            x, y = coordinate['lat'], coordinate['lng']
            thread = threading.Thread(target=call_wolfram_api, args=(x, y, results, index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Get the top 3 numerical values
        numerical_values = [(index, value) for index, value in enumerate(results) if value is not None]
        top_10_values = sorted(numerical_values, key=lambda x: x[1], reverse=True)[:10]

        # Construct a response object with top 3 values and indices
        response_data = {
            'top_10_results': [{'index': index, 'value': value} for index, value in top_10_values]
        }

        response = jsonify(response_data)
        return response
    else:
        response = jsonify({'error': 'Method not allowed'})
        response.status_code = 405
        return response
