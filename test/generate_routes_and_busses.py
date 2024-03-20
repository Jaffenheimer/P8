import xml.etree.ElementTree as ET
    
routes = ET.Element('routes')
routes.attrib = {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:noNamespaceSchemaLocation' :'http://sumo.dlr.de/xsd/routes_file.xsd'}
all_routes = ["r_0","r_1"]
rightRoads = ["-overlap", "-R2", "-R1", "-R0"] 
leftRoads = ["-overlap", "-L3", "-L2", "-L1", "-L0"]
all_roads = [rightRoads,leftRoads]
vtype = ET.SubElement(routes, 'vType')
vtype.attrib = {'id': 'minibus', 'length': '7.00', 'maxSpeed': '13.90', 'desiredMaxSpeed': '13.90', 'vClass': 'bus', 'personCapacity': '24'}



#generate the routes
for i in range(len(all_routes)):
    route = ET.SubElement(routes, 'route')
    route.attrib = {'id': f'{all_routes[i]}', 'edges': '-overlap -R2 -R1 -R0' if all_routes[i] == "r_0" else '-overlap -L3 -L2 -L1 -L0', 'color': 'yellow' if all_routes[i] == "r_0" else 'blue', 'cycleTime': '300.00', 'repeat': '10'}
    for road in all_roads[i]:
        stop = ET.SubElement(route, 'stop')
        stop.attrib = {'busStop': f'bs_road_{road}', 'duration': '5.00'}

#generate the vehicles
all_vehicles = []
for route in all_routes:
    departTime = 0
    for i in range(5):
        vehicle_dict = {'id': f'bus_{route}_{i}', 'type': 'minibus', 'depart': str(departTime), 'color': 'yellow' if route == "r_0" else 'blue', 'route': route}
        all_vehicles.append(vehicle_dict)
        departTime += 30

# Sort all vehicles by 'depart'
all_vehicles.sort(key=lambda x: int(x['depart']))

# Create XML elements
for vehicle_dict in all_vehicles:
    vehicle = ET.SubElement(routes, 'vehicle')
    vehicle.attrib = vehicle_dict
        
tree = ET.ElementTree(routes)
ET.indent(tree, space="    ")
tree.write('routes_and_busses.xml')