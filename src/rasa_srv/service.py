import json
from functools import reduce

from sqlalchemy.sql.elements import False_
from ithor.utils.items import Items

from functools import reduce

import requests
import re


class RasaException(Exception):
    pass


def send_msg_rasa(sender_id, msg):
    return requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": sender_id, "message": msg},
    )


get_res_msg = lambda res: res.json()[0]["text"]

is_res_success = lambda res: res.status_code == 200

get_att_OrDict = lambda d, k: d[k] if k in d else d


def get_items_matrix(m, list_items, get_item_fields):

    get_item = lambda l, name: list(filter(lambda item: item["name"] == name, l))[0]

    items_flat_lst = list(
        map(
            lambda x: get_item_fields(x),
            filter(
                lambda x: x[2] != None,
                reduce(
                    lambda x, y: x + y,
                    map(
                        lambda i_lst: list(
                            map(
                                lambda i_e: (
                                    i_lst[0],
                                    i_e[0],
                                    None
                                    if i_e[1] == None
                                    else get_item(list_items, i_e[1]),
                                ),
                                enumerate(i_lst[1]),
                            )
                        ),
                        enumerate(m),
                    ),
                ),
            ),
        )
    )

    return items_flat_lst


splitName = lambda s: re.split("(\d+)", s)


def get_rcpt_data(tupl):

    x = tupl[0]
    y = tupl[1]

    rcpt_dta = tupl[2]

    name = splitName(rcpt_dta["name"])[0].lower()

    shape = "circle" if "ircle" in rcpt_dta["name"] else "square"

    return {
        "id": rcpt_dta["name"],
        "name": "mat",
        "shape": shape,
        "colour": rcpt_dta["colour"].lower(),
        "pos": (x, y),
    }


def get_obj_data(tupl):

    x = tupl[0]
    y = tupl[1]

    obj_dta = tupl[2]

    isSliced = "lice" in obj_dta["name"]

    name = splitName(obj_dta["name"])[0].lower()

    return {
        "id": obj_dta["name"],
        "name": name,
        "colour": obj_dta["colour"].lower(),
        "hasMoved": False,
        "isSliced": isSliced,
        "pos": (x, y),
    }


def get_rcpts(m, list_rcpts):
    return get_items_matrix(m, list_rcpts, get_rcpt_data)


def get_objs(m, list_rcpts):
    return get_items_matrix(m, list_rcpts, get_obj_data)


def get_scene_configs(level, variant, user):
    with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
        configs = json.load(json_file)

    return configs[level][variant][user]


def get_leader_scene(level, variant):
    return get_scene_configs(level, variant, "leader")


def read_json(slurk_port, item_type):
    filename = str(slurk_port) + "_" + item_type
    with open(f"src/rasa_srv/lead_configs/{filename}.json", encoding="utf-8") as jFile:
        data = json.load(jFile)
    return data


def read_obj_json(slurk_port):
    return read_json(slurk_port, "obj")


def read_rcpt_json(slurk_port):
    return read_json(slurk_port, "rcpt")


def write_json(slurk_port, item_type, dct):
    filename = str(slurk_port) + "_" + item_type
    with open(f"src/rasa_srv/lead_configs/{filename}.json", "w") as outfile:
        json.dump(dct, outfile)


def write_obj_json(slurk_port, dct):
    write_json(slurk_port, "obj", dct)


def write_rcpt_json(slurk_port, dct):
    write_json(slurk_port, "rcpt", dct)


BOT_VARIANT_MAPPING = {"v5": 1, "v6": 1, "v7": 2, "v8": 2, "v9": 3, "v10": 3}


class RasaService:
    def __init__(self, port, level, variant, write_file=False):
        self.scene = None
        self.slurk_port = port
        self.metadata_objects, self.metadata_mats = self._get_metadata()
        self.level = level
        self.variant = variant
        self.bot_variant = (
            BOT_VARIANT_MAPPING[self.variant]
            if self.variant in BOT_VARIANT_MAPPING.keys()
            else 2
        )

        if write_file:
            mats, objs = self.get_scene()

            write_rcpt_json(self.slurk_port, mats)
            write_obj_json(self.slurk_port, objs)

    def write_rcpts(self):
        return

    def write_objs(self):
        return

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

        self.scene["mats"] = get_rcpts(self.scene["mats"], self.metadata_mats)

        self.scene["objs"] = get_objs(self.scene["objects"], self.metadata_objects)

        return self.scene["mats"], self.scene["objs"]

        # this is the method called when the bot joins the Slurk room
        # it makes the scene config of the current game available to be used in Rasa

    def get_response(self, follower_message):

        res = send_msg_rasa(self.slurk_port, follower_message)

        if is_res_success(res):
            return get_res_msg(res)
        else:
            raise RasaException(
                "sender_id: ", self.slurk_port, ", message: ", follower_message
            )
        # this is the method called when the follower types a message in Slurk
        # IMPORTANT regardless of how we handle the passing of the message to Rasa
        # and getting the bot generated response, this method needs to return
        # a bot response as this will then be sent to the Slurk room

    def reset(self):

        self.scene = None
        # and whatever other stuff you need to reset
