import json
from functools import reduce
from ithor.utils.items import Items



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



class RasaService:
    def __init__(self,port):
        self.scene = None
        self.slurk_port = port
        self.metadata_objects, self.metadata_mats = self._get_metadata()


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

        self.scene['mats'] = self.map_matrix(
            self.scene['mats'], 
            self.metadata_mats,
            lambda mat: {
                'name': mat['name'],
                'colour': mat['colour'],
                'is_mat': mat['is_mat'],
                'home_pos': mat['home_pos']
            }
        )

        print("\n\n NEW scene: ", self.scene['mats'])

        print("\n\nget element: ", self.get_element_matrix(self.scene['mats'], "Circle4"))

        return self.scene['mats']

        # this is the method called when the bot joins the Slurk room
        # it makes the scene config of the current game available to be used in Rasa

    def get_response(self, follower_message, sender_id):

        res = send_msg_rasa(sender_id, follower_message)

        if is_res_success(res):
            return get_res_msg(res)
        else:
            raise RasaException("sender_id: ", sender_id, ", message: ", follower_message)
        # this is the method called when the follower types a message in Slurk
        # IMPORTANT regardless of how we handle the passing of the message to Rasa
        # and getting the bot generated response, this method needs to return
        # a bot response as this will then be sent to the Slurk room

    def reset(self):

        self.scene = None
        # and whatever other stuff you need to reset



    def map_matrix(self, m, list_items, f_item=lambda x: x):

        get_item = lambda l, name: list(filter(lambda item: item['name'] ==name, l))[0]

        return list(map(
            lambda lst: list(map(
                lambda l_element_name: (
                    None if l_element_name == None else f_item(
                        get_item(list_items, l_element_name)
                    )
                ),
                lst
            )),
            m
        ))

    

    def get_element_matrix(self, m, name_element, name_attribute=False):

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

