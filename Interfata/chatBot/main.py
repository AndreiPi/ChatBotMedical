from flask import Flask, render_template
from flask import request
import requests
import  validators
app = Flask(__name__)
lista = [("Inima", "Inima sau cordul este organul reprezentativ al aparatului cardiovascular, ea fiind situată în cutia toracică. Are un rol vital în circulația sângelui și implicit în menținerea vieții.","../static/inima.jpg"),("inima","Inima este localizată la nivelul toracelui,în mediastinul mijlociu, o treime din aceasta fiind localizată la dreapta față de linia mediană și două treimi fiind localizate la stânga liniei mediene.")]



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