import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import io
from collections import defaultdict
import networkx as nx
from io import BytesIO

# Function to extract edges and their shapes from map.net.xml
def extract_edges_from_net(net_file):
    tree = ET.parse(net_file)
    root = tree.getroot()

    edges = {}
    for edge in root.findall('edge'):
        road_id = edge.get('id')
        shape = edge.find('lane').get('shape')  # Get the shape attribute from the lane
        coordinates = [(float(x), float(y)) for x, y in (point.split(',') for point in shape.split())]
        edges[road_id] = coordinates

    return edges

# Function to calculate total density per edge from netstatedump.xml
def calculate_density(netstate_file):
    tree = ET.parse(netstate_file)
    root = tree.getroot()

    total_density = {}
    for timestep in root.findall('timestep'):
        for edge in timestep.findall('edge'):
            edge_id = edge.get('id')
            if edge_id not in total_density:
                total_density[edge_id] = 0
            for lane in edge.findall('lane'):
                total_density[edge_id] += len(lane.findall('vehicle'))

    return total_density

def total_density_by_road(net_file,netstatedump_file):
    edges = extract_edges_from_net(net_file)
    print(f"Extracted {len(edges)} edges from net file.")

    total_density = calculate_density(netstatedump_file)
    print(f"Calculated densities for {len(total_density)} edges.")

    final_ = {}

    for i in total_density:
        if ":" not in i:
            # print(f"{i} : {total_density[i]}")
            final_[i] = total_density[i]
    
    # print(final_)
    return final_
    print("Done !!")



def plot_total_vehicle_heatmap(net_file, netstatedump_file):
    print("Starting plot_total_vehicle_heatmap...")
    print(f"Net file: {net_file}")
    print(f"Netstate dump file: {netstatedump_file}")

    edges = extract_edges_from_net(net_file)
    print(f"Extracted {len(edges)} edges from net file.")

    total_density = calculate_density(netstatedump_file)
    print(f"Calculated densities for {len(total_density)} edges.")

    # Convert densities to a numpy array for easier manipulation
    density_values = np.array(list(total_density.values()))
    print(f"Density values: {density_values[:10]} (showing first 10 values)")

    # Calculate quartiles
    q1, q3 = np.percentile(density_values, [5, 96])
    print(f"Quartile 1: {q1}, Quartile 3: {q3}")

    # Define normalization using quartiles
    norm = mcolors.Normalize(vmin=q1, vmax=q3)
    print(f"Normalization range: vmin={q1}, vmax={q3}")

    # Create a colormap
    cmap = cm.get_cmap('coolwarm')
    print(f"Colormap: {cmap.name}")

    # Set up the figure
    fig, ax = plt.subplots(figsize=(15, 10))
    print("Figure and axis set up.")

    # Plot each edge with a color based on its density
    for edge_id, density in total_density.items():
        try:
            shape = edges[edge_id]
            x, y = zip(*shape)
            color = cmap(norm(density))
            ax.plot(x, y, color=color, linewidth=2)
        except KeyError:
            print(f"Edge ID {edge_id} not found in edges.")
    
    print("Plotted all edges.")

    # Add a color bar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Total Vehicle Count')
    print("Color bar added.")

    ax.set_title('Total Vehicle Count on Roads')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    print("Title and labels set.")

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Rewind the buffer to the beginning
    print("Plot saved to buffer.")

    return img

def aggregate_vehicle_counts(netfile, networkfile):
    # Step 1: Parse the netstatedump.xml file to get vehicle counts by edge
    tree = ET.parse(netfile)
    root = tree.getroot()

    edge_vehicle_count = defaultdict(int)

    for timestep in root.findall('timestep'):
        for edge in timestep.findall('edge'):
            edge_id = edge.get('id')
            vehicle_count = 0
            for lane in edge.findall('lane'):
                vehicle_count += len(lane.findall('vehicle'))
            edge_vehicle_count[edge_id] += vehicle_count

    # Step 2: Parse the network file to map edge IDs to road types
    tree = ET.parse(networkfile)
    root = tree.getroot()

    edge_to_type = {}

    for edge in root.findall('edge'):
        edge_id = edge.get('id')
        road_type = edge.get('type')
        edge_to_type[edge_id] = road_type

    # Step 3: Aggregate vehicle counts by road type, handling None values
    road_type_vehicle_count = defaultdict(int)

    for edge_id, count in edge_vehicle_count.items():
        road_type = edge_to_type.get(edge_id, "misc")  # Replace None with "misc"
        road_type_vehicle_count[road_type] += count
    # Replace None key with 'misc'
    if None in road_type_vehicle_count:
        road_type_vehicle_count['misc'] = road_type_vehicle_count.pop(None)
        
    # Convert the result to JSON
    return road_type_vehicle_count

def plot_highlighted_roads(net_file, road_id1):
    # Parse the SUMO net.xml file
    tree = ET.parse(net_file)
    root = tree.getroot()

    # Initialize a graph
    G = nx.Graph()

    # Extract edges and their coordinates from the SUMO network file
    for edge in root.findall('edge'):
        edge_id = edge.get('id')
        for lane in edge.findall('lane'):
            shape = lane.get('shape')
            if shape:
                # Parse the shape attribute to get coordinates
                coordinates = shape.split()
                x_coords, y_coords = zip(*[map(float, coord.split(',')) for coord in coordinates])

                # Add nodes and edges to the graph
                for i in range(len(x_coords) - 1):
                    u = (x_coords[i], y_coords[i])
                    v = (x_coords[i+1], y_coords[i+1])
                    if not G.has_node(u):
                        G.add_node(u)
                    if not G.has_node(v):
                        G.add_node(v)
                    G.add_edge(u, v, id=edge_id)

    # Define edge colors and widths
    edge_colors = []
    edge_widths = []
    for u, v, data in G.edges(data=True):
        if data['id'] == road_id1:
            edge_colors.append('RED')  # Bright color for the specified roads
            edge_widths.append(2.5)  # Thicker line width for highlighted roads
        else:
            edge_colors.append('lightgray')  # Lighter color for other roads
            edge_widths.append(1.0)  # Default line width for other roads

    # Draw the graph
    pos = {node: node for node in G.nodes()}  # Use node coordinates as positions
    fig, ax = plt.subplots(figsize=(12, 12))
    nx.draw(G, pos, with_labels=False, edge_color=edge_colors, node_size=10, width=1.5, ax=ax)
    ax.set_title('SUMO Network with Highlighted Roads')

    return fig

net_file = "E:\\finale-submission\\backend\\config\\map.net.xml"
netstate_file = "E:\\finale-submission\\backend\\config\\netstatedump.xml"


# total_density_by_road(net_file,netstate_file)

# plot_total_vehicle_heatmap(net_file,netstate_file)