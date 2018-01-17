import FrecvencyModule as FM
import aiml
import time
import threading
import random


class RaspberryThread(threading.Thread):
    def __init__(self, function):
        self.running = False
        self.function = function
        super(RaspberryThread, self).__init__()

    def start(self):
        self.running = True
        super(RaspberryThread, self).start()

    def run(self):
        while self.running:
            self.function()

    def stop(self):
        self.running = False


def check():
    global answer
    time.sleep(60)

    if answer is not None:
        return

    print(random.choice(foo))

    check()


answer = None

foo = ["Daca v-ati plictisit de conversatie, putem schimba oricand subiectul.", "Vreti sa discutam despre altceva?",
       "Nu ati mai spus nimic de mult timp.", "Daca doriti, putem discuta si despre altceva.",
       "Medicina este o stiinta minunata studiata inca din antichitate.", "Stiati ca atunci cand v-ati nascut aveati 350 de oase, iar dupa terminarea copilariei 144 dintre ele s-au unit intre ele.",
       "Stiati ca o persoana sub 30 de ani inhaleaza de doua ori mai mult oxigen decat una de peste 80 de ani."]


def check_for_answer():
    global answer

    thread1.start()

    answer = input()

    return answer


kernel = aiml.Kernel()

kernel.bootstrap(learnFiles="client.aiml")

thread1 = RaspberryThread(function=check)


def start_idle():
    while True:
        print("Introduceti un mesaj: ")
        global answer
        answer = None
        message = check_for_answer()
        searchMedicalTerm = FM.printBotFinalResponse(message)
        if message == "gata":
            exit()
        elif searchMedicalTerm != "none":
            print(searchMedicalTerm)
        else:
            print(kernel.respond(message))


start_idle()
