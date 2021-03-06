# coding=utf8
from suds.client import Client
import docx
import os

def read_from_file(path):
    try:
        text = ''
        #doc = docx.Document(path)
        doc=open(path,"r", encoding='utf8')
        for line in doc:
            text += line
        return text
    except IOError:
        print("Couldn't open the file!")

def write_in_file(input, path_output):
    try:
        text = input
        file = open(path_output, "w+", encoding='utf8')
        for i in text:
            file.write(i)
        file.close()
    except IOError:
        print("Couldn't open the file(s)!")

#Legatura cu parser-ul de pe website

client = Client("http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl")
#print (client)
client.set_options(port='FdgParserRoWSPort')


#Folosirea documentelor transformate in format .docx
dir_path = os.path.dirname(os.path.realpath(__file__))
file1 = os.path.join(dir_path, 'DocumenteInput\\t0.txt')
file2 = os.path.join(dir_path, 'DocumenteInput\\t1.txt')
file3 = os.path.join(dir_path, 'DocumenteInput\\t2.txt')
file4 = os.path.join(dir_path, 'DocumenteInput\\t3.txt')
file5 = os.path.join(dir_path, 'DocumenteInput\\t4.txt')


#Primul fisier
response = client.service.parseText(txt=read_from_file(file1))
file_output = os.path.join(dir_path, 'DocumenteOutput\Fisier1.xml')
write_in_file(response, file_output)

#Al 2-lea fisier
response = client.service.parseText(txt=read_from_file(file2))
file_output = os.path.join(dir_path, 'DocumenteOutput\Fisier2.xml')
write_in_file(response, file_output)

#Al 3-lea fisier
response = client.service.parseText(txt=read_from_file(file3))
file_output = os.path.join(dir_path, 'DocumenteOutput\Fisier3.xml')
write_in_file(response, file_output)

#Al 4-lea fisier
response = client.service.parseText(txt=read_from_file(file4))
file_output = os.path.join(dir_path, 'DocumenteOutput\Fisier4.xml')
write_in_file(response, file_output)

#Al 5-lea fisier
response = client.service.parseText(txt=read_from_file(file5))
file_output = os.path.join(dir_path, 'DocumenteOutput\Fisier5.xml')
write_in_file(response, file_output)


#print(read_from_file(path))

#print (response)