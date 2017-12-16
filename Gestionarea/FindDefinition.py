#import queue
import createtree
import pickle
from queue import Queue
from suds.client import Client

def create_XML(input):
    client = Client("http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl")
    # print (client)
    client.set_options(port='FdgParserRoWSPort')
    response = client.service.parseText(txt=input)
    f=open("search.xml","w")
    f.write(response)
    f.close()
    return response








def ChooseProp(propoz,search):
    bestS=9999
    bestP=9999
    bestProp=""
    #print(search[0][0])
    pred=search[0][0]["S"][0][1]
    sub=search[0][0][pred][0][1]
    print(sub,pred)
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
                print(cuv)
                if cuv[1]==sub and depth<minS:
                    minS=depth
                if cuv[1]==pred and depth<minP:
                    minP=depth
                if cuv[1] in dict.keys():
                    queue.put(dict[cuv[1]])
            print(" ")
        if minS+minP<bestS+bestP:
            bestS=minS
            bestP=minP
            bestProp=prop
        print(" ")
    return bestProp
def get_prop(input):
    print(create_XML(input))
    #file1=createtree.get_list_of_dictionaries("DocumenteOutput/Fisier1.xml")
    #createtree.pickleIT(file1)
    searchDict=createtree.get_list_of_dictionaries("search.xml")
    with open("dictionaries_list.pkl","rb") as f:
        fileDict=pickle.load(f, encoding="bytes")
    print(searchDict)
    p=ChooseProp(fileDict,searchDict)
    print(p)
    return p




