import re
import docx
import os

def read_from_file(path):
    try:
        text = ''
        doc = docx.Document(path)
        for line in doc.paragraphs:
            text += line.text
        return text
    except IOError:
        print("Couldn't open the file!")

def arbore(fisier):
    adnotare = open(fisier, "rt",encoding='utf8')
    text = adnotare.read()
    result = re.findall("<node parent=\"\s*\w+.*\">\s*\w+.*</node>", text)
    #print(result)
    arb = dict()
    for element in result:
        ind1 = element.index("parent=\"") + 8
        ind2 = element.index("\">") - 1
        cheie = element[ind1: ind2+1]
        #print(key)
        ind3 = element.index("\">") + 2
        ind4 = element.index("</node") - 1
        value = element[ind3: ind4+1]
        #value.strip()
        #print(value)
        #arb.update({cheie: value})
        if cheie in arb:
            arb[cheie].append(value.strip())
        else:
            arb.update({cheie: [value.strip()]})
    return arb
# dir_path = os.path.dirname(os.path.realpath(__file__))
# path = os.path.join(dir_path,"3.VASCULAR2012_corr.docx")
# print(path)
# text=read_from_file(path)
print(arbore("adnotari.txt"))

