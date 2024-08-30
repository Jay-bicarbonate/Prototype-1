
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import osmnx as ox
import subprocess
import os
import base64

import xml.etree.ElementTree as ET

import warnings

import traci
import traci.constants as tc
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

from utils.roadblocker import block_road
# from utils.Visualiser import plot_total_vehicle_heatmap, aggregate_vehicle_counts, plot_highlighted_roads
from utils.Visualiser import total_density_by_road
from utils.TrafficGen import TrafficGenerator

app = Flask(__name__)
CORS(app)

RandomTripsCount = None

# Suppress specific warnings from osmnx, it was making the console very verbose hence supressing it
warnings.filterwarnings('ignore', category=UserWarning, module='osmnx')
warnings.filterwarnings('ignore', category=FutureWarning, module='osmnx')

path_to_public_folder = 'E:/finale-submission/frontend/public'
config_folder_path = 'E:\\finale-submission\\backend\\config'  #make sure to change this config to your config path



def net2geojson(net_file,output_path):
    #----------------------add your tools path here ------------------------#
    path_to_tool = "C:/Program Files (x86)/Eclipse/Sumo/tools/net/net2geojson.py"


    print("Converting XML to geojson...")
    subprocess.run(['python', path_to_tool, '-n', net_file , '-o', output_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("conversion Complete :")


@app.route('/generatemap', methods=['POST'])
def MapGenerator():

    data = request.get_json()

    print('[*] Received Data ; ')
    print(data)
    print()

    north = data['north']
    south = data['south']
    east = data['east']
    west = data['west']

    trips = data['trips']

    print(f"Trips count : {trips}")

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

        #-------------add appropiate outpute path for map.geojson-----------#
        geojson_output_path = os.path.join(path_to_public_folder, 'map.geojson')
        net2geojson(sumo_network_filepath,geojson_output_path)

        #Generating Traffic using RandomTrips
        TrafficGenerator(trips,config_folder_path)

        result = {"status" : "Map Generated Successfully !"}

        return jsonify(result)

    except ValueError as e:
        print(f"Error: {e}")
        print("Please check the bounding box coordinates or try a larger area.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    


#button click "run simulation" triggers this function to execute some commands
#executes ActivityGen to create vehicle and executes duarouter to create routes
#also creates the mainsim.sumocfg config file used by TraCI and SUMO
@app.route('/run-simulation', methods=['POST'])
def run_simulation():

    print('[*] Starting simulation ....')
    sumocfg_file_path = os.path.join(config_folder_path, 'main_sim.sumocfg')

    subprocess.run(['sumo', '-c', sumocfg_file_path],
                   cwd=config_folder_path, check=True, stderr=subprocess.STDOUT)

    result = {"status": "Simulation Completed ..."}

    return jsonify(result)

#this function sends the density data per road to the frontend in the form of JSON 
#which is extracted by frontend to generated interactive heatmap
@app.route('/get-density-data', methods=['GET'])
def send_density_data():
    #density data in the form of a dict with RoadIDs as Keys and values as total density
    net_file = os.path.join(config_folder_path, 'map.net.xml')
    netstate_file = os.path.join(config_folder_path, 'netstatedump.xml')

    density_data = total_density_by_road(net_file,netstate_file)
    # print(f"density_data : {density_data}")

    return jsonify(density_data)


#this will edit the netfile , blocking the selected road given RoadID
@app.route('/update-road', methods=['POST'])
def update_road():
    data = request.json
    road_id = data.get('roadId')

    if not road_id:
        return jsonify({'error': 'No road ID provided'}), 400

    try:
        file_path = 'E:/finale-submission/backend/config/map.net.xml'
        block_road(file_path, road_id)
        return jsonify({'success': 'Road ID updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Reinforment Learning experiment
#we will do this experiment in the SUMO-GUI with realtime TraCI interface
@app.route('/rlexperiment', methods=['POST'])
def ReinforcementLearningExperiment():
    pass



if __name__ == '__main__':
    app.run(debug=True)
