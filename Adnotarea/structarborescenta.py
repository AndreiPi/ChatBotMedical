# -*- coding: utf-8 -*-
# encoding=utf8
# decoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import docx
import os
import json


def read_from_file(path):
    try:
        text = ''
        doc = docx.Document(path)
        for line in doc.paragraphs:
            text += line.text
            text+= '\n'
        text2=text.replace("”", "\"");
        with open("adnotari.txt", "a") as file:
            file.write("%s" % text2)
        return os.path.splitext(path)[0] + ".txt"
    except IOError:
        print("Couldn't open the file!")

def arbore(fisier):
    adnotare = open(fisier, "rt")
    text = adnotare.read()
    result = re.findall("<node parent=\"\s*\w+.*\">\s*\w+.*</node>", text)
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

    # preview pt capitole (e preview separat doar pt capitolele principale,
    # nu si pentru subcapitole:
    previews = [
            {
                'titlu': "PROBLEMATICA NEUROCHIRURGIEI",
                'id': "?",
                'prop': "Neurochirurgia este o ramură a ştiinţelor medicale care se ocupă cu tratamentul patologiei sistemului nervos şi a învelişurilor sale care poate avea indicaţie de intervenţie (chirurgicală)."
            },
            {
                'titlu': "SINDROMUL COMATOS",
                'id': "?",
                'prop': "Criteriul principal pentru a afirma că un pacient se află în stare de comă îl constituie abolirea stării de conştienţă cu absenţa reacţiei de trezire şi orientare. Această definiţie diferenţiază coma de stările de alterare a stării de conştienţă (somnolenţă, confuzie, obnubilare, stupoare, torpoare s.a.). "
            },
            {
                'titlu': "ACCIDENTELE VASCULARE CEREBRALE NEUROCHIRURGIA VASCULARĂ",
                'id': "?",
                'prop': "Fluxul sanguin cerebral este asigurat prin cele două artere carotide interne şi de cele două artere vertebrale care se unesc în trunchiul vertebrobazilar. Ramificaţiile intracraniene ale acestor artere sunt de tip terminal ceea ce conferă o gravitate crescută ocluziilor vasculare cerebrale"
            },
            {
                'titlu': "PATOLOGIA VERTEBROMEDULARĂ NEUROCHIRURGICALĂ",
                'id': "?",
                'prop': "Măduva spinării şi coada de cal, învelite în teaca durală, sunt adăpostite de canalul vertebral. Numeroşi factori (tumori, alunecări sau dislocări osoase traumatice, hernii ale materialului discal, formarea de osteofite, hematoame şi unele infecţii determină compresiuni asupra rădăcinilor nervoase, măduvei spinării, cozii de cal, în interiorul acestui canal îngust şi rigid"
            }
        ]

    #creare arbore iduri
    nr=1
    arbore_ids = dict()
    main_chs = []
    for key, value in arbore("adnotari.txt").items():
        if key not in arbore_ids:
            if key=="root" or key=="ROOT":
                arbore_ids[key] = 0;
                for vl in value:
                    main_chs.append(vl);
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
            #nu are nici un subcapitol -> nu a fost niciodata cheie -> nu e in arbore -> trebuie creat id
            if subb not in arbore_ids:
                ch.ID=str(nr2)
                nr2=nr2+1
            else:
                ch.ID=str(arbore_ids[subb])
            ch.parentID=str(arbore_ids[key])

            propozitie=""
            if (ch.parentID=="0"):
                for idx2, mainCh in enumerate(main_chs):
                        for idx, val in enumerate(previews):
                            if (val['titlu']==mainCh):
                                previews[idx]['id']=ch.ID;
                                propozitie=previews[idx]['prop']

            data['chapters'].append({
                'nume': ch.name,
                'id': ch.ID,
                'parinte': ch.parentID,
                'prop':propozitie
            })
    #scrie JSON-ul in fisier
    with open('data.json', 'w') as outfile:
        json.dump(data,outfile)

#documentele trebuie sa aiba extensia .docx
create_JSON(["0.docx","3.docx","4.docx","5.docx"], "data.json")

