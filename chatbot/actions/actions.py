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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


word_varients_colour = {"Colour", "colour", "Color", 'color', 'culor', 'colur', 'coulour', 'coler', 'clour', 'colar', 'colr', 'culour', 'coleur'}


class Obj():
    def __init__(type, colour, state, rcpt):
        self.type = type
        self.colour = colour
        self.state = state
        self.rcpt = rcpt
        self.has_moved = False

    def set_moved():
        self.hasMoved = True


class Rcpt():
    def __init__(shape, colour, pos):
        self.shape = shape
        self.colour = colour
        self.pos = pos

class Obj_Manager():
    def __init__(self) -> None:
        obj_list = []
        prev_obj = []
        pass

    #takes the metadata from SLURK and converts it to a Python array
    def set_obj_list(metadat):
        return 0
    
    #Gets the next obj to be moved
    def get_obj():
        for o in self.obj_list:
            if not o.has_moved:
                self.prev_obj.push(o)
                return o
        #Task is completed
        return False
    
    def get_prev_obj():
        return self.prev_obj[-1]

    def get_obj_context(obj):
        return 0
    
obj_manager = Obj_Manager()


class Action_put_obj_on_rcpt(Action):
    def name(self) -> Text:
        return "Action_put_obj_on_rcpt"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     #To store the previous conversation. Same as rasa shell.
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    #Intents and Actions

        obj = obj_manager.get_obj()
        if(obj):
            slotvars = {
                "obj_description": obj_manager.get_obj_context(obj), 
                "rcpt": obj.rcpt
            }
        else:
            dispatcher.utter_message(response="uttter_ask_remaining_obj")  
        return []
    
class Action_confirm_obj_on_rcpt(Action):
    def name(self) -> Text:
        return "Action_confirm_obj_on_rcpt"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                   
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        obj = obj_manager.get_obj()
        if(obj):
            slotvars = {
                "obj": obj, 
                "rcpt": obj.rcpt
            }
        dispatcher.utter_message(response="utter_confirm_obj_in_rcpt", **slotvars)            
        return []
    
class Action_do_it(Action):
    def name(self) -> Text:
        return "Action_do_it"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        dispatcher.utter_message(response="utter_do_it")         
        return []
    


class Action_help_delete(Action):
    def name(self) -> Text:
        return "Action_help_delete"
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        dispatcher.utter_message(response="utter_help_delete")         
        return []
    
class Action_help_done(Action):
    def name(self) -> Text:
        return "Action_help_done"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        dispatcher.utter_message(response="utter_help_done")         
        return []
    
class Action_help_request(Action):
    def name(self) -> Text:
        return "Action_help_request"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        obj = obj_manager.get_obj()
        slotvars = {
                "obj": obj, 
            }
        dispatcher.utter_message(response="utter_help_spawn", **slotvars)  
        return []
    


class Action_describe_rcpt(Action):
    def name(self) -> Text:
        return "Action_describe_rcpt"
    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,                                     
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:    
        
        #Assuming we are talking about the last rcpt
        rcpt = obj_manager.get_obj().rcpt

        last_message =  tracker.latest_message.split()
        isColour = [e for e in last_message if e in word_varients_colour]

        #what colour is the rcpt
        if tracker.get_latest_entity_values("colour") != None:
            slotvars = {
                "rcpt": rcpt, 
                "colour": rcpt.colour()
            }
            dispatcher.utter_message(response="utter_rcpt_is_colour", **slotvars)  

        #what shape is the rcpt
        if tracker.get_latest_entity_values("shape") != None:
            slotvars = {
                "rcpt": rcpt, 
                "colour": rcpt.shape()
            }
            dispatcher.utter_message(response="utter_rcpt_is_shape", **slotvars)  

        #what pos is the rcpt
        if tracker.get_latest_entity_values("pos") != None:
            slotvars = {
                "rcpt": rcpt, 
                "colour": rcpt.pos()
            }
            dispatcher.utter_message(response="utter_rcpt_is_located", **slotvars)  

        #what obj is on rcpt
        if tracker.get_latest_entity_values("obj") != None:
            slotvars = {               
                "obj": obj,
                "rcpt": rcpt
            }
            dispatcher.utter_message(response="utter_obj_is_in_rcpt", **slotvars)  

        return []

