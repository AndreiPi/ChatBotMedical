import re


def arbore(fisier):
    adnotare = open(fisier, "rt")
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


#print(arbore("adnotareTest.txt"))

