import json
from typing import Any, Text, Dict, List    
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    FollowupAction,
    ActionExecuted,
    UserUttered 
)

#LEVEL OF DETAIL FUNCTIONS #############################################################################################################

#This function returns the minimum level of detail required to uniquely identify an object
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

#This function returns the minimum level of detail required to uniquely identify an rcpt
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
    if nameColour and nameShape:
        return curr["colour"] + " " + curr["shape"] 
    return get_pos(curr["pos"]) + curr["colour"] + " " + curr["shape"] 

def get_pos(pos):
    if pos[0] == 0:
        pos[0] = "left"
    if pos[0] == 1:
        pos[0] = "left"
    if pos[0] == 2:
        pos[0] = "middle"
    if pos[0] == 3:
        pos[0] = "middle"
    if pos[0] == 4:
        pos[0] = "right"
    if pos[0] == 5:
        pos[0] = "right"

    if pos[1] == 0:
        pos[1] = "top"
    if pos[1] == 0:
        pos[1] = "middle"
    if pos[1] == 1:
        pos[1] = "bottom"
    
    return pos[0] +" "+ pos[1]

def forced_context(curr):
    return 0

#NEXT OBJ FUNCTIONS #############################################################################################################

def next_obj():
    for o in obj_ls:
        if not o["hasMoved"]:
            return o
    return False

def next_rcpt(o):
    for r in rcpt_ls:
        if r["pos"] == o["pos"]:
            return r
    return False

def update_obj(obj):
    for o in obj_ls:
        if o["id"] == obj["id"]:
            o['hasMoved'] = True
    print (obj_ls)
            
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

#obj_ls = read_obj_json(5000)
#rcpt_ls= read_rcpt_json(5000)

obj_ls = []
rcpt_ls = []
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


def purple_shape_grounding(tracker, shape):
    shape11 = False
    shape12 = False
    shape13 = False

    for r in rcpt_ls:
        if r["id"].lower() == shape+"11".lower():
            shape11 = True
        if r["id"].lower() == shape+"12".lower():
            shape12 = True
        if r["id"].lower() == shape+"13".lower():
            shape13 = True

    if shape11 and shape12 and shape13:
        # Colour = Violet
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"11".lower()):
            return "middle shade of purple"
        # Colour = Indigo
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"12".lower()):
            return "darkest shade of purple"
        # Colour = Iris
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"13".lower()):
            return "lightest shade of purple"
        
    if shape12 and shape13:
        # Colour = Indigo
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"12".lower()):
            return "dark purple"
        # Colour = Iris
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"13".lower()):
            return "light purple"

    if shape11 and shape13:
        # Colour = Violet
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"11".lower()):
            return "dark purple"
        # Colour = Iris
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"13".lower()):
            return "light purple"
        
    if shape11 and shape12:
        # Colour = Violet
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"11".lower()):
            return "light purple"
        # Colour = Indigo
        if(tracker.get_slot("rcpt")["id"].lower() == shape+"12".lower()):
            return "dark purple"

    if shape11:
        return "purple"
    if shape12:
        return "purple"
    if shape13: 
        return "purple"


#ACTIONS #############################################################################################################

class affirm(Action):
    def name(self) -> Text:
        return "affirm"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        temp_list = []
        for e in tracker.events:
            if e["event"] == "bot":
                temp_list.append(e['metadata'])

        clarification_action_list = ["utter_tell_colour","utter_tell_shape", "utter_tell_pos", "utter_tell_state", "utter_tell_general", "utter_tell_next_step"]
      
        if(temp_list[-1]['utter_action']):
            if  (temp_list[-1]['utter_action'] in clarification_action_list):
                dispatcher.utter_message(response="utter_tell_me_when_done")
            elif(temp_list[-1]['utter_action'] == "utter_greet"):
                return [ActionExecuted("action_listen")] + [UserUttered("whats next", { 
                "intent": {"confidence": 1, "name": "ask_next_step"}, 
                "entities": [] 
                })]
        return []

class resp_done_it(Action):
    def name(self) -> Text:
        return "resp_done_it"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #return [FollowupAction("tell_next_step")]
        update_obj(tracker.get_slot("obj"))
        return [ActionExecuted("action_listen")] + [UserUttered("whats next", { 
		"intent": {"confidence": 1, "name": "ask_next_step"}, 
		"entities": [] 
		})]
        


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
        # Getting last bot action event
        temp_list = []
        for e in tracker.events:
            if e["event"] == "bot":
                temp_list.append(e['metadata'])

        if  (temp_list[-1]['utter_action'] == "utter_greet"):
                dispatcher.utter_message(text="Let me know when ready")
        dispatcher.utter_message(response="utter_deny", **slotvars)
        return []


