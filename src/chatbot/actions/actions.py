# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,                                     #To store the previous conversation. Same as rasa shell
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    #Intents and Actions
#
#         dispatcher.utter_message(text="Hello World!")             #Sent to user
#
#         return []

import json
from typing import Any, Text, Dict, List    
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet
)

#LEVEL OF DETAIL FUNCTIONS #############################################################################################################

def get_min_context_obj(curr):

    name = True
    nameSlice = True
    nameColour = True
    
    for o in obj_ls:
        if o["id"] != curr["id"]:
            if o["name"] == curr["name"]:
                name = False
            if o["name"] == curr["name"] and o["isSliced"] == curr["isSliced"]:
                nameSlice = False
            if o["name"] == curr["name"] and o["colour"] == curr["colour"]:
                nameColour = False
    if name:
        return "only"
    if nameSlice:
        return "sliced "
    if nameColour:
        return curr["colour"] 
    return  "sliced " + curr["colour"] 

def get_min_context_rcpt(curr):

    name = True
    nameShape = True
    nameColour = True
    
    for r in rcpt_ls:
        if r["id"] != curr["id"]:
            if r["name"] == curr["name"]:
                name = False
            if r["name"] == curr["name"] and r["shape"] == curr["shape"]:
                nameShape = False
            if r["name"] == curr["name"] and r["colour"] == curr["colour"]:
                nameColour = False
    if name:
        return "only"
    if nameShape:
        return curr["shape"] 
    if nameColour:
        return curr["colour"] 
    return curr["colour"] + " " + curr["shape"] 

def get_pos(pos):
    if pos[0] == 0:
        pos[0] = "left"
    if pos[0] == 1:
        pos[0] = "middle"
    if pos[0] == 2:
        pos[0] = "right"

    if pos[1] == 0:
        pos[1] = "bottom"
    if pos[1] == 1:
        pos[1] = "top"
    
    return pos[0] +" "+ pos[1]

def forced_context(curr):
    return 0
#NEXT OBJ FUNCTIONS #############################################################################################################
def next_obj():
    for o in obj_ls:
        if not o.hasMoved:
            return o
    return False
def next_rcpt(o):
    for r in rcpt_ls:
        if r.pos == o.pos:
            return r
    o.hasMoved = True
    return False

#HELPER FUNCTIONS #############################################################################################################

def read_json(slurk_port, item_type):
    filename = str(slurk_port) + "_" + item_type
    with open(f'../../src/rasa_srv/lead_configs/{filename}.json', encoding="utf-8") as jFile:
        data = json.load(jFile)
    return data

def read_obj_json(slurk_port):
    return read_json(slurk_port, "obj")

def read_rcpt_json(slurk_port):
    return read_json(slurk_port, "rcpt")

obj_ls = read_obj_json(5000)
rcpt_ls= read_rcpt_json(5000)

#TRACKER PRINTING FUNCTIONS #############################################################################################################

def print_prev_events(tracker):
    print("\n\ntracker.events:")
    for e in tracker.events:
        if e["event"] == "user":
            parse_data = e["parse_data"]
            print(json.dumps(parse_data["intent"], indent=4))
            print(json.dumps(parse_data["entities"], indent=4))

def print_slots(tracker):
    print("\ntracker.slots:")
    print(tracker.slots)

def print_latest_message(tracker):
    print("\ntracker.latest_message:")
    print(tracker.latest_message["intent"])
    print(json.dumps(tracker.latest_message["entities"], indent=4))
    print(tracker.latest_message["text"])

def print_all(tracker):
    print("____________________________________")
    #print_prev_events(tracker)
    print_slots(tracker)
    print_latest_message(tracker)
    print("____________________________________")

#ACTIONS #############################################################################################################

class affirm(Action):
    def name(self) -> Text:
        return "affirm"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "state": "sliced",
        }

        dispatcher.utter_message(response="utter_affirm", **slotvars)
        return []


class deny(Action):
    def name(self) -> Text:
        return "deny"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "state": "sliced",
        }
        dispatcher.utter_message(response="utter_deny", **slotvars)
        return []


class greet(Action):
    def name(self) -> Text:
        return "greet"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "state": "sliced",
        }

        dispatcher.utter_message(response="utter_greet", **slotvars)
        return []


class goodbye(Action):
    def name(self) -> Text:
        return "goodbye"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slotvars = {
            "state": "sliced",
        }

        dispatcher.utter_message(response="utter_goodbye", **slotvars)
        return []

#TODO 
class tell_colour(Action):
    def name(self) -> Text:
        return "tell_colour"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #by default use obj
        objRcpt = "obj"
        if(len(tracker.latest_message["entities"]) > 0):
            objRcpt = tracker.latest_message["entities"][0]["entity"]
        polite = ""
        for c in set_colours:
            if c in tracker.latest_message["text"].lower():
                polite = "No. "

        if(tracker.get_slot(objRcpt)["colour"] in tracker.latest_message["text"].lower()):
            polite = "Yes. "

        slotvars = {
            "polite": polite,
            "objRcpt": tracker.get_slot(objRcpt)["name"],
            "colour": tracker.get_slot(objRcpt)["colour"]
        }
        print(tracker.latest_message)

        dispatcher.utter_message(response="utter_tell_colour", **slotvars)
        
        return []

