from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generatemap', methods=['POST'])
def bounding_box():
    data = request.get_json()

    print(data)

    north = data['north']
    south = data['south']
    east = data['east']
    west = data['west']
    
    # Process the bounding box data here
    # For this example, we'll just return it back as JSON
    result = {
        'status' : 'Result Received succesfully',
        'north': north,
        'south': south,
        'east': east,
        'west': west
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
