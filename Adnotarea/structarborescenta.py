import re
import docx
import os
import json
import jsonpickle


def read_from_file(path):
    try:
        text = ''
        doc = docx.Document(path)
        for line in doc.paragraphs:
            text += line.text
            text+= '\n'
        text2=text.replace("”", "\"");
        with open("adnotari.txt", "a",encoding='utf8') as file:
            file.write("%s" % text2)
        return os.path.splitext(path)[0] + ".txt"
    except IOError:
        print("Couldn't open the file!")


def arbore(fisier):
    adnotare = open(fisier, "rt",encoding='utf8')
    text = adnotare.read()
    result = re.findall("<node parent=\"\s*\w+.*\">\s*\w+.*</node>", text)
    print(result)
    arb = dict()
    for element in result:
        ind1 = element.index("parent=\"") + 8
        ind2 = element.index("\">") - 1
        cheie = element[ind1: ind2+1]
        #print(key)
        ind3 = element.index("\">") + 2
        ind4 = element.index("</node") - 1
        value = element[ind3: ind4+1]
        if cheie in arb:
            arb[cheie].append(value.strip())
        else:
            arb.update({cheie: [value.strip()]})
    return arb

def create_JSON(fisiereDoc, JSONFile):
    class Chapter:
        chapter_count = 0;
        def __init__(self):
            Chapter.chapter_count += 1
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)



    #salveaza intr-un txt doc
    for fisierDoc in fisiereDoc:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, fisierDoc)
        text=read_from_file(path)


    #creare arbore iduri
    nr=1
    arbore_ids = dict()
    for key, value in arbore("adnotari.txt").items():
        if key not in arbore_ids:
            if key=="root" or key=="ROOT":
                arbore_ids[key] = 0;
            else:
                arbore_ids[key] = nr;
                nr = nr + 1

    nr2=nr;

    data={}
    data['chapters']=[]

    chs = []
    for key, value in arbore("adnotari.txt").items():
        for subb in value:
            ch = Chapter()
            ch.name=subb
            if subb not in arbore_ids:
                ch.ID=str(nr2)
                nr2=nr2+1
            else:
                ch.ID=str(arbore_ids[subb])
            ch.parentID=str(arbore_ids[key])
            data['chapters'].append({
                'nume': ch.name,
                'id': ch.ID,
                'parinte': ch.parentID
            })

    #scrie JSON-ul in fisier
    with open('data.json', 'w') as outfile:
        json.dump(data,outfile)


#documentele trebuie sa aiba extensia .docx
create_JSON(["0.docx","3.docx","4.docx","5.docx"], "data.json");

