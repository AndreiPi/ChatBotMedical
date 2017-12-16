def Initiere(file):
    File = open(file, "r")
    for line in File:
        afisareDefinitii(line[:-1])
    File.close()

def afisareDefinitii(word):
    print("Cuvantul: " + word)
    definitions_read = open("Definitii", "r", encoding="utf8")
    definitions_write = open("Corecte-Gresite", "r", encoding="utf8")
    timer = 0
    found = False
    for line in definitions_read:
        definitions_write.close()
        definitions_write = open("Corecte-Gresite", "r", encoding="utf8")
        foundWordInTrue = False
        foundWordInFalse = False
        if(word in line):
            timer = timer + 1
            lineInCorecteGresiteFalse = ""
            lineInCorecteGresiteTrue = ""
            lineInCorecteGresiteTrue += word + " = " + line[:-1] + "(da)"
            lineInCorecteGresiteFalse += word + " = " + line[:-1] + "(nu)"
            index = lineInCorecteGresiteFalse.index("=") + 2
            for wordsInTrueFalse in definitions_write:
                if lineInCorecteGresiteTrue[index:] in wordsInTrueFalse[index:]:
                    print("Definitia este: ", line)
                    foundWordInTrue = True
                if lineInCorecteGresiteFalse[index:] in wordsInTrueFalse[index:]:
                    foundWordInFalse = True
            if(foundWordInFalse):
                continue
            if(foundWordInTrue):
                break

            print("Definitia este: ", line)
            print("Este aceasta definitie corecta ?")
            true_false = input()
            if(true_false == "da"):
                definitions_write.close()
                definitions_write = open("Corecte-Gresite", "a", encoding="utf8")
                print("Raspunsul a fost retinut !")
                trueResponse = word + " = " + line[:-1] + "(da)" + "\n"
                definitions_write.write(trueResponse)
                found = True

            else:
                definitions_write.close()
                definitions_write = open("Corecte-Gresite", "a", encoding="utf8")
                print("Se cauta definitia cuvantului...")
                falseResponse = word + " = " + line[:-1] + "(nu)" + "\n"
                definitions_write.write(falseResponse)
        if(timer == 2):
            break
        if(found == True):
            break

Initiere("Lista")
