import collections
from lxml import etree
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_output = os.path.join(dir_path, 'DocumenteOutput\\Fisier2.xml')

tree = etree.parse(file_output)
dictionary = collections.OrderedDict()

#Obtinem FDG_Output si display
root = tree.getroot()
#dictionary["file_root"] = "[0][" + root.tag + "]"

# Get tabs seeing element's importance in text

def element_position(position):
    text = ''
    for index in range(0, position):
        text += '\t'
    return text

def get_path_for_element(element, root):
    if element.get('head') == '0':
        return 2
    else:
         for nodes in range(0, len(root)):
             if root[nodes] != element:
                 if element.get('head') == str(nodes + 1):
                     return get_path_for_element(root[nodes], root) + 1

#def search_element_position(element, root):
 #   for

#Obtinem root-urile

def get_children(element, root):
    list = []
    for nodes in range(0, len(root)):
        if root[nodes] != element:
            if get_path_for_element(root[nodes], root) == (get_path_for_element(element, root) + 1):
                list.append(root[nodes])
    return list

print("[0]" + str(root.tag))

for roots in root:
    print("\n\n\t[1][" + str(roots.tag) + "]" + str(roots.items()[0]))
    #dictionary["[1][" + str(roots.tag) + "]" + str(roots.items()[0])]
    for elements in range(0, len(roots)):
        print(get_children(roots[elements], roots))
        #if element_position()
       # dictionary[roots[elements].text] =
        #print(element_position(get_path_for_element(roots[elements], roots)) + "[" + str(get_path_for_element(roots[elements], roots)) + "] " + roots[elements].text)

#Root-ul
#for roots in tree.getroot():
    #print("\t[1][" + str(roots.tag) + "]" + str(roots.items()[0]))
  #  dictionary[str(roots.items()[0])] = "\t[1][" + str(roots.tag) + "]" + str(roots.items()[0])
  #  for index in roots:
       # if index.text.isalpha():
        #    if index.get('deprel') in ("sbj.", "ROOT"):
          #      dictionary[index.get('id')] = "\t\t[2] " + str(index.text)
            #    #print("\t\t[2] " + str(index.text))
          #  else:
              #  dictionary[index.get('id')] = "\t\t\t[3] " + str(index.text)
                #print("\t\t\t[3] " + str(index.text))
            #if index.items().attrib[0]:
              #  print("da")
                # if attritubes[0] == "deprel":
                #     if attritubes[1] == "sbj.":
                #         print("\t\t[2] " + str(index.text))
                #     if attritubes[1] == "ROOT":
                #         print("\t\t[2] " + str(index.text))
                # else:
                #     print("\t\t\t[3] " + str(index.text))
    #print(index.items())
#   #path = tree.getpath()
   # if index.text.isalpha():
    #   dictionary[index.text] = index.items()
  ##path = tree.text
  #print(path)
  # position = str(tree.getpath(index).count('/')  - 1)
  # print("[" + str(position) + "]: " + index.text)
  # for elements in index.items():
     #   if elements[0] == "deprel":
     #       if elements[1] in ("sbj.", "ROOT"):
         #       print(elements[1])
  # print("\n")

#for i in dictionary.items():
  #  print(i[1])

#print(tree.getpath(etree.Element("PROBLEMATICA")))

# print("[0] " + root.tag + ":")
#
# for elements in dictionary.items():
#     #print("Dict: " + str(elements[0]) + "\n")
#     for attritubes in elements[1]:
#         if attritubes[0] == "deprel":
#             if attritubes[1] == "sbj.":
#                 print("\t[1] " + str(elements[0]))
#             if attritubes[1] == "ROOT":
#                 print("\t[1] " + str(elements[0]))
