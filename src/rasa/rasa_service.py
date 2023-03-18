import json
from ithor.utils.items import Items


class RasaService:
    def __init__(self):
        self.scene = None
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
        # this is the method called when the bot joins the Slurk room
        # it makes the scene config of the current game available to be used in Rasa

    def get_response(self, follower_message):
        bot_response = "TEST"
        return bot_response
        # this is the method called when the follower types a message in Slurk
        # IMPORTANT regardless of how we handle the passing of the message to Rasa
        # and getting the bot generated response, this method needs to return
        # a bot response as this will then be sent to the Slurk room

    def reset(self):
        self.scene = None
        # and whatever other stuff you need to reset
