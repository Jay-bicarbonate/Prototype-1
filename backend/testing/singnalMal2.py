import xml.etree.ElementTree as ET

def add_tl_logic_to_junction(net_file, junction_id):
    # Parse the XML file
    tree = ET.parse(net_file)
    root = tree.getroot()

    # Find the junction element with the given junction_id
    junction = root.find(f"./junction[@id='{junction_id}']")
    if junction is None:
        print(f"Junction with ID {junction_id} not found in the net file.")
        return

    # Update the junction type to 'traffic_light'
    junction.set('type', 'traffic_light')

    # Count the number of <request> tags within the junction
    request_tags = junction.findall('request')
    num_states = len(request_tags)

    if num_states == 0:
        print(f"No <request> tags found for junction {junction_id}.")
        return

    # Create the <tlLogic> tag with all red states
    tl_logic = ET.Element('tlLogic', attrib={
        'id': junction_id,
        'type': 'static',
        'programID': '0',
        'offset': '0'
    })
    state = 'r' * num_states
    ET.SubElement(tl_logic, 'phase', attrib={'duration': '16', 'state': state})

    # Insert the <tlLogic> tag before the first junction element
    first_junction_index = next((i for i, elem in enumerate(root) if elem.tag == 'junction'), None)
    if first_junction_index is not None:
        root.insert(first_junction_index, tl_logic)
    else:
        # If there are no junctions, append it to the root
        root.append(tl_logic)

    # Write back to the net.xml file
    tree.write(net_file, encoding='UTF-8', xml_declaration=True)
    print(f"tlLogic added to junction {junction_id} with {num_states} states all set to 'r'.")
    print(f"Junction type updated to 'traffic_light'.")

# Example usage
net_file = 'E:\\finale-submission\\backend\\config\\map.net.xml'  # Update this path to your actual net.xml file
junction_id = '8540581958'  # Replace with the actual junction ID you want to modify
add_tl_logic_to_junction(net_file, junction_id)
