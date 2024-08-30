import matplotlib
matplotlib.use('Agg')  # Set the Matplotlib backend to 'Agg' for non-GUI usage
from langchain_community.llms import Ollama 

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

# def return_news_headlines():
#     news_reports = [
#     "Major Traffic Disruption on Race Course Road Following Serious Accident",
#     "Mahatma Gandhi Marg Blocked After Truck and Car Collision",
#     "headline": "heehaww incident on Mahatma Gandhi Marg",
#     "headline": "Ujjain-Indore Road Closed After Truck Overturns in Major Crash"
# ]
#     return news_reports



def news_report_LLM():
    news_reports = [
    {
        "headline": "Major Traffic Disruption on Race Course Road Following Serious Accident",
        "summary": "In a significant traffic disruption this morning, Race Course Road near Junction 21 was blocked after a severe collision between a truck and a car. The truck, which overturned, scattered its cargo across the highway, causing a complete closure of both lanes. Emergency services are currently on the scene, with both drivers being transported to the hospital with non-life-threatening injuries. Commuters are advised to avoid the area and seek alternative routes as traffic is expected to be severely affected for several hours."
    },
    {
        "headline": "Mahatma Gandhi Marg Blocked After Truck and Car Collision",
        "summary": "Mahatma Gandhi Marg has been rendered impassable following a major accident involving a truck and a passenger car near Junction 21. The incident, which occurred around 8:00 AM today, resulted in the truck overturning and spreading debris across the road. Emergency response teams are working to clear the wreckage, and both drivers have been hospitalized. Travelers are warned of significant delays and should plan accordingly."
    },
    {
        "headline": "heehaww incident on Mahatma Gandhi Marg",
        "summary": "A major heehaww breakout happen this morning everyone who lives near Mahatma Gandhi Marg, especially around Junction 21 is happy. The heehaww has affected many hahaha, causing funny jokes around. Utility crews are working to restore sadness. Residents are advised to be happy and expect heehawws everywhere."
    },
    {
        "headline": "Ujjain-Indore Road Closed After Truck Overturns in Major Crash",
        "summary": "Ujjain-Indore Road is closed in both directions near Junction 21 following a major accident involving a truck and a car. The truck overturned upon impact, spilling its cargo and blocking the highway. Authorities are on-site, working to clear the debris and manage the situation. Both drivers have been taken to local hospitals with non-life-threatening injuries. Commuters should expect significant delays and are encouraged to use alternate routes."
    }
]


def get_location_id(location_name):
    location_id = location_dict.get(location_name)
    return location_id


loc_list = []
id_list = []
for report in news_reports:
    llm = Ollama(model="llama3:8b")
    seed = 1
    temperature = 0.0
    prompt = f"""
    from this given news summary I want you to identify the road mentioned in the summary which is causing road blockage and give output as one line string so i can fetch it via request, or for other news meaning which doesn't block the road give output as empty string ''. And don't give any other extra words other than output.
    here is the summary- {report["summary"]}
        """
    loc_data = llm.invoke(prompt, temperature=temperature, seed=seed)
    print(loc_data)
    location_dict = {
        "Race Course Road": "23",
        "Mahatma Gandhi Marg": "87",
        "Mahatma Gandhi Marg": "45",
        "Ujjain-Indore Road": "61"
    }
    print(get_location_id(loc_data))
    id_list.append(get_location_id(loc_data))
    loc_list.append(loc_data)

    print(loc_list)
    print(id_list)

    return [loc_list,id_list]

# news_report_LLM()


