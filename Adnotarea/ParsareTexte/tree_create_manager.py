import os
from createtree import create_tree_from_xml


dir_path = os.path.dirname(os.path.realpath(__file__))

file_output1 = os.path.join(dir_path, 'DocumenteOutput\\Fisier1.xml')
file_output2 = os.path.join(dir_path, 'DocumenteOutput\\Fisier2.xml')
file_output3 = os.path.join(dir_path, 'DocumenteOutput\\Fisier3.xml')
file_output4 = os.path.join(dir_path, 'DocumenteOutput\\Fisier4.xml')
file_output5 = os.path.join(dir_path, 'DocumenteOutput\\Fisier5.xml')

create_tree_from_xml(file_output1)
create_tree_from_xml(file_output2)
create_tree_from_xml(file_output3)
create_tree_from_xml(file_output4)
create_tree_from_xml(file_output5)
