from flask import Flask, render_template
from flask import request
import requests
import os
import validators
import FindDefinition
import WikiTextImage
import integrareAiml as ia
import datetime

app = Flask(__name__)
lista = []

def getLatestInputs(lista):
    latestInputs = []
    for i in lista[-3:]:
        latestInputs.append(i)
    return latestInputs

@app.route("/")
def index():
    return render_template("finalPage.html", dialogue=lista)


@app.route("/<dialogue>", methods=["POST", "GET"])
def discutie(dialogue=None):
    global lista
    query = request.form["querry"]
    print(query)

    #Adaugam data/timpul curent
    now = datetime.datetime.now()
    localtime = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " - " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    if query[len(query)-1] in  "?!.":
        query=query[:-1
              ]
    if ' ' in query:
        try:
            sub,prop=FindDefinition.get_prop(query,0,0)
            subject = next(iter(sub))
        except Exception as e :
            subject = query
            sub = query
            prop = ""
            #raise e



    abspath = os.path.abspath(os.path.dirname(__file__))
    fname=os.path.join(abspath,"termeni.txt")
    with open(fname,"r") as f:
        terms=f.read().lower()
        for s in sub:
            if s in terms:
                subject=s
                break
    # lista=[(sub,prop,None)]
    print(sub, subject)
    #Cautat prin aiml
    aimlResponse = ia.respond(query)
    #print(aimlResponse)

    #Cautat prin wiki
    try:
        ok = WikiTextImage.extractContent(subject)
    except:
        ok=False
    theme = subject
    bookresponse=""
    for p in prop:
        bookresponse+=p+"\n"

    if ok:
        find_An_Img = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path,"static")
        path_dir = os.path.join(dir_path,theme)
        #print(path_dir)
        #print(os.path.isdir(path_dir))
        img_name = ""
        find_text = False
        txt_name = ""
        images=[]
        nr_images=0
        for fille in os.listdir(path_dir):
            if fille.endswith(".png") or fille.endswith(".jpg") or fille.endswith("jpeg"):
                if not find_An_Img:
                    img_name = fille
                    find_An_Img = True
                    #print(fille, "\n")
                else:
                    images.append("../static/" +theme+"/"+fille)
                    nr_images=nr_images+1
            if fille.endswith(".txt"):
                if not find_text:
                    txt_name = fille
                    find_text = True
                    #print(fille, "\n")
        if find_An_Img:
            path_img = "../static/" +theme+"/"+img_name
        else:
            path_img = None

        path_txt=path_dir + "\\" + txt_name
        #print(path_txt)
        with open(path_txt, 'r',encoding='utf-8') as f:
            read_data = f.readline()
            nrlines=1
            lines=[]
            for a_line in f:
                lines.append((a_line))
                nrlines+=1
            #print(lines)

            #Aici adaugam toate raspunsurile din aiml, texte adnotate & wiki
            #Astfel, aimlResponse va avea in secondPage item[2], read_data va avea item[3], etc.
            #lista va fi de forma: (user/bot, raspuns_aiml, raspuns_wiki, cale_imagine)

            lista += [(query, read_data, path_img,lines,images,range(1,nr_images), len(lista) + 1, aimlResponse+"\n"+bookresponse)]
            #lista += [("", read_data, path_img, lines, images, range(1, nr_images),
             #          len(lista) + 1, aimlResponse)]
    else:
        lista += [(query, "",aimlResponse + "\n" + bookresponse)]
        #lista = [(sub, prop, None)]
    # as vrea ca in lista sa fi pusa o lista de tuple de forma: (nume topic, text, cale_imagine)
    # cale_11imagine o sa fie ca calea spre imagine daca exista, None caz contrar
    #return render_template("mainPage.html", dialogue=lista)
    return render_template("secondPage.html", dialogue=getLatestInputs(lista))


if __name__ == "__main__":
    app.run()
