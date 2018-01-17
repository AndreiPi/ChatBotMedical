from flask import Flask, render_template
from flask import request
import requests
import os
import validators
import FindDefinition
import WikiTextImage
import integrareAiml as ia
import time

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("finalPage.html", dialogue=history)


@app.route("/<dialogue>", methods=["POST", "GET"])
def discutie(dialogue=None):
    global history
    query = request.form["querry"]
    print(query)
    # Obtinem data curenta + mesajul userului, astfel vom avea formatul: [Data][User] : [mesaj_user] si [Data][Bot] : [raspuns_bot]
    localtime = time.asctime(time.localtime(time.time()))
    currentInput = ("[" + localtime + "] User", query)

    #Introducere in dictionar a formatului corect
    history.append(currentInput)

    nrOfWords = query.split(" ")

    if len(nrOfWords) > 2:
        sub, prop = FindDefinition.get_prop(query, 0)
        if len(prop) > 0:
            history.append(("[" + localtime + "] Bot", prop, None))
        else:
            history.append(("[" + localtime + "] Bot", "Nu am gasit prin textele adnotate!", None))
    else:
        ok = WikiTextImage.extractContent(query)
        theme = query

        if ok:
            find_An_Img = False
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.join(dir_path,"static")
            path_dir = os.path.join(dir_path,theme)
            img_name = ""
            find_text = False
            txt_name = ""
            images=[]
            nr_images=0
            print("VERIFICARE LOOP")
            for fille in os.listdir(path_dir):
                if fille.endswith(".png") or fille.endswith(".jpg") or fille.endswith(".jpeg"):
                    if not find_An_Img:
                        img_name = fille
                        find_An_Img = True
                    else:
                        images.append("../static/" +theme+"/"+fille)
                        nr_images=nr_images+1
                if fille.endswith(".txt"):
                    if not find_text:
                        txt_name = fille
                        find_text = True
            if find_An_Img:
                path_img = "../static/" +theme+"/"+img_name
            else:
                path_img = None

            path_txt=path_dir + "\\" + txt_name
            print(path_txt)
            with open(path_txt, 'r',encoding='utf-8') as f:
                read_data = f.readline()
                nrlines=1
                lines=[]
                for a_line in f:
                    lines.append((a_line))
                    nrlines+=1
                history += [(query, read_data, path_img,lines,images,range(0,nr_images))]

   # else:
        #lista = [(query, query + query, None)]
       # lista = [(sub, prop, None)]
    # as vrea ca in lista sa fi pusa o lista de tuple de forma: (nume topic, text, cale_imagine)
    # cale_11imagine o sa fie ca calea spre imagine daca exista, None caz contrar
    #return render_template("mainPage.html", dialogue=lista)
    print(history)
    return render_template("finalPage.html", dialogue=history)


if __name__ == "__main__":
    app.run()
