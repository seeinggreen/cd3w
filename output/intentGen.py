import json

class Intent(object):

    def __init__(self, intent, message):
        self.intent = intent
        self.messages = {message}

class Actions(object):

    def __init__(self, action, message):
        self.action = "utter_"+action
        self.messages = {message}



def readJSON(data, intents, actions):

    for d in data["2023-03-08"]:
        if(d["user"] == "follower" or d["user"] == "Follower" ):
            if("message" in d):
                if(not intents):
                    intents.append( Intent(d["label"], d["message"])) 
                for i in intents:
                    if i.intent == d["label"]:
                        i.messages.add(d["message"])
                        break
                    if i == intents[-1]:
                        intents.append(Intent(d["label"], d["message"]))    

        elif(d["user"] == "Leader" or d["user"] == "leader"):
            if("message" in d):
                if(not actions):
                    actions.append(Actions(d["label"], d["message"])) 
                for a in actions:
                    if a.action == "utter_"+d["label"]:
                        a.messages.add(d["message"])
                        break
                    if a == actions[-1]:
                        actions.append( Actions(d["label"], d["message"])) 

def printActions(actions):

    for a in actions:
        print(a.action)
        for m in a.messages:
            print(" ",m)

def printIntents(intents):
    for i in intents:
        print(i.intent)
        for m in i.messages:
            print(" ",m)

files = ["l0_v1.json","l0_v2.json","l1_v1.json","l1_v4.json","l2_v3.json","l3_v1.json","l3_v2.json","l4_v1.json","l4_v3.json","l5_v2.json","l6_v1.json","l6_v3.json","l7_v3.json","l7_v4.json","l8_v2.json","l8_v2.json","l8_v3.json","l9_v3.json","l9_v4.json" ]

intents = []
actions = []

for addr in files:
    print(addr)
    f = open("dialogues/"+addr, "r")
    data = json.load(f)
    f.close()
    readJSON(data, intents, actions)

printActions(actions)
printIntents(intents)
