import lxml.etree
import lxml.builder 
import xml.etree.ElementTree as ET

# <routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">


# E = lxml.builder.ElementMaker()
ROUTES = ET.Element('routes')
ROUTES.attrib = {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

# Create a new child element
child = ET.SubElement(ROUTES, 'child')

# Set the attributes of the child element
child.attrib = {'attribute_name': 'attribute_value'}

# Set the text of the child element
child.text = 'child text'


tree = ET.ElementTree(ROUTES)
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