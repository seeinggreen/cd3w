import json
from ithor import IthorManager
from slurk import SlurkBot
from argparsing import get_args

args = get_args()
token = args["token"]
user = args["variant"]
level = args["level"]
variant = args["variant"]

with open('scene_configs.json') as json_file:
    scene_configs = json.load(json_file)
scene_config = scene_configs[level][variant]
scene_root_path = f'images/{level}_{variant}'
ithor_manager = IthorManager(scene_config, scene_root_path)

slurk_bot = SlurkBot(token, user, 'localhost', 5000, ithor_manager)
slurk_bot.run() 

