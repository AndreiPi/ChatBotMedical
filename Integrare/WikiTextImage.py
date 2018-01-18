import wikipedia
import requests
from bs4 import BeautifulSoup
from re import split
import os
import urllib

def extractText(page):
    wikipedia.set_lang("ro")
    try:
        content = wikipedia.page(page).content
        return content
    except wikipedia.exceptions.DisambiguationError:
        lista = [0]
        content = wikipedia.search(page)
        message = ""
        message += "Prea multe optiuni, reincercati cu unul dintre urmatoarele:\n"
        for i in content:
            message += i + "\n"
        lista.extend(message)
        return lista

def extractImages(page):
    wikia = wikipedia.page(page).url
    pageNeeded = requests.get(wikia)
    soup = BeautifulSoup(pageNeeded.text,'html.parser')
    imgTag = soup.find_all('img')
    rezultat = [img['src'] for img in imgTag]
    teme = split(" ",page)
    rezultatFinal = []
    for i in teme:
        for j in rezultat:
            if i in j:
                rezultatFinal.append(j)
    return rezultatFinal


def extractContent(theme):
    directory = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(directory,"static")
    if ( not os.path.exists(directory) ):
        os.makedirs("static")
    os.chdir(directory)
    textContent = extractText(theme)
    if ( textContent[0] == 0 ):
        directory = os.path.join(directory, theme)
        if (not os.path.exists(directory)):
            os.makedirs(theme)
        os.chdir(directory)
        fisierText = theme + ".txt"
        finalMessage = ""
        for i in range(1,len(textContent)):
            finalMessage+=textContent[i]
        open(fisierText, "wt", encoding="utf8").write(finalMessage)
        return
    images = extractImages(theme)
    directory = os.path.join(directory,theme)
    if ( not os.path.exists(directory) ):
        os.makedirs(theme)
    os.chdir(directory)
    fisierText = theme + ".txt"
    open(fisierText,"wt", encoding="utf8").write(textContent)
    for i in images:
        fisier = split("/",i)
        x ="https:"+i
        urllib.request.urlretrieve(x,fisier[-1])