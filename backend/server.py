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
from utils.Visualiser import plot_total_vehicle_heatmap, aggregate_vehicle_counts, plot_highlighted_roads

app = Flask(__name__)
CORS(app)

RandomTripsCount = None

# Suppress specific warnings from osmnx, it was making the console very verbose hence supressing it
warnings.filterwarnings('ignore', category=UserWarning, module='osmnx')
warnings.filterwarnings('ignore', category=FutureWarning, module='osmnx')

config_folder_path = 'E:\\finale-submission\\backend\\config' 

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

    #to be used in "run simulation" later
    global RandomTripsCount

    # Receive JSON data from the request
    data = request.json

    #assigning value to the variable for later use in "run Simulation"
    RandomTripsCount = str(data.get('randomTrips'))
    print(f'[*] Received Random trips {RandomTripsCount}')

    #now creating the XML file for ActivityGen
    #this file will contain a lot demographic data such as general-info , population-info, work-hour-info etc.
    # Create the root XML element
    city = ET.Element('city')

    # Create the 'general' sub-element with attributes from the received data
    general = ET.SubElement(city, 'general', attrib={
        'inhabitants': data.get('inhabitants', '1300'),
        'households': data.get('households', '252'),
        'childrenAgeLimit': data.get('childrenAgeLimit', '18'),
        'retirementAgeLimit': data.get('retirementAgeLimit', '60'),
        'carRate': data.get('carRate', '0.075'),
        'unemploymentRate': data.get('unemploymentRate', '0.071'),
        'footDistanceLimit': data.get('footDistanceLimit', '1.5'),
        'incomingTraffic': data.get('incomingTraffic', '121'),
        'outgoingTraffic': data.get('outgoingTraffic', '121')
    })

    # Add 'parameters' element
    parameters = ET.SubElement(city, 'parameters', attrib={
        'carPreference': '0.50',
        'meanTimePerKmInCity': '6',
        'freeTimeActivityRate': '0.15',
        'uniformRandomTraffic': '0.20',
        'departureVariation': '300'
    })

    # Add 'population' element with 'bracket' sub-elements
    population = ET.SubElement(city, 'population')
    ET.SubElement(population, 'bracket', attrib={'beginAge': '0', 'endAge': '30', 'peopleNbr': '40'})
    ET.SubElement(population, 'bracket', attrib={'beginAge': '30', 'endAge': '60', 'peopleNbr': '30'})
    ET.SubElement(population, 'bracket', attrib={'beginAge': '60', 'endAge': '90', 'peopleNbr': '30'})

    # Add 'workHours' element with 'opening' and 'closing' sub-elements
    work_hours = ET.SubElement(city, 'workHours')
    ET.SubElement(work_hours, 'opening', attrib={'hour': '30600', 'proportion': '0.30'})
    ET.SubElement(work_hours, 'opening', attrib={'hour': '32400', 'proportion': '0.70'})
    ET.SubElement(work_hours, 'closing', attrib={'hour': '43200', 'proportion': '0.20'})
    ET.SubElement(work_hours, 'closing', attrib={'hour': '63000', 'proportion': '0.20'})
    ET.SubElement(work_hours, 'closing', attrib={'hour': '64800', 'proportion': '0.60'})

    # Add 'streets' element with 'street' sub-elements
    streets = ET.SubElement(city, 'streets')
    ET.SubElement(streets, 'street', attrib={'edge': '0', 'population': '10', 'workPosition': '100'})
    ET.SubElement(streets, 'street', attrib={'edge': '1', 'population': '10', 'workPosition': '100'})
    ET.SubElement(streets, 'street', attrib={'edge': '10', 'population': '10', 'workPosition': '100'})

    # Create an ElementTree object with the root element
    print()
    print('[*] Creating XML elements')
    tree = ET.ElementTree(city)
    
    # Define the path for the XML file to be saved (the file is called statistics file hence the name stats.xml)
    stats_file_path = os.path.join(config_folder_path, 'stats.xml')
    
    # Write the XML data to the file
    print(f'[*] Saving XML file at {stats_file_path}')
    tree.write(stats_file_path)
    
    sumo_network_filepath = os.path.join(config_folder_path, 'map.net.xml')
    stats_file_path = os.path.join(config_folder_path, 'stats.xml')
    output_file_path_ActivityGen = os.path.join(config_folder_path, 'routes.rou.xml')
    output_file_path_RandomTrips = os.path.join(config_folder_path, 'trips.trips.xml')
    duorouter_generated_file_path = os.path.join(config_folder_path, 'Final_routes.rou.xml')

    randomTripspy_path = os.path.join("C:\\Program Files (x86)\\Eclipse\\Sumo\\tools","randomTrips.py")

    print()
    print('[*] executing ActivityGen...')
    subprocess.run(['activitygen', '--net-file', sumo_network_filepath, '--stat-file',stats_file_path, '--output-file', output_file_path_ActivityGen],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    print('[*] executing duorouter...')
    try:
        subprocess.run(['duarouter', '--net-file', sumo_network_filepath, '--route-files', output_file_path_ActivityGen, '--output-file', duorouter_generated_file_path],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Continuing execution with randomTrips.py")
        pass

    print()
    print(f'[*] Generating RandomTrips : {RandomTripsCount}....')
    
    subprocess.run(['python', randomTripspy_path, '--net-file', sumo_network_filepath, '-e', RandomTripsCount],
                   cwd=config_folder_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print('[*] executing duorouter...')
    try:
        subprocess.run(['duarouter', '--net-file', sumo_network_filepath, '--route-files', output_file_path_RandomTrips, '--output-file', duorouter_generated_file_path],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")    


    # Define the content of the sumocfg file
    sumocfg_content = """
    <configuration>
        <input>
            <net-file value="map.net.xml"/>
            <route-files value="Final_routes.rou.xml"/>
        </input>
        <processing>
            <ignore-route-errors value="true"/>
        </processing>
        <routing>
            <device.rerouting.adaptation-steps value="18"/>
            <device.rerouting.adaptation-interval value="10"/>
        </routing>
        <output>
            <netstate-dump value="netstatedump.xml"/>
        </output>
    </configuration>
    """
    
    print("[*]Generating main_sim.sumocfg.")
    # Save the content to main_sim.sumocfg
    sumocfg_file_path = os.path.join(config_folder_path, 'main_sim.sumocfg')
    with open(sumocfg_file_path, "w") as file:
        file.write(sumocfg_content)

    print("[#] All files generated Successfully")
    print()
    
    # Return a success message as JSON response
    return jsonify({'message': 'Data received and stored in XML file'}), 200

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



#visualisation
#this function will visualise the generated traffic data and show it to the user as per the parameters.
#parameters could be different visulaisation option such as "average speed per road" OR "total vehicle count per road" etc
@app.route('/create-plot', methods=['GET'])
def create_plot():

    net_file = os.path.join(config_folder_path, 'map.net.xml')
    netstate_file = os.path.join(config_folder_path, 'netstatedump.xml')

    #get plot image and covert to b64 to send!!
    img = plot_total_vehicle_heatmap(net_file,netstate_file)
    img_base64 = base64.b64encode(img.read()).decode('utf-8')

    # Get JSON plot data
    json_plot_data = aggregate_vehicle_counts(netstate_file, net_file)

    # Combine the image data and JSON data into one response
    response = {
        'image': img_base64,
        'json_data': json_plot_data
    }

    return jsonify(response)


#what-if scinario
#need to think about this one , either do it in the webapp or need to use SUMO netedit for similicity.
#implimenting netedit functionality into a webapp would be a time taking and not so easy task tbh.
@app.route('/whatif', methods=['POST'])
def whatif():
    pass

#to get the road_ids from the netfile so that we can make the dropdown menu
@app.route('/road_ids', methods=['GET'])
def get_road_ids():
    net_file = os.path.join(config_folder_path, 'map.net.xml')  # Update this path to your net.xml file
    print(f"Parsing XML file: {net_file}")  # Debug print

    tree = ET.parse(net_file)
    root = tree.getroot()

    road_ids = []
    print(f"Fetching Road IDs from net file ....")
    for edge in root.findall('edge'):
        edge_id = edge.get('id')
        if edge_id and not edge_id.startswith(':'):  # Filter out internal edges
            # print(f"Found road ID: {edge_id}")  # Debug print
            road_ids.append(edge_id)

    print(f"Total road IDs fetched: {len(road_ids)}")  # Debug print

    return jsonify(road_ids)


#this is triggered when the user selects any road
@app.route('/select_road', methods=['POST'])
def select_road():
    data = request.json
    road_id = data.get('road_id')

    if not road_id:
        return {'error': 'Road ID is required'}, 400

    try:
        # Path to your net.xml file
        net_file = os.path.join(config_folder_path, 'map.net.xml')
        fig = plot_highlighted_roads(net_file, road_id)

        # Save the plot to a BytesIO object
        img_io = BytesIO()
        fig.savefig(img_io, format='png')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='plot.png')

    except Exception as e:
        print(f'Error occurred: {e}')
        return {'error': 'Internal server error'}, 500


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
