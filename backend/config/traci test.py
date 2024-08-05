import traci
import traci.constants as tc
import matplotlib.pyplot as plt
import numpy as np

# Path to your sumo executable
sumoBinary = "sumo"  # or "sumo" for non-GUI version
sumoConfig = "test.sumocfg"  #this is sumo config file which will contain the address of network file , routes file , time start , time end etc

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

# Normalize counts for heatmap visualization
counts = np.array(counts)
normalized_counts = counts / counts.max()

# Visualization using matplotlib
# plt.figure(figsize=(10, 5))
# plt.bar(roads, normalized_counts, color='orange')
# plt.xlabel('Roads')
# plt.ylabel('Normalized Vehicle Count')
# plt.title('Heatmap of Vehicle Counts per Road')
# plt.xticks(rotation=90)
# plt.show()
