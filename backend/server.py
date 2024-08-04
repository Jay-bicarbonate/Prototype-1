from flask import Flask, request, jsonify
from flask_cors import CORS

import osmnx as ox
import subprocess
import os

import xml.etree.ElementTree as ET

import warnings

app = Flask(__name__)
CORS(app)

# Suppress specific warnings from osmnx, it was making the console very verbose hence supressing it
warnings.filterwarnings('ignore', category=UserWarning, module='osmnx')
warnings.filterwarnings('ignore', category=FutureWarning, module='osmnx')

config_folder_path = 'E:\\finale-submission\\backend\\config' 

# @app.route('/generatemap', methods=['POST'])
# def MapGenerator():

    # data = request.get_json()

    # print('[*] Received Data ; ')
    # print(data)
    # print()

    # north = data['north']
    # south = data['south']
    # east = data['east']
    # west = data['west']
@app.route('/bounding-box', methods=['POST'])
def bounding_box():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    north = data.get('north')
    south = data.get('south')
    east = data.get('east')
    west = data.get('west')

    # Define the bounding box (north, south, east, west)
    bbox = (north, south, east, west)

    try:
        # Download the OSM data within the bounding box
        G = ox.graph.graph_from_bbox(bbox=bbox, network_type='all')

        # Save the OSM data to a .osm file
        osm_filepath = os.path.join(config_folder_path, 'map.osm')
        ox.io.save_graph_xml(G, filepath=osm_filepath)

        # Convert the .osm file to SUMO XML format using netconvert
        sumo_network_filepath = os.path.join(config_folder_path, 'map.net.xml')
        print()
        print("[*] Converting map.osm to map.osm.xml ...")
        subprocess.run(['netconvert', '--osm-files', osm_filepath, '-o', sumo_network_filepath],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        print()
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
    # Receive JSON data from the request
    data = request.json

    # Create the root XML element
    city = ET.Element('city')
    
    # Create the 'general' sub-element with attributes from the received data
    general = ET.SubElement(city, 'general', attrib={
        'inhabitants': data.get('inhabitants', ''),
        'households': data.get('households', ''),
        'childrenAgeLimit': data.get('childrenAgeLimit', ''),
        'retirementAgeLimit': data.get('retirementAgeLimit', ''),
        'carRate': data.get('carRate', ''),
        'unemploymentRate': data.get('unemploymentRate', ''),
        'footDistanceLimit': data.get('footDistanceLimit', ''),
        'incomingTraffic': data.get('incomingTraffic', ''),
        'outgoingTraffic': data.get('outgoingTraffic', '')
    })


    # Create an ElementTree object with the root element
    print()
    print('[*] Creating XML elements')
    tree = ET.ElementTree(city)
    
    # Define the path for the XML file to be saved (the file is called statistics file hence the name stats.xml)
    stats_file_path = os.path.join(config_folder_path, 'stats.xml')
    
    
    # Write the XML data to the file
    print(f'[*] Saving XML file at {stats_file_path}')
    tree.write(stats_file_path)
    
    # Return a success message as JSON response
    return jsonify({'message': 'Data received and stored in XML file'}), 200


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
