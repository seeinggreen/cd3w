import json
from functools import reduce
from ithor.utils.items import Items

from functools import reduce

import requests


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


def get_element_matrix(m, name_element, name_attribute=False):

    f = lambda d:d

    if name_attribute != False: 
        f = lambda d: get_att_OrDict(d, name_attribute)

    els = list(filter(
        lambda e: e != None and e['name'] == name_element,
        reduce(
            lambda xs, x: xs+x, 
            m
        )
    ))

    if len(els) == 0: return False

    return f(els[0])


class RasaService:
    def __init__(self,port, sender_id=0):
        self.scene = None
        self.slurk_port = port
        self.metadata_objects, self.metadata_mats = self._get_metadata()
        self.sender_id = sender_id

    def _get_metadata(self):
        assets = Items().assets

        objects = [a for a in assets if not a["is_mat"]]
        mats = self.mats = [a for a in assets if a["is_mat"]]

        return objects, mats
        # this can be used to get metadata like the color of a certain object or mat
        # in the scene of the current game
        #

    def get_scene(self, level, variant):
        with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
            configs = json.load(json_file)
        self.scene = configs[level][variant]["leader"]

        # store in a data structure for rasa

        #`for obj
            # id
            # colour
            # shape
            # attributes metadata file

        print("getting scene")
        print("\n\nscene: ", self.scene['mats'])

        self.scene['mats'] = get_rcpts(
            self.scene['mats'], 
            self.metadata_mats
        )

        print("\n\nNEW scene: ", self.scene['mats'])

        print("\n\nobjs: ", self.scene['mats'])


        #print("elements: ", self.get_element_matrix(
            #self.scene['mats'],
            #"Square2"
        #))


        return self.scene['mats']

        # this is the method called when the bot joins the Slurk room
        # it makes the scene config of the current game available to be used in Rasa

    def get_response(self, follower_message):

        res = send_msg_rasa(self.sender_id, follower_message)

        if is_res_success(res):
            return get_res_msg(res)
        else:
            raise RasaException("sender_id: ", self.sender_id, ", message: ", follower_message)
        # this is the method called when the follower types a message in Slurk
        # IMPORTANT regardless of how we handle the passing of the message to Rasa
        # and getting the bot generated response, this method needs to return
        # a bot response as this will then be sent to the Slurk room

    def reset(self):

        self.scene = None
        # and whatever other stuff you need to reset


