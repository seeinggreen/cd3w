import json
import os
import sys

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from argparsing import get_args
from ithor.ithor_controller import IthorController
from ithor.ithor_service import IthorService
from slurk.slurk_bot import SlurkBot

if __name__ == "__main__":
    # Get the experiment arguments from the command line
    args = get_args()
    token = args["token"]
    user = args["user"]
    level = args["level"]
    variant = args["variant"]

    # Check if run as test or experiment and retrieve leader and follower configs from json file
    if level == "t" or variant == "t":
        with open("src/ithor/test_configs.json", encoding="utf-8") as json_file:
            configs = json.load(json_file)
        leader_config = configs["leader"]
        follower_config = configs["follower"]
    else:
        with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
            configs = json.load(json_file)
        leader_config = configs[level][variant]["leader"]
        follower_config = configs[level][variant]["follower"]

    # Create a filename base for saving scene
    image_filename_base = f"{level}_{variant}"

    # Create IthorController instances for leader and follower and set up scenes
    leader_controller = IthorController(leader_config)
    leader_controller.init_scene(pos=[0.25, 1, 0], rot=270, horizon=70)
    leader_controller.place_assets()

    follower_controller = IthorController(follower_config)
    follower_controller.init_scene(pos=[0.25, 1, 0], rot=270, horizon=70)
    follower_controller.place_assets()

    # Instantiate IthorService with the leader and follower controllers
    ithor_service = IthorService(
        leader_controller, follower_controller, image_filename_base
    )

    # Instantiate and start up SlurkBot with the IthorService
    slurk_bot = SlurkBot(token, user, "localhost", 5000, ithor_service)
    slurk_bot.run()
