import wikipedia
import requests
from bs4 import BeautifulSoup
from re import split
import os
import urllib


def extractText(page):
    content = wikipedia.page(page).content
    return content


def extractImages(page):
    wikia = wikipedia.page(page).url
    pageNeeded = requests.get(wikia)
    soup = BeautifulSoup(pageNeeded.text, 'html.parser')
    imgTag = soup.find_all('img')
    rezultat = [img['src'] for img in imgTag]
    teme = split(" ", page)
    rezultatFinal = []
    for i in teme:
        for j in rezultat:
            if i in j:
                rezultatFinal.append(j)
    return rezultatFinal


def extractContent(theme):
    themepath = os.path.join("static", theme)
    directory = os.path.dirname(os.path.realpath(__file__))
    textContent = extractText(theme)
    images = extractImages(theme)
    directory = os.path.join(directory, themepath)
    print(directory)
    if (not os.path.exists(directory)):
        print("make")
        os.makedirs(directory)
    os.chdir(directory)
    fisierText = theme + ".txt"
    open(fisierText, "wt", encoding="utf8").write(textContent)
    for i in images:
        fisier = split("/", i)
        x = "https:" + i
        urllib.request.urlretrieve(x, fisier[-1])


def safe_extaractContent(theme):
    ok = True
    try:
        themepath = os.path.join("static", theme)
        directory = os.path.dirname(os.path.realpath(__file__))
        textContent = extractText(theme)
        images = extractImages(theme)
        directory = os.path.join(directory, themepath)
        if (not os.path.exists(directory)):
            os.makedirs(directory)
        os.chdir(directory)
        fisierText = theme + ".txt"
        open(fisierText, "wt", encoding="utf8").write(textContent)
        for i in images:
            fisier = split("/", i)
            x = "https:" + i
            urllib.request.urlretrieve(x, fisier[-1])
    except NameError:
        a = 1 + 2
    except Exception as e:
        ok = False
        print(type(e))
    finally:
        if ok:
            return ok, theme
        else:
            return None, None
# extractContent("Mihai Eminescu")
# extractContent("Ion Creanga")
# extractContent("Anton pan")