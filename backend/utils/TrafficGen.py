import os
import subprocess

#traffic Generator using the ActivityGen algorithm from SUMO
def TrafficGenerator(Randomtrips,config_folder_path):

    print(f'[*] Received Random trips {Randomtrips}')

    sumo_network_filepath = os.path.join(config_folder_path, 'map.net.xml')
    output_file_path_ActivityGen = os.path.join(config_folder_path, 'routes.rou.xml')
    output_file_path_RandomTrips = os.path.join(config_folder_path, 'trips.trips.xml')
    duorouter_generated_file_path = os.path.join(config_folder_path, 'Final_routes.rou.xml')

    randomTripspy_path = os.path.join("C:\\Program Files (x86)\\Eclipse\\Sumo\\tools","randomTrips.py")

    print()
    print(f'[*] Generating RandomTrips : {Randomtrips}....')
    
    subprocess.run(['python', randomTripspy_path, '--net-file', sumo_network_filepath, '-e', Randomtrips],
                   cwd=config_folder_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print('[*] executing duorouter...')
    try:
        subprocess.run(['duarouter', '--net-file', sumo_network_filepath, '--route-files', output_file_path_RandomTrips, '--output-file', duorouter_generated_file_path, '--ignore-errors'],
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
    return {'message': 'Data received and stored in XML file'}