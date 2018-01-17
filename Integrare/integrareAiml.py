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
    global thread2
    time.sleep(60)

    if answer is not None:
        return
    thread1.stop()
    thread2.stop()
    print(random.choice(foo))

    thread2 = RaspberryThread(function=check)
    thread2.start()


answer = None
thread1 = RaspberryThread(function=check)
thread2 = RaspberryThread(function=check)
foo = ["Daca v-ati plictisit de conversatie, putem schimba oricand subiectul.", "Vreti sa discutam despre altceva?",
       "Nu ati mai spus nimic de mult timp.", "Daca doriti, putem discuta si despre altceva.",
       "Medicina este o stiinta minunata studiata inca din antichitate.", "Stiati ca atunci cand v-ati nascut aveati 350 de oase, iar dupa terminarea copilariei 144 dintre ele s-au unit intre ele.",
       "Stiati c ao persoana sub 30 de ani inhaleaza de doua ori mai mult oxigen decat una de peste 80 de ani."]



def check_for_answer(message):
    global answer
    global thread1

    thread2.stop()
    thread1.stop()

    thread1 = RaspberryThread(function=check)
    thread1.start()

    #answer = input()
    answer=message

    return answer


kernel = aiml.Kernel()

kernel.bootstrap(learnFiles="AIML\client.aiml")
kernel.bootstrap(learnFiles="AIML\client_profile.aiml")
kernel.bootstrap(learnFiles="AIML\cultura-generala.aiml")
kernel.bootstrap(learnFiles="AIML\date.aiml")
kernel.bootstrap(learnFiles="AIML\defi.aiml")
def respond(message):
#while True:
    print("Introduceti un mesaj: ")
    answer = None
    message = check_for_answer(message)
    # message = input("User>")
    searchMedicalTerm = FM.printBotFinalResponse(message)
    if message == "gata":
        exit()
    elif searchMedicalTerm != "none":
        print(searchMedicalTerm)
        return searchMedicalTerm
    else:
        response=kernel.respond(message)
        print(response)
        return response
