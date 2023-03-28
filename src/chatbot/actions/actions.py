import json
import random
from typing import Any, Text, Dict, List    
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    FollowupAction,
    ActionExecuted,
    UserUttered ,
    Restarted
)

#LEVEL OF DETAIL FUNCTIONS #############################################################################################################
# RCPT ##############
def context_manager_rcpt(curr, sender_id):

    context_level = dict_context[sender_id]["context"]
    
    if context_level == 1:
        return get_low_context_rcpt(curr, sender_id)
    if context_level == 2:
        return get_min_context_rcpt(curr, sender_id)
    else:
        return get_high_context_rcpt(curr, sender_id)
    
# under specify
def get_low_context_rcpt(curr, sender_id):
    rand = random.randint(0,2)
    if rand == 0:
        return curr["shape"] + " " + curr["name"]
    if rand == 1:
        return curr["colour"] + " " + curr["name"]
    if rand == 2:
        return curr["pos"] + " " + curr["name"]

# over specify
def get_high_context_rcpt(curr, sender_id):
    return curr["pos"] + ", " + curr["colour"] + ", and " + curr["shape"] + " " + curr["name"] 

#Incremental Algorithm 
#This function returns the minimum level of detail required to uniquely identify an rcpt
def get_min_context_rcpt(curr, sender_id):

    name = True
    nameShape = True
    nameColour = True
    rcpt_ls = dict_rcpt.get(sender_id)
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
        return curr["shape"] + " " + curr["name"]
    if nameColour:
        return curr["colour"] + " " + curr["name"]
    if nameColour and nameShape:
        return curr["colour"] + " " + curr["shape"]  + " " + curr["name"]
    return curr["colour"] + " " + curr["shape"] + " " + curr["name"]

# OBJ ##############
def context_manager_obj(curr, sender_id):

    context_level = dict_context[sender_id]["context"]
    
    if context_level == 1:
        return get_low_context_obj(curr, sender_id)
    if context_level == 2:
        return get_min_context_obj(curr, sender_id)
    else:
        return get_high_context_obj(curr, sender_id)

# under specify
def get_low_context_obj(curr, sender_id):

    if(curr["name"] == "apple"  or curr["colour"] == "bread"):
        return curr["state"] + " " + curr["name"]
    else:
        return curr["colour"] + " " + curr["name"]
    
# over specify      
def get_high_context_obj(curr, sender_id):
    if(curr["name"] == "apple"  or curr["colour"] == "bread"):
        return curr["colour"] + " " + curr["state"] + " " + curr["name"]
    else:
        return curr["colour"] + " " + curr["name"]

#Incremental Algorithm 
#This function returns the minimum level of detail required to uniquely identify an object
def get_min_context_obj(curr, sender_id):

    name = True
    nameSlice = True
    nameColour = True
    obj_ls = dict_obj.get(sender_id)
    for o in obj_ls:
        if o["id"] != curr["id"]:
            if o["name"] == curr["name"]:
                name = False
            if o["name"] == curr["name"] and o["isSliced"] == curr["isSliced"]:
                nameSlice = False
            if o["name"] == curr["name"] and o["colour"] == curr["colour"]:
                nameColour = False
    if name:
        return "only" + " " + curr["name"]
    if nameSlice:
        return "sliced " + " " + curr["name"]
    if nameColour:
        return curr["colour"] + " " + curr["name"]
    return  "sliced " + curr["colour"] + " " + curr["name"]

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
    if pos[1] == 1:
        pos[1] = "middle"
    if pos[1] == 2:
        pos[1] = "bottom"
    
    return pos[0] +" "+ pos[1]

def forced_context(curr):
    return 0

#NEXT OBJ FUNCTIONS #############################################################################################################


def next_obj(sender_id):
    obj_ls = dict_obj.get(sender_id)
    for o in obj_ls:
        if not o["hasMoved"]:
            return o
    return False

def next_rcpt(o, sender_id):
    rcpt_ls = dict_rcpt.get(sender_id)
    for r in rcpt_ls:
        if r["pos"] == o["pos"]:
            return r
    return False

def update_obj(obj, sender_id):
    obj_ls = dict_obj.get(sender_id)
    for o in obj_ls:
        if o["id"] == obj["id"]:
            o['hasMoved'] = True
    
            
