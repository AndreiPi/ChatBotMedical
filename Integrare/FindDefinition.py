#import queue
import createtree
import os
import pickle
from queue import Queue
from suds.client import Client

def create_XML(input):
    client = Client("http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl")
    # print (client)
    client.set_options(port='FdgParserRoWSPort')
    response = client.service.parseText(txt=input)
    f=open("search.xml","w",encoding="utf-8")
    f.write(response)
    f.close()
    return response



def ChooseProp(propoz,search):
    bestS=9999
    bestP=9999
    bestProp=""
    #print(search[0])
    pred=search[0][0]["S"][0][1]
    sub=search[0][0][pred][0][1]
    print(sub,pred)


    #print(propoz)
    for dict,prop in propoz:
        queue = Queue()
        queue.put(dict["S"])
        depth=0
        minS=9999
        minP=9999
        while not queue.empty() and depth < 100:
            depth+=1
            node=queue.get()
            for cuv in node:
                if cuv[1]==sub and depth<minS:
                    minS=depth
                if cuv[1]==pred and depth<minP:
                    minP=depth
                if cuv[1] in dict.keys():
                    queue.put(dict[cuv[1]])
        if minS+minP<bestS+bestP:
            bestS=minS
            bestP=minP
            bestProp=prop
    return sub,bestProp

def get_prop(input,fileIndex):
    create_XML(input)
    #file1=createtree.get_list_of_dictionaries("DocumenteOutput/Fisier1.xml")
    #createtree.pickleIT(file1)
    searchDict=createtree.get_list_of_dictionaries("search.xml")
    pklFileName="dictionaries_list_Fisier"
    fileDict=[]
    for i in range(1,6):
        name=os.path.join("Fisiere pkl",pklFileName+str(i)+".pkl")
        with open(name,"rb") as f:
            fileDict.append(pickle.load(f, encoding="bytes"))
    #print(searchDict)
    p=ChooseProp(fileDict[fileIndex],searchDict)
    print(p)
    return p



#get_prop("Sistemul nervos este alcatuit faina",0)


