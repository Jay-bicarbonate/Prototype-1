from flask import Flask, request, jsonify
from flask_cors import CORS

import osmnx as ox
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/generatemap', methods=['POST'])
def MapGenerator():

    data = request.get_json()

    print('[*] Received Data ; ')
    print(data)

    north = data['north']
    south = data['south']
    east = data['east']
    west = data['west']

    # Define the bounding box (north, south, east, west)
    bbox = (north, south, east, west)

    try:
        # Download the OSM data within the bounding box
        G = ox.graph.graph_from_bbox(*bbox, network_type='all')

        # Save the OSM data to a .osm file
        osm_filepath = 'map.osm'
        ox.io.save_graph_xml(G, filepath=osm_filepath)

        # Convert the .osm file to SUMO XML format using netconvert
        sumo_network_filepath = 'map.net.xml'
        subprocess.run(['netconvert', '--osm-files', osm_filepath, '-o', sumo_network_filepath], check=True)

        print(f"SUMO network file saved to {sumo_network_filepath}")

        result = {"status" : "Map Generated Successfully !"}

        return jsonify(result)

    except ValueError as e:
        print(f"Error: {e}")
        print("Please check the bounding box coordinates or try a larger area.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



#traffic Generator using the ActivityGen algorithm from SUMO
#parameter will be provided via a input form for demographic data , then sent here in the form a JSON post req
@app.route('/generatetraffic', methods=['POST'])
def TrafficGenerator():
    pass


#visualisation
#this function will visualise the generated traffic data and show it to the user as per the parameters.
#parameters could be different visulaisation option such as "average speed per road" OR "total vehicle count per road" etc
@app.route('/visualiser', methods=['POST'])
def visualiser():
    pass


#what-if scinario
#need to think about this one , either do it in the webapp or need to use SUMO netedit for similicity.
#implimenting netedit functionality into a webapp would be a time taking and not so easy task tbh.
@app.route('/whatif', methods=['POST'])
def whatif():
    pass


#Reinforment Learning experiment
#we will do this experiment in the SUMO-GUI with realtime TraCI interface
@app.route('/rlexperiment', methods=['POST'])
def ReinforcementLearningExperiment():
    pass








if __name__ == '__main__':
    app.run(debug=True)