class tell_shape(Action):
    def name(self) -> Text:
        return "tell_shape"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)

        polite = ""
        if(tracker.get_slot("rcpt")["shape"] == "square"):
            if( "circle" in tracker.latest_message["text"].lower()):
                polite = "No. "

        if(tracker.get_slot("rcpt")["shape"] == "circle"):
            if( "square" in tracker.latest_message["text"].lower()):
                polite = "No. "

        if(tracker.get_slot("rcpt")["shape"] in tracker.latest_message["text"].lower()):
            polite = "Yes. "

        slotvars = {
            "polite": polite,
            "rcpt": tracker.get_slot("rcpt")["name"],
            "shape": tracker.get_slot("rcpt")["shape"]
        }

        dispatcher.utter_message(response="utter_tell_shape", **slotvars)
        return []

class tell_pos(Action):
    def name(self) -> Text:
        return "tell_pos"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pos = get_pos(tracker.get_slot("rcpt")["pos"])

        polite = ""
        slotvars = {
            "polite": polite,
            "rcpt": tracker.get_slot("rcpt")["name"],
            "pos": pos
        }

        dispatcher.utter_message(response="utter_tell_pos", **slotvars)
        return []

class tell_state(Action):
    def name(self) -> Text:
        return "tell_state"
        
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        polite = ""
        if tracker.get_slot("obj")["isSliced"]:
            state="sliced"
            #user says "slice" and the obj is sliced
            if("slice" in tracker.latest_message["text"].lower()):
                polite = "Yes. "
                #user says sliced and whole, implying they are asking "sliced or whole?" or "I have a slice and a whole"
                if("whole" in tracker.latest_message["text"].lower()):
                    polite = ""
            #user says "whole" and the obj is sliced
            elif("whole" in tracker.latest_message["text"].lower()):
                polite = "No. "
        else:
            state="whole"
            if("whole" in tracker.latest_message["text"].lower()):
                polite = "Yes. "
                if("slice" in tracker.latest_message["text"].lower()):
                    polite = ""
            elif("slice" in tracker.latest_message["text"].lower()):
                polite = "No. "
            
        slotvars = {
            "polite": polite,
            "obj":tracker.get_slot("obj")["name"],
            "state": state
        }

        dispatcher.utter_message(response="utter_tell_state", **slotvars)
        return []

class tell_general(Action):
    def name(self) -> Text:
        return "tell_general"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if(len(tracker.latest_message["entities"]) > 0):
            objRcpt = tracker.latest_message["entities"][0]["entity"]
        if(objRcpt == "obj"):
            context = get_min_context_obj(tracker.get_slot(objRcpt))

        if(objRcpt == "rcpt"):
            context = get_min_context_rcpt(tracker.get_slot(objRcpt))

        slotvars = {
            "context": context,
            "objRcpt": tracker.get_slot(objRcpt)["name"]
        }

        dispatcher.utter_message(response="utter_tell_general", **slotvars)
        return []

class tell_next_step(Action):
    def name(self) -> Text:
        return "tell_next_step"
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        obj =  next_obj()
        #{'id': 'Apple3Slice', 'name': 'apple', 'colour': 'yellow', 'hasMoved': False, 'isSliced': True, 'pos': (1, 0)}
        #rcpt =  next_rcpt(obj)
        rcpt = next_rcpt(obj)
        #{'id': 'Circle4', 'name': 'mat', 'shape': 'circle', 'colour': 'red', 'pos': (1, 0)}

        slotvars = {
            "obj": obj["name"],
            "rcpt": rcpt["name"] 
        }
        print_all(tracker)

        dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
        return [SlotSet("obj",obj), SlotSet("rcpt",srcpt)]

class tell_me_when_done(Action):
    def name(self) -> Text:
        return "tell_me_when_done"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            
        }

        dispatcher.utter_message(
            response="utter_tell_me_when_done", **slotvars)
        return []

class help_delete(Action):
    def name(self) -> Text:
        return "help_delete"
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
        
        }

        dispatcher.utter_message(
            response="utter_help_delete", **slotvars)
        return []

class help_request(Action):
    def name(self) -> Text:
        return "help_delete"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            
        }

        dispatcher.utter_message(
            response="utter_help_delete", **slotvars)
        return []
    


set_colours = {"red","blue","orange","green","purple","yellow","iris","black","ocean blue","sky blue","gold","silver","gray","brown","khaki","white","color","Beige","Maroon","Navy","Teal","Turquoise","Magenta","Lavender","Olive","Forest Green","Mustard","Ruby","Gold","Silver","Bronze","Peach"}