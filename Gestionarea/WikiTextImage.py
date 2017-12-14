import wikipedia
import requests
from bs4 import BeautifulSoup
from re import split

def extractText(page):
    content = wikipedia.page(page).content
    return content

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
                rezultatFinal.append(j);
    return rezultatFinal

print(extractImages("Albert Einstein"))

