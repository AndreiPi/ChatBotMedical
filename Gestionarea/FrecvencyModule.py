import random
import structarborescenta as SB

#medical terms searched in content(or informative text with medicine definitions)
medicalTerms = []
#content of a text file that contains medical definitions
content = ""
#frequency or the chapters , of the medical terms that are used into the ChatBot answers
frequencyChapters = dict()
#total number of apparitions of the chapter in informative text
maxfrequency = dict()
#SAVE USED ANSWERS FROM INFORMATIVE TEXT
answersUsed = []
#CATALOG
subChapters = dict()
#ARBORE DE STRUCTURA AL CAPITOLELOR,SUBCAPITOLELOR
structureTree = SB.arbore("adnotari.txt")



def getMedicalTerms():
    global structureTree
    for key in structureTree.keys():
        medicalTerms.append(key.lower())
        for value in structureTree[key]:
            medicalTerms.append(value.lower())
    medicalTerms.append('mainchapter')

#ADD VALUES TO A GIVEN KEY
def addSubchapterToBigChapter(bigchap,subchap):
    global subChapters
    if bigchap in subChapters:
        # append the new number to the existing array at this slot
        subChapters[bigchap].append(subchap)
    else:
        # create a new array in this slot
        subChapters[bigchap] = [subchap]

#CREATE THE CHAPTERS/SUBCHAPTERS TREE
def makeChaptersDictionary():
    global subChapters
    for key in structureTree.keys():
        for value in structureTree[key]:
            addSubchapterToBigChapter(key.lower(),value.lower())
    for key in structureTree.keys():
        addSubchapterToBigChapter('mainchapter',key.lower())

    # #addSubchapterToBigChapter('creier','creier')
    # addSubchapterToBigChapter('creier','neuron')
    # addSubchapterToBigChapter('creier','emisfer')
    # addSubchapterToBigChapter('creier','encefal')
    # #addSubchapterToBigChapter('inima','inima')
    # addSubchapterToBigChapter('inima','vene')
    # addSubchapterToBigChapter('inima','arter')
    # #addSubchapterToBigChapter('organe','organe')
    # addSubchapterToBigChapter('organ','creier')
    # addSubchapterToBigChapter('organ','inima')
    # # addSubchapterToBigChapter('plamanii', 'plamanii')
    # # addSubchapterToBigChapter('ficatul', 'ficatul')
    # # addSubchapterToBigChapter('rinichii', 'rinichii')
    # # addSubchapterToBigChapter('encefalul', 'encefalul')
    # # addSubchapterToBigChapter('emisfera', 'emisfera')
    # # addSubchapterToBigChapter('neuroni', 'neuroni')
    # # addSubchapterToBigChapter('vene', 'vene')
    # # addSubchapterToBigChapter('artere', 'artere')


#GET THE KEY OF A VALUE
def getKey(value_search,dictionary):
    for key in dictionary.keys():
        vect = dictionary[key]
        if value_search in vect:
            return key

#REMOVE KEYS,VALUES,MEDTERM THAT ARE DIGITS , NUMBERS
def removeInvalidMedTermsChapters():
    global subChapters
    global medicalTerms
    for key in subChapters.keys():
        if key.isdigit():
            subChapters.pop(key,None)
        else:
            for value in subChapters[key]:
                if value.isdigit():
                    vect = subChapters[key]
                    vect.remove(value)
                    subChapters[key] = vect
    for item in medicalTerms:
        if item.isdigit():
            medicalTerms.remove(item)


def increaseSimilarTermFrequency(value):
    global frequencyChapters
    global medicalTerms
    for term in medicalTerms:
        if term is not value:
            if term in value:
                frequencyChapters[term] = frequencyChapters[term] + 1


