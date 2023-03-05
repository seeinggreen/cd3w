import os
import re
import time
import json

from ithor.utils.items import Items
from ithor.ithor_controller import IthorController


class IthorService:
    def __init__(self):
        self.leader_controller = None
        self.follower_controller = None

    def initialise_scenes(self, level, variant):
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

        # Initialise controllers
        self.leader_controller = IthorController()
        self.leader_controller.init_scene(pos=[0.25, 1, 0], rot=270, horizon=70)
        self.leader_controller.place_assets(leader_config)

        self.follower_controller = IthorController()
        self.follower_controller.init_scene(pos=[0.25, 1, 0], rot=270, horizon=70)
        self.follower_controller.place_assets(follower_config)

    def update_follower_ithor_scene(self, command):
        # Examples of expected commands:
        # "\\done", "\\discard #8", "\\request #1", "\\put #3 on #V", "put #3 on #table"

        item_slurk_id = re.findall("#\d+", command)
        if len(item_slurk_id) != 1:
            raise Exception(
                "You used an incorrect identifier for the item, please refer to the lookup sheet and try again"
            )
        item_slurk_id = item_slurk_id[0]
        item = Items().get_name_by_slurkid(item_slurk_id)
        if "discard" in command.lower():
            self.follower_controller.hide_asset(item)
            print(f"successfully discarded {item}")
        elif "request" in command.lower():
            self.follower_controller.place_asset_at_empty_location(item)
            print(f"successfully requested {item}")
        elif "slice" in command.lower():
            sliced_item_slurk_id = "#" + str(
                int(re.findall("\d+", item_slurk_id)[0]) + 1
            )
            sliced_item = Items().get_name_by_slurkid(sliced_item_slurk_id)
            if "Slice" not in sliced_item:
                raise Exception("This item can't be sliced. Try again with another!")
            self.follower_controller.hide_asset(item)
            self.follower_controller.place_asset_at_empty_location(sliced_item)
            print(f"successfully sliced {item}")
        else:
            # Pick up the specified item
            self.follower_controller.pickup(item)
            print(f"successfully picked up {item}")
            # Place item on the specified mat's slot or the table
            if "#table" in command.lower():
                self.follower_controller.place_asset_at_empty_location(item)
                print(f"successfully placed {item} on table")
            else:
                mat_slurk_id = re.findall("#[A-Z]", command)

                if len(mat_slurk_id) != 1:
                    raise Exception(
                        "You used an incorrect identifier for the mat or the item, please refer to the lookup sheet and try again"
                    )
                mat_slurk_id = mat_slurk_id[0]
                mat = Items().get_name_by_slurkid(mat_slurk_id)
                self.follower_controller.place_object_on_mat(item, mat)
                print(f"successfully placed {item} on {mat}")

    def snapshot_scene(self, agent_type):
        if agent_type == "leader":
            controller = self.leader_controller
        else:
            controller = self.follower_controller
        return controller.snapshot_scene()

    def get_follower_lookup_sheet(self):
        # TODO: Generate a lookup sheet instead of snapshotting the scene
        return self.follower_controller.snapshot_scene()
