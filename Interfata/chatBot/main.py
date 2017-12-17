from flask import Flask, render_template
from flask import request
import requests
import  validators
app = Flask(__name__)
lista = [("inima","este un organ al corpului","../static/john"),("inima","este un organ special")]



@app.route("/")
def index():
    return render_template("mainPage.html", dialogue=list())

@app.route("/<dialogue>", methods = ["POST","GET"])
def discutie(dialogue = None):
    query = request.form["querry"]
    print(query) #aici se afla intrebarea pusa pe site
    #as vrea ca in lista sa fi pusa o lista de tuple de forma: (nume topic, text, cale_imagine)
    #cale_imagine o sa fie ca calea spre imagine daca exista, None caz contrar
    return render_template("mainPage.html", dialogue=lista)


if __name__=="__main__":
    app.run()