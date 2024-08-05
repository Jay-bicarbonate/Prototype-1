from flask import Flask, request, jsonify
from flask_cors import CORS

import osmnx as ox
import subprocess
import os

import xml.etree.ElementTree as ET

import warnings

import traci
import traci.constants as tc
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
CORS(app)

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
    # Receive JSON data from the request
    data = request.json

    #now creating the XML file for ActivityGen
    #this file will contain a lot demographic data such as general-info , population-info, work-hour-info etc.
    # Create the root XML element
    city = ET.Element('city')

    # Create the 'general' sub-element with attributes from the received data
    general = ET.SubElement(city, 'general', attrib={
        'inhabitants': data.get('inhabitants', '56000'),
        'households': data.get('households', '12000'),
        'childrenAgeLimit': data.get('childrenAgeLimit', '18'),
        'retirementAgeLimit': data.get('retirementAgeLimit', '60'),
        'carRate': data.get('carRate', '0.075'),
        'unemploymentRate': data.get('unemploymentRate', '0.071'),
        'footDistanceLimit': data.get('footDistanceLimit', '1.5'),
        'incomingTraffic': data.get('incomingTraffic', '5726'),
        'outgoingTraffic': data.get('outgoingTraffic', '5726')
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
    ET.SubElement(population, 'bracket', attrib={'beginAge': '0', 'endAge': '30', 'peopleNbr': '30'})
    ET.SubElement(population, 'bracket', attrib={'beginAge': '30', 'endAge': '60', 'peopleNbr': '40'})
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
    
    # Return a success message as JSON response
    return jsonify({'message': 'Data received and stored in XML file'}), 200


#button click "run simulation" triggers this function to execute some commands
#executes ActivityGen to create vehicle and executes duarouter to create routes
#also creates the mainsim.sumocfg config file used by TraCI and SUMO
@app.route('/run-simulation', methods=['POST'])
def run_simulation():

    sumo_network_filepath = os.path.join(config_folder_path, 'map.net.xml')
    stats_file_path = os.path.join(config_folder_path, 'stats.xml')
    output_file_path = os.path.join(config_folder_path, 'routes.rou.xml')
    duorouter_generated_file_path = os.path.join(config_folder_path, 'Final_routes.rou.xml')

    print()
    print('[*] executing ActivityGen...')
    subprocess.run(['activitygen', '--net-file', sumo_network_filepath, '--stat-file',stats_file_path, '--output-file', output_file_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    print('[*] executing duorouter...')
    subprocess.run(['duarouter', '--net-file', sumo_network_filepath, '--route-files', output_file_path, '--output-file', duorouter_generated_file_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    # Define the content of the sumocfg file
    sumocfg_content = """
    <configuration>
        <input>
            <net-file value="map.net.xml"/>
            <route-files value="Final_routes.rou.xml"/>
        </input>
        <time>
            <begin value="0"/>
            <end value="300"/>
        </time>
    </configuration>
    """

    print("[*]Generating main_sim.sumocfg.")
    # Save the content to main_sim.sumocfg
    sumocfg_file_path = os.path.join(config_folder_path, 'main_sim.sumocfg')
    with open(sumocfg_file_path, "w") as file:
        file.write(sumocfg_content)

    print("[#] All files generated Successfully")
    print()

    print('[*] Starting simulation ....')

    # Path to your sumo executable
    sumoBinary = "sumo"  # or "sumo-gui" for GUI version
    sumoConfig = sumocfg_file_path  #this is sumo config file which will contain the address of network file , routes file , time start , time end etc

    # Start the SUMO simulation using TraCI
    traci.start([sumoBinary, "-c", sumoConfig])

    # Dictionary to store vehicle counts per road
    road_vehicle_counts = {}

    # Run the simulation
    step = 0
    while step < 100:
        traci.simulationStep()
        # Get the list of edges
        edges = traci.edge.getIDList()
        for edge in edges:
            if edge not in road_vehicle_counts:
                road_vehicle_counts[edge] = 0
            road_vehicle_counts[edge] += traci.edge.getLastStepVehicleNumber(edge)
        step += 1
        print(step)

    # Close the simulation
    traci.close()

    # Extract data for visualization
    roads = list(road_vehicle_counts.keys())
    counts = list(road_vehicle_counts.values())

    print('[*]Data Generated successfully !!')

    result = {"status": "Simulation Completed ..."}

    return jsonify(result)



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