def defineGlobalVariables():
    global medicalTerms
    global content
    global frequencyChapters
    global subChapters
    global maxfrequency
    global maxNumberOfDefinitions
    # medicalTerms = ['organ','creier','inima','plaman','ficat','rinichi','encefal','emisfer','neuron','vene','arter']
    getMedicalTerms()
    medicalTerms = list(set(medicalTerms))
    #medicalTerms.remove('sporirea de volum a unei componente normal existente')
    with open('informations.txt', 'r') as f:
        content = f.read()
    for i in range (0,len(medicalTerms)):
        frequencyChapters[medicalTerms[i]] = 0
    for i in range (0,len(medicalTerms)):
        maxfrequency[medicalTerms[i]] = content.lower().count(medicalTerms[i].lower())
    makeChaptersDictionary()
    removeInvalidMedTermsChapters()
    #subChapters.pop('sporirea de volum a unei componente normal existente',None)


defineGlobalVariables()
#print("max ",maxfrequency)
# print(medicalTerms)
# print("NEXT")
# print(subChapters)
# print("Next")
# print(maxfrequency)

def printTopicsFrequency():
        print(frequencyChapters)

def addToUsedAnswers(answer):
    global answersUsed
    answersUsed.append(answer)

#GET ALL INDICES OF A PATTERN IN A TEXT
def allindices(string, sub):
    listindex = []
    i = string.lower().find(sub.lower(), 0)
    while i >= 0:
        listindex.append(i)
        i = string.lower().find(sub.lower(), i + 1)
    return listindex

#GET PROPOSITION FOR A GIVEN INDEX OF THE PATTERN IN TEXT
def getProposition(indexOfPattern):
    global content
    startPropIndex = indexOfPattern
    endPropIndex = indexOfPattern
    finalPropMarks = ['.',';','!','?']
    while content[startPropIndex] not in finalPropMarks:
        startPropIndex = startPropIndex - 1
    while content[endPropIndex] not in finalPropMarks:
        endPropIndex = endPropIndex + 1
    #print("start " , startPropIndex , "end ",endPropIndex)
    finalProposition = content[startPropIndex+1:endPropIndex+1]
    #print(finalProposition)
    return finalProposition

#INCREASE frequency OF ALL WORDS THAT REPRESENT A TOPIC AND EXIST IN THE PROPOSITION PRINTED TO THE CLIENT
def increasefrequency(propositionPrinted):
    global frequencyChapters
    global medicalTerms
    for i in range (0,len(medicalTerms)):
         frequencyChapters[medicalTerms[i]] = frequencyChapters[medicalTerms[i]] + propositionPrinted.lower().count(medicalTerms[i].lower())
         #increaseSimilarTermFrequency(medicalTerms[i])

#GET THE MEDICINE TERM THAT THE CLIENT WHANTS A DEFINITION FOR
def getMedicineTermFromQuestion(humanQuestion):
    global medicalTerms
    words = humanQuestion.split()
    if len(humanQuestion.split()) is 1 and words[0].lower() in medicalTerms:
        return words[0].lower()
    elif "ce este " in humanQuestion.lower() and len(humanQuestion.split()) is 3 and words[2].lower() in medicalTerms:
        return words[2].lower()
    elif "as dori sa aflu mai multe despre " in humanQuestion.lower() and len(humanQuestion.split()) is 8 and words[7].lower() in medicalTerms:
        return words[7].lower()
    for term in medicalTerms:
        if term in humanQuestion:
            return term.lower()
    return "none"

#CHECK A MEDICAL TERM(CHAPTER) STILL HAVE OR NOT INFORMATIONS UNUSED IN TEXT ABOUT THE "TERM" ITSELF OF ITS SUBCHAPTERS STILL HAVE INFORMATIONS IN TEXT
def chapterIsFinished(chapter):
    global subChapters
    global frequencyChapters
    global maxfrequency
    if chapter not in subChapters.keys():
        if frequencyChapters[chapter] < maxfrequency[chapter]:
            return False
    else:
        if frequencyChapters[chapter] < maxfrequency[chapter]:
            return False
        subchapVector = subChapters[chapter]
        for i in range (0,len(subchapVector)):
            if frequencyChapters[subchapVector[i]] is not maxfrequency[subchapVector[i]]:
                return False
    return True