#HELPER FUNCTIONS #############################################################################################################

def read_json(slurk_port, item_type):
    filename = str(slurk_port) + "_" + item_type
    with open(f'../../src/rasa_srv/lead_configs/{filename}.json', encoding="utf-8") as jFile:
        data = json.load(jFile)
    return data

def read_obj_json(slurk_port):
    if (slurk_port not in dict_obj):
        dict_obj[slurk_port] = read_json(slurk_port, "obj")


def read_rcpt_json(slurk_port):
    if (slurk_port not in dict_rcpt):
        dict_rcpt[slurk_port] = read_json(slurk_port, "rcpt")


def read_context_json(slurk_port):
    if (slurk_port not in dict_context):
        dict_context[slurk_port] = read_json(slurk_port, "sceneInfo")
    

def write_events_log(data, file_name):
    log_folder = f'../../output/rasa_logs/lead_configs'
    with open(f'../../output/rasa_logs/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

dict_obj = {}
dict_rcpt = {}
dict_context = {}

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


def purple_shape_grounding(tracker, shape, sender_id):
    shape11 = False
    shape12 = False
    shape13 = False
    rcpt_ls = dict_rcpt.get(sender_id)
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

        clarification_action_list = ["utter_grounding_purple","utter_grounding_purple_variant","utter_tell_colour","utter_tell_shape", "utter_tell_pos", "utter_tell_state", "utter_tell_general", "utter_tell_next_step"]
        print ("utter_Action")
        print (temp_list[-1]['utter_action'])
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
        update_obj(tracker.get_slot("obj"), tracker.current_state()['sender_id'] )
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

        print ("GREET")
        # Setting json scene data on greet by checking sender id        
        read_obj_json(tracker.current_state()['sender_id'])
        read_rcpt_json(tracker.current_state()['sender_id'])
        read_context_json(tracker.current_state()['sender_id'])

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

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #by default use obj
        sender_id = tracker.current_state()['sender_id']
        objRcpt = "rcpt"
        polite = ""
        temp_list = []
        if(len(tracker.latest_message["entities"]) > 0):
            for entity_track in tracker.latest_message["entities"]:
                if entity_track['entity'] == "obj":
                     objRcpt = "obj"
                     break
     
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
                    grounding_term = purple_shape_grounding(tracker, tracker.get_slot(objRcpt)["shape"], sender_id)
                    if user_colour != grounding_term:
                        slotvars = {
                            
                            "grounding_term": grounding_term,
                            "slot_colour": slot_colour
                        }
                        dispatcher.utter_message(response="utter_grounding_purple_variant", **slotvars)
                        #print("I'm not sure what " + user_colour + " is. I'm talking about the "+ grounding_term +" mat, lets call that colour "+ slot_colour)
                        return []
                    if user_colour == grounding_term:
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
        
        
        sender_id = tracker.current_state()['sender_id']
        
        if(len(tracker.latest_message["entities"]) > 0):
            objRcpt = tracker.latest_message["entities"][0]["entity"]
        print ("obj_rcpt")
        print (objRcpt)
        if(objRcpt == "obj"):
            context = get_min_context_obj(tracker.get_slot(objRcpt), sender_id)

        if(objRcpt == "rcpt"):
            context = get_min_context_rcpt(tracker.get_slot(objRcpt), sender_id)

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
       
        obj =  next_obj(tracker.current_state()['sender_id'])
        if (obj):
            rcpt = next_rcpt(obj, tracker.current_state()['sender_id'])

            obj_context =  context_manager_obj(obj, tracker.current_state()['sender_id'])
            rcpt_context = context_manager_rcpt(rcpt, tracker.current_state()['sender_id'])

            slotvars = {
                "obj": obj_context,
                "rcpt": rcpt_context
            }
        
            dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
            return [SlotSet("obj",obj), SlotSet("rcpt",rcpt)]
        else:
            dispatcher.utter_message(text="Congratulations. We are done with the game. Thanks for playing")
            dict_obj.pop(tracker.current_state()['sender_id'])
            dict_rcpt.pop(tracker.current_state()['sender_id'])
            return [Restarted()]

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
