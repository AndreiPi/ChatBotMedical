import collections
from lxml import etree
import os
import docx

def read_from_file(path):
    try:
        text = ''
        doc = docx.Document(path)
        for line in doc.paragraphs:
             text += line.text
        return text
    except IOError:
        print("Couldn't open the file!")

def write_in_file(listInput, path_output):
    try:
        myList = listInput
        file = open(path_output, "w+", encoding='utf8')
        for item in myList:
            file.write(item)
            file.write('\n')
        file.close()
    except IOError:
        print("Couldn't open the file(s)!")


def textIntoWords(text):
    txt = text
    rList = list()
    txt = txt.lower()
    separators = "!@#$%^&*()_+-=”“{}[];:'\"\\|,./<>?–0123456789"
    for sep in separators:
        txt = txt.replace(sep, " ")
    A=txt.split(' ')
    for item in A:
        if (item not in rList):
            rList.append(item)
    rList.sort()
    return rList

dir_path = os.path.dirname(os.path.realpath(__file__))
file1 = os.path.join(dir_path, 'DocumenteInput\curs0 facultativ introducere diagnostic tehnici urgente_corr.docx')
file2 = os.path.join(dir_path, 'DocumenteInput\\1.hic procese expansive hidrocefalie 2012_corr.docx')
file3 = os.path.join(dir_path, 'DocumenteInput\\2 curscoma tcc 2012_corr.docx')
file4 = os.path.join(dir_path, 'DocumenteInput\\3.VASCULAR 2012_corr.docx')
file5 = os.path.join(dir_path, 'DocumenteInput\\4 vertebromedular 2012_corr.docx')


txt1  = read_from_file(file1)
txt2  = read_from_file(file2)
txt3  = read_from_file(file3)
txt4  = read_from_file(file4)
txt5  = read_from_file(file5)

write_in_file(textIntoWords(txt1),"DocumenteOutput\\ListaCuvinte1.doc")
write_in_file(textIntoWords(txt2),"DocumenteOutput\\ListaCuvinte2.doc")
write_in_file(textIntoWords(txt3),"DocumenteOutput\\ListaCuvinte3.doc")
write_in_file(textIntoWords(txt4),"DocumenteOutput\\ListaCuvinte4.doc")
write_in_file(textIntoWords(txt5),"DocumenteOutput\\ListaCuvinte5.doc")