#GET A RANDOM SUBCHAPTER OR A GIVEN CHAPTER THAT STILL HAVE INFORMATIONS UNUSED IN TEXT
def getANotFinishedSubchapter(chapter):
    global subChapters
    vect = []
    for item in subChapters[chapter]:
         if chapterIsFinished(item) is False:
             vect.append(item)
    if frequencyChapters[chapter] < maxfrequency[chapter]:
        vect.append(chapter)
    if len(vect)>0:
        term = vect[random.randint(0, len(vect) - 1)]
        return term
    return "Thats all Fox!"

#PARSE THE TREE OF CHAPTERS AND GET AN INFORMATION AS CLOSE AS POSSIBLE FROM THE USER QUESTION
def getANotUsedAnswer(indexesOfMedTermsInText,medTerm):
    global content
    global answersUsed
    global subChapters
    global frequencyChapters
    global maxfrequency
    numbersOfTries = 0
    foundNewAnswer = False
    randPropIndex = random.randint(0, len(indexesOfMedTermsInText) - 1)
    finalProposition = getProposition(indexesOfMedTermsInText[randPropIndex])
    if finalProposition not in answersUsed:
        foundNewAnswer = True
    if frequencyChapters[medTerm] < maxfrequency[medTerm]:
        while finalProposition in answersUsed and foundNewAnswer is False:
            randPropIndex = random.randint(0, len(indexesOfMedTermsInText) - 1)
            finalProposition = getProposition(indexesOfMedTermsInText[randPropIndex])
            if finalProposition not in answersUsed:
                foundNewAnswer = True
            numbersOfTries = numbersOfTries + 1


    if foundNewAnswer is False:
        if medTerm is None:
            return "Nu mai cunosc alte detalii! Multa bafta!"
        if medTerm in subChapters.keys() and chapterIsFinished(medTerm) is False:
            term = getANotFinishedSubchapter(medTerm)
            # if term is not medTerm:
            frequencyChapters[term] = frequencyChapters[term] - 1
            frequencyChapters[medTerm] = frequencyChapters[medTerm] - 1
            # else:
            #     frequencyChapters[term] = frequencyChapters[term] - 1
            return "Am spus destule despre \"" + medTerm + "\". Ai vrea sa vorbim despre " + term + " ?"
        else:
            if medTerm is None:
                return "Nu mai cunosc alte detalii! Multa bafta!"
            else:
                higherTerm = medTerm
                while chapterIsFinished(higherTerm) is True and higherTerm is not 'mainchapter':
                    higherTerm = getKey(higherTerm, subChapters)

                if chapterIsFinished(higherTerm):
                    return "Nu mai cunosc alte detalii!"
                else:
                    print("high term =  " , higherTerm)
                    higherTerm = getANotFinishedSubchapter(higherTerm)
                    # if medTerm is not higherTerm:
                    frequencyChapters[higherTerm] = frequencyChapters[higherTerm] - 1
                    frequencyChapters[medTerm] = frequencyChapters[medTerm] - 1
                    # else:
                    #     frequencyChapters[medTerm] = frequencyChapters[medTerm] - 1
                    return "Am spus destule despre \"" + medTerm + "\". Ai vrea sa vorbim despre " + higherTerm + " ??"
    else:
        answersUsed.append(finalProposition)
        return finalProposition

#PRINT A FINAL ANSWER FOR THE CLIENT AND INCREASE frequency OF ALL TOPICS THAT IS ABOUT IN THAT ANSWER
def printBotFinalResponse(humanQuestion):
    global content
    global frequencyChapters
    global medicalTerms
    medicineTerm = getMedicineTermFromQuestion(humanQuestion).strip()
    #print(medicineTerm)
    indexesOfMedTermsInText = allindices(content, medicineTerm)
    #print(indexesOfMedTermsInText)
    finalProposition = getANotUsedAnswer(indexesOfMedTermsInText,medicineTerm)
    increasefrequency(finalProposition)
    addToUsedAnswers(finalProposition)
    print(finalProposition.strip())




