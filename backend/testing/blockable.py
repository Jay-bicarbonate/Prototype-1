import os
import sumolib
import traci

# Set the path to your SUMO binary
sumo_binary = r'C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo.exe'

# Set the path to your simulation files
network_file = r'E:\\finale-submission\\backend\\config\\map.net.xml'
route_file = r'E:\\finale-submission\\backend\\config\\Final_routes.rou.xml'
config_file = r'E:\\finale-submission\\backend\\config\\main_sim.sumocfg'

# Start the SUMO simulation
traci.start([sumo_binary, '-c', config_file])

# Get the road network
net = sumolib.net.readNet(network_file)

# Get the list of edges (roads) in the network
edges = net.getEdges()

# Create a list to store the edges that can be blocked
blockable_edges = []

# Iterate through the edges and check if blocking them will not cause a connectivity issue
for edge in edges:
    # Disable the current edge
    current_allows = edge.allows('passenger')
    edge.allows('none')
    print(f"Checking edge: {edge.getID()}")
    
    # Try to find a route from all vehicles
    try:
        for vehicle in traci.vehicle.getIDList():
            traci.vehicle.rerouteHelper(vehicle, True)
    except traci.exceptions.TraCIException:
        # If there's an exception, it means the edge cannot be blocked
        print(f"Cannot block edge: {edge.getID()}")
        edge.allows(current_allows)
        continue
    
    # Check if there are alternative routes for all vehicles
    has_alternative_routes = True
    for vehicle in traci.vehicle.getIDList():
        if len(traci.vehicle.getEdges(vehicle)) == 1:
            has_alternative_routes = False
            break
    
    if has_alternative_routes:
        # If we reach this point, the edge can be blocked
        print(f"Can block edge: {edge.getID()}")
        blockable_edges.append(edge.getID())
    else:
        print(f"Cannot block edge: {edge.getID()} (no alternative routes)")
    
    # Restore the edge's access
    edge.allows(current_allows)

# Close the SUMO simulation
traci.close()

print("Blockable road IDs:", blockable_edges)

# Verify the blockable roads
for blockable_edge in blockable_edges:
    # Start the SUMO simulation
    traci.start([sumo_binary, '-c', config_file])
    
    # Get the road network
    net = sumolib.net.readNet(network_file)
    
    # Disable the blockable edge
    edge = net.getEdge(blockable_edge)
    current_allows = edge.allows('passenger')
    edge.allows('none')
    
    # Try to find a route from all vehicles
    try:
        for vehicle in traci.vehicle.getIDList():
            traci.vehicle.rerouteHelper(vehicle, True)
    except traci.exceptions.TraCIException:
        # If there's an exception, it means the edge cannot be blocked
        print(f"Cannot block edge: {blockable_edge}")
        edge.allows(current_allows)
        traci.close()
        continue
    
    # If we reach this point, the edge can be blocked
    print(f"Edge {blockable_edge} can be blocked")
    
    # Restore the edge's access
    edge.allows(current_allows)
    
    # Close the SUMO simulation
    traci.close()