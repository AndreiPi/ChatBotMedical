from flask import Flask, render_template
from flask import request
import requests
import  validators
app = Flask(__name__)


@app.route("/")
def profile():
    return render_template("mainPage.html")


if __name__=="__main__":
    app.run()