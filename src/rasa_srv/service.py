import json
from functools import reduce
from ithor.utils.items import Items

from functools import reduce

import requests
from src.chatbot.chatbot_interface import *

class RasaException(Exception):
    pass


def send_msg_rasa(sender_id, msg):
    return requests.post(
        "http://localhost:5005/webhooks/rest/webhook", 
        json={
            "sender": sender_id, 
            "message": msg
        }
    )

get_res_msg = lambda res: res.json()[0]["text"]

is_res_success = lambda res: res.status_code == 200

get_att_OrDict = lambda d, k: d[k] if k in d else d




def get_items_matrix(m, list_items, get_item_fields):

    get_item = lambda l, name: list(filter(lambda item: item['name'] ==name, l))[0]

    items_flat_lst = list(
        map(
            lambda x: get_item_fields(x),
            filter(
                lambda x: x[2] != None,
                reduce(
                    lambda x, y: x+y,
                    map(
                        lambda i_lst: list(map(
                            lambda i_e: (
                                i_lst[0],
                                i_e[0],
                                None if i_e[1] == None else get_item(list_items, i_e[1])
                            ),
                            enumerate(i_lst[1])
                        )),
                        enumerate(m)
                    )
                )
            )
        )
    )

    return items_flat_lst


def get_rcpt_data(tupl):

    x=tupl[0]
    y=tupl[1]

    rcpt_dta = tupl[2]

    shape = "circle" if "ircle" in rcpt_dta['name'] else "square"

    return {
        "name": rcpt_dta['name'],
        "shape": shape,
        "colour": rcpt_dta["colour"].lower(),
        "pos": (x, y)
    }


def get_rcpts(m, list_rcpts):
    return get_items_matrix(m, list_rcpts, get_rcpt_data)


def get_scene_configs(level, variant, user):
    with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
        configs = json.load(json_file)

    return configs[level][variant][user]


def get_leader_scene(level, variant): 
    return get_scene_configs(level, variant, "leader")


def get_leader_rcpts(level, variant):
    mats = get_leader_scene(level, variant)["mats"]
    return mats

list_rcpt = []
list_obj = []

def set_list_rcpt(list_rcpt):
    list_rcpt = list_rcpt

def set_list_obj(list_obj):
    list_obj = list_obj


class RasaService:
    def __init__(self,port,level, varient):
        self.scene = None
        self.slurk_port = port
        self.metadata_objects, self.metadata_mats = self._get_metadata()
        self.level = level
        self.varient = varient

        set_list_rcpt(self.get_scene())
        set_list_obj(self.get_scene())

    def _get_metadata(self):
        assets = Items().assets

        objects = [a for a in assets if not a["is_mat"]]
        mats = self.mats = [a for a in assets if a["is_mat"]]

        return objects, mats
        # this can be used to get metadata like the color of a certain object or mat
        # in the scene of the current game
        #

    def get_scene(self):
        self.scene = get_leader_scene(self.level, self.variant)


        print("getting scene")
        print("\n\nscene: ", self.scene['mats'])

        self.scene['mats'] = get_rcpts(
            self.scene['mats'], 
            self.metadata_mats
        )

        print("\n\nNEW scene: ", self.scene['mats'])


        return self.scene['mats']

        # this is the method called when the bot joins the Slurk room
        # it makes the scene config of the current game available to be used in Rasa

    def get_response(self, follower_message):

        res = send_msg_rasa(self.slurk_port, follower_message)

        if is_res_success(res):
            return get_res_msg(res)
        else:
            raise RasaException("sender_id: ", self.slurk_port, ", message: ", follower_message)
        # this is the method called when the follower types a message in Slurk
        # IMPORTANT regardless of how we handle the passing of the message to Rasa
        # and getting the bot generated response, this method needs to return
        # a bot response as this will then be sent to the Slurk room

    def reset(self):

        self.scene = None
        # and whatever other stuff you need to reset


