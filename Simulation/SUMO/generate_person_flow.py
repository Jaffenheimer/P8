import xml.etree.ElementTree as ET
import random

routes = ET.Element('routes')
routes.attrib = {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:noNamespaceSchemaLocation' :'http://sumo.dlr.de/xsd/routes_file.xsd'}

busLocationDict={"-overlap": "123", "-R2": "259", "-R1": "125", "-R0": "267", "-L3": "117", "-L2": "110", "-L1": "123", "-L0": "120"}
busStopDict = {"-overlap": "bs_road_-overlap", "-R2": "bs_road_-R2", "-R1": "bs_road_-R1", "-R0": "bs_road_-R0", "-L3": "bs_road_-L3", "-L2": "bs_road_-L2", "-L1": "bs_road_-L1", "-L0": "bs_road_-L0"}
rightRoute = ["-overlap", "-R2", "-R1", "-R0"] 
leftRoute = ["-overlap", "-L3", "-L2", "-L1", "-L0"]

allRoutes = [leftRoute,rightRoute]


for route in allRoutes:
    for i in range(len(route)): 
        for j in range(len(route)):
            if i==j:
                continue
            
            currentRoute = leftRoute if route[i] in leftRoute else rightRoute
            # if route[i] == "-overlap":
            #     if route[j].startswith("-R"):
            #         currentRoute = rightRoute
                    
            
            personFlow = ET.SubElement(routes, 'personFlow')
            # 86400 is 24 hours in seconds
            personFlow.attrib = {'id': f'person_from_{route[i]}_to_{route[j]}', 'begin': '0.00', 'end':'86400', 'probability': f'{round(random.uniform(0.01,0.03),2)}', 'departPos': busLocationDict[route[i]]}
            walk = ET.SubElement(personFlow, 'walk')
            walk.attrib = {'from': currentRoute[i], 'to': currentRoute[i], 'busStop':busStopDict[route[i]] }
            ride = ET.SubElement(personFlow, 'ride')
            ride.attrib = {'from': route[i], 'to': route[j]}
     
     
        


tree = ET.ElementTree(routes)
ET.indent(tree, space="    ")
tree.write('person_flow.xml')