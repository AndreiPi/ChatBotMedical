import os
from lxml import etree
import _pickle as cPickle


def print_spaces(number_of_spaces, index):
    for i in range(0, number_of_spaces):
        print(" ", end='')

    print("[" + str(index) + "]", end='')


def print_hierarchy(root, number_of_spaces=1, index=1):
    if root.lemma is not None:
        print(root.word + " - " + root.lemma + " - " + root.deprel)
    else:
        print(root.word)

    for child in root.children:
        print_spaces(number_of_spaces + 3, index)
        print_hierarchy(child, number_of_spaces + 3, index + 1)


def create_dictionary(node):
    dictionary = dict()

    if len(node.children) > 0:
        if node.lemma:
            dictionary.update({node.lemma: [(node.children[0].deprel, node.children[0].lemma)]})
        else:
            dictionary.update({node.word: [(node.children[0].deprel, node.children[0].lemma)]})

    i = 1
    while i < len(node.children):
        if node.lemma:
            ceva = dictionary[node.lemma]
        else:
            ceva = dictionary[node.word]
        ceva2 = (node.children[i].deprel, node.children[i].lemma)
        ceva.append(ceva2)
        if node.lemma:
            dictionary[node.lemma] = ceva
        else:
            dictionary[node.word] = ceva

        i += 1

    for child in node.children:
        dictionary.update(create_dictionary(child))

    return dictionary


class Node:
    def __init__(self, head, word, lemma, deprel):
        self.head = head
        self.word = word
        self.lemma = lemma
        self.deprel = deprel
        self.parent_node = None
        self.children = []


def get_list_of_dictionaries(path):
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #file_output = os.path.join(dir_path, 'DocumenteOutput\\Fisier1.xml') # Andrei

    tree = etree.parse(path)

    initial = tree.getroot()
    initial_node = Node(None, initial.tag, None, None)

    lista_propozitiilor = []
    nr_prop = -1

    for s in initial:
        nr_prop += 1

        nodes_list = []

        s_node = Node(None, s.tag, None, None)
        s_node.parent_node = initial_node
        initial_node.children.append(s_node)

        lista_propozitiilor.append("")

        for w in s:
            lista_propozitiilor[nr_prop] = lista_propozitiilor[nr_prop] + " " + w.text

            node = Node(w.get('head'), w.text, w.get('LEMMA'), w.get('deprel'))
            nodes_list.append(node)

            if w.get('head') == '0':
                s_node.children.append(node)

        for node in nodes_list:
            if node.head != '0':
                node.parent_node = nodes_list[int(node.head) - 1]
                node.parent_node.children.append(node)
            else:
                continue


    #print("[0]", end='')
    #print_hierarchy(initial_node)

    dictionaries_tuple_list = []

    for root_child in initial_node.children:
        dictionaries_tuple_list.append(create_dictionary(root_child))

    #print(dictionaries_tuple_list)

    #for dic in dictionaries_tuple_list:
    #    print("{")
    #    for x in dic:
    #        print(x + ":" + str(dic[x]))
    #    print("}")

    #for prop in lista_propozitiilor:
    #    print(prop)

    final_list = []

    i = 0
    for dic in dictionaries_tuple_list:
        final_list.append((dic, lista_propozitiilor[i]))

        i += 1

    #print(final_list)



    return final_list

def pickleIT(list):
    with open("dictionaries_list.pkl", "wb") as f:
        f.write(cPickle.dumps(list))
#dir_path = os.path.dirname(os.path.realpath(__file__))
#file_output = os.path.join(dir_path, 'DocumenteOutput\\Fisier1.xml') # Andrei

#print(get_list_of_dictionaries(file_output))
