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


class affirm(Action):
    def name(self) -> Text:
        return "affirm"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker)
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
        print(tracker)
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
        print(tracker)
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
        print(tracker)
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
        print("tracker                      :   "+tracker                   )
        print("tracker.sender_id            :   "+tracker.sender_id         )
        print("tracker.slots                :   "+tracker.slots             )
        print("tracker.latest_message       :   "+tracker.latest_message    )
        print("tracker.events               :   "+tracker.events            )
        print("tracker.active_loop          :   "+tracker.active_loop       )
        print("tracker.latest_action_name   :   "+tracker.latest_action_name)
        slotvars = {
            "objRcpt": "OBJRCPT",
            "colour": "COLOUR"
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
        print(tracker)
        slotvars = {
            "rcpt": "RCPT",
            "shape": "SHAPE"
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
        print(tracker)
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
        print(tracker)

        slotvars = {
            "obj": "OBJ",
            "state": "STATE"
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
        print(tracker)
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
        print(tracker)
        slotvars = {
            "obj": "OBJ",
            "rcpt": "RCPT"
        }
        dispatcher.utter_message(response="utter_tell_next_step", **slotvars)
        return []


class tell_me_when_done(Action):
    def name(self) -> Text:
        return "tell_me_when_done"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker)
        slotvars = {
            
        }
        dispatcher.utter_message(
            response="utter_tell_me_when_done", **slotvars)
        return []
