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
    print_prev_events(tracker)
    print_slots(tracker)
    #print_latest_message(tracker)
    print("____________________________________")


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
        e = tracker.latest_message
        objRcpt = tracker.latest_message["entities"][0]["entity"]
        slotvars = {
            "objRcpt": tracker.latest_message["entities"][0]["value"],
            "colour": tracker.get_slot(objRcpt)["colour"]
        }
        dispatcher.utter_message(response="utter_tell_colour", **slotvars)
        
        return []

#DONT HAVE
class tell_shape(Action):
    def name(self) -> Text:
        return "tell_shape"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "rcpt": "RCPT",
            "shape": "SHAPE"
        }
        dispatcher.utter_message(response="utter_tell_shape", **slotvars)
        return []

#DONT HAVE
class tell_pos(Action):
    def name(self) -> Text:
        return "tell_pos"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slotvars = {
            "rcpt": "RCPT",
            "pos": "POS"
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
        print_latest_message(tracker)
        slotvars = {
            "obj":tracker.get_slot("obj")["type"],
            "state": tracker.get_slot("obj")["state"]
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
        slotvars = {
            "context": "CONTEXT",
            "objRcpt": "OBJRCPT"
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
        next_obj = {"obj":"apple","colour":"green","state":"whole"}
        next_rcpt = {"rcpt":"mat","colour":"green","shape":"square","pos":"top left"}

        #obj_context = get_context(next_obj)
        #rcpt_context = get_context(next_rcpt)

        slotvars = {
            "obj": next_obj["obj"],
            "rcpt": next_rcpt["rcpt"] 
        }

        dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
        return [SlotSet("obj", {"type":"apple","colour":"green","state":"whole"}), SlotSet("rcpt", {"type":"mat","colour":"red","shape":"square","pos":"top left"})]


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
