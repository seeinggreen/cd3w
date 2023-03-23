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
        print_all(tracker)
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
        print_all(tracker)
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

        objRcpt = tracker.latest_message["entities"][0]["entity"]

        print_all(tracker)
        slotvars = {
            "objRcpt": tracker.get_slot(objRcpt)["name"],
            "colour": tracker.get_slot(objRcpt)["colour"]
        }
        print_all(tracker)
        dispatcher.utter_message(response="utter_tell_colour", **slotvars)
        
        return []

class tell_shape(Action):
    def name(self) -> Text:
        return "tell_shape"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        polite = ""
        if(tracker.get_slot("rcpt")["shape"] == "square"):
            if( "circle" in tracker.latest_message["text"]):
                polite = "No, "

        if(tracker.get_slot("rcpt")["shape"] == "circle"):
            if( "square" in tracker.latest_message["text"]):
                polite = "No, "

        if(tracker.get_slot("rcpt")["shape"] in tracker.latest_message["text"]):
            polite = "Yes, "

        slotvars = {
            "polite": polite,
            "rcpt": tracker.get_slot("rcpt")["name"],
            "shape": tracker.get_slot("rcpt")["shape"]
        }
        print_all(tracker)



        dispatcher.utter_message(response="utter_tell_shape", **slotvars)
        return []

class tell_pos(Action):
    def name(self) -> Text:
        return "tell_pos"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        slotvars = {
            "rcpt": tracker.get_slot("rcpt")["name"],
            "pos": tracker.get_slot("rcpt")["pos"]
        }
        print_all(tracker)
        dispatcher.utter_message(response="utter_tell_pos", **slotvars)
        return []

class tell_state(Action):
    def name(self) -> Text:
        return "tell_state"
        
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "obj":tracker.get_slot("obj")["name"],
            "state": tracker.get_slot("obj")["isSliced"]
        }
        print_all(tracker)
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
        print_all(tracker)
        dispatcher.utter_message(response="utter_tell_general", **slotvars)
        return []

class tell_next_step(Action):
    def name(self) -> Text:
        return "tell_next_step"
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        next_obj =  {'id': 'Apple3Slice', 'name': 'apple', 'colour': 'yellow', 'hasMoved': False, 'isSliced': True, 'pos': (1, 0)}
        next_rcpt = {'id': 'Circle4', 'name': 'mat', 'shape': 'circle', 'colour': 'red', 'pos': (1, 0)}

        slotvars = {
            "obj": next_obj["name"],
            "rcpt": next_rcpt["name"] 
        }
        print_all(tracker)

        dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
        return [SlotSet("obj",next_obj), SlotSet("rcpt",next_rcpt)]

class tell_me_when_done(Action):
    def name(self) -> Text:
        return "tell_me_when_done"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            
        }
        print_all(tracker)
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
        print_all(tracker)
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
        print_all(tracker)
        dispatcher.utter_message(
            response="utter_help_delete", **slotvars)
        return []