class greet(Action):
    def name(self) -> Text:
        return "greet"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Setting json scene data on greet by checking sender id
        global obj_ls, rcpt_ls
        obj_ls= read_obj_json(tracker.current_state()['sender_id'])
        rcpt_ls= read_rcpt_json(tracker.current_state()['sender_id'])
        
        dispatcher.utter_message(response="utter_greet")
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


class tell_colour(Action):
    def name(self) -> Text:
        return "tell_colour"

    def grounding(tracker, dispatcher, objRcpt, slot_colour):

            for p in set_purples:
                if p in tracker.latest_message["text"].lower():
                    user_colour = p
                    grounding_term = purple_shape_grounding(tracker, tracker.get_slot(objRcpt)["shape"])
                    if user_colour != "purple":
                        slotvars = {
                            "user_colour": user_colour,
                            "grounding": grounding_term,
                            "slot_colour": slot_colour
                        }
                        #dispatcher.utter_message(response="utter_grounding_purple_variant", **slotvars)

                        print("I'm not sure what " + user_colour + " is. I'm talking about the "+ grounding_term +" mat, lets call that colour "+ slot_colour)
                    if user_colour == grounding_term:
                        slotvars = {
                            "user_colour": user_colour,
                            "slot_colour": slot_colour
                        }
                        #dispatcher.utter_message(response="utter_grounding_purple_variant", **slotvars)

                        print("Lets call " + user_colour + ", " + slot_colour+ ".")

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #by default use obj
        objRcpt = "rcpt"
        polite = ""
        temp_list = []
        if(len(tracker.latest_message["entities"]) > 0):
            for entity_track in tracker.latest_message["entities"]:
                if entity_track['entity'] == "obj":
                     objRcpt = "obj"
                     break
            #if(tracker.latest_message["entities"][0]["entity"] == "obj"):
                #objRcpt = "obj"
            for c in set_colours:
                if c in tracker.latest_message["text"].lower():
                    polite = "No. "
            if(tracker.get_slot(objRcpt)["colour"] in tracker.latest_message["text"].lower()):
                polite = "Yes. "
    
        slot_colour = tracker.get_slot(objRcpt)["colour"].lower()
        user_colour = ""
        if(slot_colour == "violet" or slot_colour == "indigo" or slot_colour == "iris"):
            for p in set_purples:
                if p in tracker.latest_message["text"].lower():
                    user_colour = p
                    grounding_term = purple_shape_grounding(tracker, tracker.get_slot(objRcpt)["shape"])
                    if user_colour != grounding_term:
                        slotvars = {
                            "user_colour": user_colour,
                            "grounding_term": grounding_term,
                            "slot_colour": slot_colour
                        }
                        dispatcher.utter_message(response="utter_grounding_purple_variant", **slotvars)
                        #print("I'm not sure what " + user_colour + " is. I'm talking about the "+ grounding_term +" mat, lets call that colour "+ slot_colour)
                        return []
                    if user_colour == "purple":
                        slotvars = {
                            "user_colour": user_colour,
                            "slot_colour": slot_colour
                        }
                        dispatcher.utter_message(response="utter_grounding_purple", **slotvars)
                        #print("Lets call " + user_colour + ", " + slot_colour+ ".")
                        return []

        slotvars = {
            "polite": polite,
            "objRcpt": tracker.get_slot(objRcpt)["name"],
            "colour": tracker.get_slot(objRcpt)["colour"]
        }

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
     
        if (obj):
            rcpt = next_rcpt(obj)
            slotvars = {
                "obj": obj["name"],
                "rcpt": rcpt["name"] 
            }
        
            dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
            return [SlotSet("obj",obj), SlotSet("rcpt",rcpt)]
        else:
            dispatcher.utter_message(text="Congratulations. We are done with the game. Thanks for playing")

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
    


set_colours = {"red","blue","orange","green","purple","yellow","iris","black","ocean blue","sky blue","gold","silver","gray","brown","khaki","white","Beige","Maroon","Navy","Teal","Turquoise","Magenta","Lavender","Olive","Forest Green","Mustard","Ruby","Gold","Silver","Bronze","Peach"}
set_purples = {"magenta", "lavendar", "dark purple", "light purple", "purple"}
