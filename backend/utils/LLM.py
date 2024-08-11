import matplotlib
matplotlib.use('Agg')  # Set the Matplotlib backend to 'Agg' for non-GUI usage

def LLM(prompt, netstate_file):
    print(f"Received Prompt: {prompt}")

    response = f'''
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from io import BytesIO

def generate_plot():
    tree = ET.parse('E:/finale-submission/backend/config/netstatedump.xml')
    root = tree.getroot()

    road_usage = {{}}
    for timestep in root:
        for edge in timestep:
            for lane in edge:
                for vehicle in lane:
                    if vehicle.attrib['id'] not in road_usage:
                        road_usage[vehicle.attrib['id']] = 0
                    road_usage[vehicle.attrib['id']] += float(vehicle.attrib['speed'])

    top_10_roads = sorted(road_usage.items(), key=lambda x: x[1], reverse=True)[:10]

    fig, ax = plt.subplots()
    ax.bar([x[0] for x in top_10_roads], [x[1] for x in top_10_roads])
    ax.set_xlabel('Road ID')
    ax.set_ylabel('Usage')
    ax.set_title('Top 10 Most Busy Roads')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img
'''

    # Execute the dynamically generated function definition
    print('Executing the function !!')
    exec(response, globals())

    print('Execution successfull')

    # Now you can call the dynamically generated function
    print("Calling the function ...")
    generated_img = generate_plot()

    print("done , returning img")
    return generated_img


