import xml.etree.ElementTree as ET

def block_road(file_path, road_id):
    # Parse the XML file
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print(f"Successfully parsed XML file: {file_path}")
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return

    # Find the edge with the given road ID
    edge_found = False
    for edge in root.findall('edge'):
        if edge.get('id') == road_id:
            edge_found = True
            print(f"Found edge with id: {road_id}")
            
            # Update disallow attribute for all lanes within this edge
            for lane in edge.findall('lane'):
                lane.set('disallow', 'all')  # Blocking all vehicle types
                print(f"Updated disallow attribute for lane: {lane.get('id')}")
            break

    if not edge_found:
        print(f"Edge with id {road_id} not found in the XML file.")
        return

    # Write the modified XML back to the file
    try:
        tree.write(file_path, xml_declaration=True, encoding='utf-8', method="xml")
        print(f"Successfully wrote changes to XML file: {file_path}")
    except Exception as e:
        print(f"Error writing XML file: {e}")

# Example usage
file_path = 'E:\\finale-submission\\backend\\config\\map.net.xml'
road_id = '31'
block_road(file_path, road_id)
