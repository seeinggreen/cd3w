import json
import os

from src.argparsing import get_args
from src.ithor.ithor_controller import IthorController
from src.ithor.ithor_service import IthorService

# Get the experiment arguments from the command line
args = get_args()
token = args["token"]
user = args["user"]
level = args["level"]
variant = args["variant"]

print("Args")
print(f"{token}\n{user}\n{level}\{variant}")
print("*" * 20)

# Check if run as test or experiment and retrieve leader and follower configs from json file
if level == "t" or variant == "t":
    print("Using test configs")
    print("*" * 20)
    with open("ithor/test_configs.json") as json_file:
        configs = json.load(json_file)
    leader_config = configs["leader"]
    follower_config = configs["follower"]
else:
    print("WARNING - Using regular configs - SHOULD NOT HAPPEN")
    with open("ithor/scene_configs.json") as json_file:
        configs = json.load(json_file)
    leader_config = configs[level][variant]["leader"]
    follower_config = configs[level][variant]["follower"]

print("Configs - keys")
print(leader_config.keys())
print(follower_config.keys())
print("*" * 20)

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

print("Taking snapshots of initial scenes")
url = ithor_service.snapshot_scene("leader")
print(url)
print(os.listdir("../images"))
url = ithor_service.snapshot_scene("follower")
print(url)
print(os.listdir(f"{os.getcwd()}/images"))
print("*" * 20)

commands = [
    "\\done",
    "\\discard #8",
    "\\request #1",
    "\\put #3 on #V",
    "put #3 on #table",
]
for c in commands:
    print("Updating scene and creating image file")
    ithor_service.update_follower_ithor_scene(c)
    url = ithor_service.snapshot_scene("follower")
    print(url)
    print(os.listdir(f"{os.getcwd()}/images"))
    print("-" * 10)
print("*" * 20)
