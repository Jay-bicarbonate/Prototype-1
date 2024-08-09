import xml.etree.ElementTree as ET
import traci
import os
import subprocess

def add_traffic_signal_to_junction(junction_id, net_file):
    print(f"Loading network XML from {net_file}...")
    tree = ET.parse(net_file)
    root = tree.getroot()

    config_path = "E:\\finale-submission\\backend\\config"
    osm_file = os.path.join(config_path,"map.osm")

    print(f"Searching for junction {junction_id}...")
    junction_found = False

    for junction in root.findall('junction'):
        if junction.get('id') == junction_id:
            junction_found = True
            if junction.get('type') != 'traffic_light':
                print(f"Junction {junction_id} found. Adding traffic signal...")
                junction.set('type', 'traffic_light')
                print(f"Traffic signal added to junction {junction_id}.")
            else:
                print(f"Junction {junction_id} already has a traffic signal.")
            break

    if not junction_found:
        print(f"Error: Junction {junction_id} not found in the network.")
        return

    # Save the modified XML file
    tree.write(net_file)
    print(f"Network XML saved to {net_file}.")

    # Run the netconvert command
    try:
        print(f"Running netconvert to add traffic lights...")
        result = subprocess.run([
            'netconvert',
            '--osm-files', osm_file,
            '--output-file', net_file,
            '--tls.set', junction_id
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("netconvert output:")
        print(result.stdout)
        print("netconvert errors (if any):")
        print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error running netconvert: {e}")
        print(e.stderr)

# def get_traffic_signal_state(junction_id, net_file):
#     """
#     Get the current state of the traffic signal for a given junction ID.
    
#     :param junction_id: The ID of the junction whose traffic signal state is to be queried.
#     :return: The current state of the traffic signal as a string.
#     """
#     add_traffic_signal_to_junction(junction_id, net_file)

#     # Ensure that the SUMO configuration file path is valid
#     sumo_config_path = "E:\\finale-submission\\backend\\config\\main_sim.sumocfg"
#     if not os.path.isfile(sumo_config_path):
#         raise FileNotFoundError(f"SUMO configuration file not found: {sumo_config_path}")

#     # Start the TraCI connection
#     if not traci.isLoaded():
#         traci.start(["sumo", "-c", sumo_config_path])

#     # Ensure the simulation is running
#     if not traci.simulation.getMinExpectedNumber() > 0:
#         raise RuntimeError("Simulation is not running. Please start the simulation first.")

#     try:
#         # Get the ID of the traffic light logic for the junction
#         tl_logic_ids = traci.trafficlight.getIDList()
#         print(f"Traffic light logic IDs: {tl_logic_ids}")

#         for tl_id in tl_logic_ids:
#             # Check if the traffic light logic ID is associated with the junction
#             if junction_id in tl_id:
#                 # Get the current state of the traffic light
#                 state = traci.trafficlight.getRedYellowGreenState(tl_id)
#                 return state

#     except Exception as e:
#         raise RuntimeError(f"An error occurred while retrieving the traffic signal state: {e}")

#     finally:
#         # Close the TraCI connection
#         traci.close()

#     raise ValueError(f"No traffic light logic found for junction ID: {junction_id}")

# def add_or_update_tl_logic(file_path, junction_id):
#     """
#     Add or update the traffic light logic for the specified junction ID in the map.net.xml file.

#     :param file_path: Path to the map.net.xml file.
#     :param junction_id: The ID of the junction where the traffic light logic needs to be added or updated.
#     """

#     try:
#         # Get the current state of the traffic signal
#         state = get_traffic_signal_state(junction_id, file_path)
#         print(f"Current state of the traffic signal for junction {junction_id}: {state}")

#         num_lanes = len(state)  # Determine the number of lanes from the state string

#         print(f"Loading XML file from: {file_path}")
#         tree = ET.parse(file_path)
#         root = tree.getroot()

#         # Define the state string based on the number of lanes
#         state = 'r' * num_lanes
#         print(f"State string for {num_lanes} lanes: {state}")

#         # Create the tlLogic element
#         tl_logic = ET.Element('tlLogic', id=junction_id, type='static', programID='all_red', offset='0')
#         phase = ET.SubElement(tl_logic, 'phase', duration='100000000', state=state)

#         # Check if there is already a tlLogic element for this junction
#         existing_tl_logic = False
#         print(f"Checking for existing tlLogic element for junction ID: {junction_id}")

#         for elem in root.findall('tlLogic'):
#             if elem.get('id') == junction_id:
#                 existing_tl_logic = True
#                 print(f"Existing tlLogic found for junction ID: {junction_id}, updating...")
#                 # Remove existing element and replace with updated one
#                 root.remove(elem)
#                 # Append the updated tlLogic element
#                 root.append(tl_logic)
#                 break

#         if not existing_tl_logic:
#             print(f"No existing tlLogic found for junction ID: {junction_id}, adding new...")
#             # Append the new tlLogic element if it does not exist
#             root.append(tl_logic)

#         # Write the changes back to the file
#         print(f"Writing changes to XML file: {file_path}")
#         tree.write(file_path, encoding='utf-8', xml_declaration=True)

#         print(f"Updated or added tlLogic for junction {junction_id}.")
    
#     except Exception as e:
#         print(f"Error: {e}")


        

if __name__ == "__main__":
    junction_id = "8540581958"  # Replace with your junction ID
    config_path = "E:\\finale-submission\\backend\\config"
    net_file = os.path.join(config_path,"map.net.xml") # Replace with the path to your net.xml file

    add_traffic_signal_to_junction(junction_id,net_file)
