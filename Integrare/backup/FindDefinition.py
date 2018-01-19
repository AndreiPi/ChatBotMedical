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

def searchprops(sub,pred,propoz):
    bestS = 9999
    bestP = 9999
    bestProp=""
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
    return sub,bestProp,bestP,bestS

def ChooseProp(propoz,search,fileindex,depth):


    #print(search[0])
   # print(search[0][0])
    pred=search[0][0]["S"][0][1]
    sub=search[0][0][pred][0][1]
    subj=[]
    subj.append(sub)
    try:
        compl=search[0][0][pred][1][1]
        subj.append(compl)
    except :
        compl=""
    try:
        atrib=search[0][0][compl][0][1]
        subj.append(atrib)
    except:
        atrib=""

    print(sub,pred,compl,atrib)




    props=set()
    if sub not in ["care","ce","unde","cand","cum"]:
        s_s, bestProp_s, bp_s, bs_s = searchprops(sub, pred, propoz)
        props.add(bestProp_s)
    else :
        if compl!="":
            s_c, bestProp_c, bp_c, bs_c = searchprops(compl, pred, propoz)
            props.add(bestProp_c)
        if atrib!="":
            s_a, bestProp_a, bp_a, bs_a = searchprops(atrib, pred, propoz)
            props.add(bestProp_a)

    moreprops=set()
    if depth<1:
        for p in props:
            mp=get_prop(p,fileindex,depth+1)[1]
            moreprops.add(p)
            for m in mp:
                moreprops.add(m)

   # if frozenset(moreprops):
   #     props.add(frozenset(moreprops))
    #print(moreprops)
    return subj,moreprops


    #print(propoz)


def get_prop(input,fileIndex,depth):
    create_XML(input)
    #file1=createtree.get_list_of_dictionaries("DocumenteOutput/Fisier1.xml")
    #createtree.pickleIT(file1)
    searchDict=createtree.get_list_of_dictionaries("search.xml")
    pklFileName="dictionaries_list_Fisier"
    fileDict=[]
    #subj=[]
    #mp=set()
    for i in range(1,6):
        name=os.path.join("Fisiere_pkl",pklFileName+str(i)+".pkl")
        with open(name,"rb") as f:
            fileDict.append(pickle.load(f, encoding="bytes"))
    #print(searchDict)
    #print(fileDict[fileIndex])
    subj,mp=ChooseProp(fileDict[fileIndex],searchDict,fileIndex,depth)
    #print(mp)
    return subj,mp



#print(get_prop("Care este compozitia sangelui din cutia craniana?",1,0))



