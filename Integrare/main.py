from flask import Flask, render_template
from flask import request
import requests
import os
import validators
import FindDefinition
import WikiTextImage

app = Flask(__name__)
lista = [("inima", "este un organ al corpului", "../static/john"), ("inima", "este un organ special")]


@app.route("/")
def index():
    return render_template("finalPage.html", dialogue=list())


@app.route("/<dialogue>", methods=["POST", "GET"])
def discutie(dialogue=None):
    query = request.form["querry"]
    print(query)
    print("1 + ", query)  # aici se afla intrebarea pusa pe site
    # sub,prop=FindDefinition.get_prop(query,0)
    ok, theme = WikiTextImage.safe_extaractContent(query)
    # lista=[(sub,prop,None)]
    if ok:
        find_An_Img = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path,"static")
        path_dir = os.path.join(dir_path,theme)
        print(path_dir)
        print(os.path.isdir(path_dir))
        img_name = ""
        find_text = False
        txt_name = ""
        images=[]
        nr_images=0
        for fille in os.listdir(path_dir):
            if fille.endswith(".png") or fille.endswith(".jpg"):
                if not find_An_Img:
                    img_name = fille
                    find_An_Img = True
                    print(fille, "\n")
                else:
                    images.append("../static/" +theme+"/"+fille)
                    nr_images=nr_images+1
            if fille.endswith(".txt"):
                if not find_text:
                    txt_name = fille
                    find_text = True
                    print(fille, "\n")
        if find_An_Img:
            path_img = "../static/" +theme+"/"+img_name
        else:
            path_img = None

        path_txt=path_dir + "\\" + txt_name
        print(path_txt)
        with open(path_txt, 'r',encoding='utf-8') as f:
            read_data = f.readline()
            read_line = f.readline()
            nrlines=1
            lines=[]
            for a_line in f:
                lines.append((a_line))
                nrlines+=1
            print(lines)
            lista = [(query,read_data, path_img,lines,images,range(1,nr_images))]
    else:
        lista = [(query, query + query, None)]
    # as vrea ca in lista sa fi pusa o lista de tuple de forma: (nume topic, text, cale_imagine)
    # cale_imagine o sa fie ca calea spre imagine daca exista, None caz contrar
    #return render_template("mainPage.html", dialogue=lista)
        return render_template("secondPage.html", dialogue=lista)


if __name__ == "__main__":
    app.run()
