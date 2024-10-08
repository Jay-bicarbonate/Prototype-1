import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

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

def plot_total_vehicle_heatmap(net_file, netstatedump_file):
    edges = extract_edges_from_net(net_file)
    total_density = calculate_density(netstatedump_file)
    
    # Convert densities to a numpy array for easier manipulation
    density_values = np.array(list(total_density.values()))
    
    # Calculate quartiles
    q1, q3 = np.percentile(density_values, [5, 96])
    
    # Define normalization using quartiles (1.5 * IQR for outliers)
    norm = mcolors.Normalize(vmin=q1, vmax=q3)
    
    # Create a colormap (blue for low traffic density, red for high traffic density)
    cmap = cm.get_cmap('coolwarm')
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Plot each edge with a color based on its density
    for edge_id, density in total_density.items():
        try:
            shape = edges[edge_id]
            x, y = zip(*shape)
            color = cmap(norm(density))
            ax.plot(x, y, color=color, linewidth=2)
        except KeyError:
            # Edge ID might not be in the network file
            pass
    
    # Add a color bar to indicate the density scale
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Total Vehicle Count')
    
    ax.set_title('Total Vehicle Count on Roads')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Rewind the buffer to the beginning

    return img

# net_file = "E:\\finale-submission\\backend\\config\\map.net.xml"
# netstate_file = "E:\\finale-submission\\backend\\config\\netstatedump.xml"

# plot_total_vehicle_heatmap(net_file,netstate_file)