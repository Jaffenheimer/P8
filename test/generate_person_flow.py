import xml.etree.ElementTree as ET

routes = ET.Element('routes')
routes.attrib = {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:noNamespaceSchemaLocation' :'http://sumo.dlr.de/xsd/routes_file.xsd'}

rightRoute = ["-overlap", "-R2", "-R1", "-R0"] 
busLocationDict={"-overlap": "123", "-R2": "259", "-R1": "125", "-R0": "267", "-L3": "117", "-L2": "110", "-L1": "123", "-L0": "120"}

leftRoute = ["-overlap", "-L3", "-L2", "-L1", "-L0"]

allRoutes = [leftRoute,rightRoute]


for route in allRoutes:
    for i in range(len(route)): 
        for j in range(len(route)):
            if i==j:
                continue
            personFlow = ET.SubElement(routes, 'personFlow')
            # 86400 is 24 hours in seconds
            personFlow.attrib = {'id': f'person_from_{route[i]}_to_{route[j]}', 'begin': '0.00', 'end':'86400', 'probability': '0.05', 'departPos': busLocationDict[route[i]]}
            # walk = ET.SubElement(personFlow, 'walk')
            # walk.attrib = {'from': leftRoute[i], 'to': leftRoute[i]}
            ride = ET.SubElement(personFlow, 'ride')
            ride.attrib = {'from': route[i], 'to': route[j]}
     
     
        


tree = ET.ElementTree(routes)
ET.indent(tree, space="    ")
tree.write('person_flow.xml')