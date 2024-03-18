import lxml.etree
import lxml.builder 
import xml.etree.ElementTree as ET
from random import randrange

# <routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">


# E = lxml.builder.ElementMaker()
routes = ET.Element('routes')
routes.attrib = {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

"""
 <personFlow id="person" begin="0.00" probability="0.1" departPos="123">
        <!-- <walk from="R0" to="-overlap"/> -->
        <ride from="-overlap" to="-R0"/>
   </personFlow>
"""

leftRoute = ["-overlap", "-R2", "-R1", "-R0"] #len(list)*len(list-1)
busLocationDict={"-overlap": "123", "-R2": "259", "-R1": "125", "-R0": "267"}

id = 0



for i in range(len(leftRoute)): 
    for j in range(len(leftRoute)):
        if i==j:
            continue
        personFlow = ET.SubElement(routes, 'personFlow')
        # Set the attributes of the child element
        personFlow.attrib = {'id': f'person{id}', 'begin': '0.00', 'probability': '0.1', 'departPos': busLocationDict[leftRoute[i]]}
        # walk = ET.SubElement(personFlow, 'walk')
        # walk.attrib = {'from': leftRoute[i], 'to': leftRoute[i]}
        ride = ET.SubElement(personFlow, 'ride')
        ride.attrib = {'from': leftRoute[i], 'to': leftRoute[j]}
        id += 1
        
            

        
        
"""
 <personFlow id="person" begin="0.00" probability="0.1" departPos="123">
        <!-- <walk from="R0" to="-overlap"/> -->
        <ride from="-overlap" to="-R0"/>
   </personFlow>
   """


tree = ET.ElementTree(routes)
ET.indent(tree, space="    ")
tree.write('person_flow.xml')

# DOC = E.doc
# FIELD1 = E.field1
# FIELD2 = E.field2

# the_doc = ROUTES(
#         DOC(
#             FIELD1('some value1', name='blah'),
#             FIELD2('some value2', name='asdfasd'),
#             )   
#         )   

# print(lxml.etree.tostring(the_doc, pretty_print=True))