import os
import re

from .utils.items import Items


class IthorService:
    def __init__(self, leader_controller, follower_controller, image_filename_base):
        self.leader_controller = leader_controller
        self.follower_controller = follower_controller
        self.image_filename_base = image_filename_base
        self.steps = 0

    def update_follower_ithor_scene(self, command):
        self.steps += 1

        # Examples of expected commands:
        # "\\done", "\\discard #8", "\\request #1", "\\put #3 on #V", "put #3 on #table"

        if "done" in command.lower():
            self.follower_controller.stop()
            print("done")
        else:
            object_slurk_id = re.findall("#\d+", command)
            assert (
                len(object_slurk_id) == 1
            ), "Used an incorrect identifier, please try again"
            object_slurk_id = object_slurk_id[0]
            object = Items().get_name_by_slurkid(object_slurk_id)
            if "discard" in command.lower():
                self.follower_controller.hide_asset(object)
                print(f"discarding {object}")
            elif "request" in command.lower():
                self.follower_controller.place_asset_at_empty_location(object)
                print(f"requesting {object}")
            else:
                # Pick up the specified object
                self.follower_controller.pickup(object)
                print(f"picking up {object}")
                # Place object on the specified mat's slot or the table
                if "#table" in command.lower():
                    self.follower_controller.place_asset_at_empty_location(object)
                    print(f"placing {object} on table")
                else:
                    mat_slurk_id = re.findall("#[A-Z]", command)
                    assert (
                        len(mat_slurk_id) == 1
                    ), "Used an incorrect identifier, please try again"
                    mat_slurk_id = mat_slurk_id[0]
                    mat = Items().get_name_by_slurkid(mat_slurk_id)
                    self.follower_controller.place_asset_on_mat(object, mat)
                    print(f"placing {object} on {mat}")

    def snapshot_scene(self, agent_type):
        if agent_type == "leader":
            controller = self.leader_controller
        else:
            controller = self.follower_controller
        snapshot_filename = f"{self.image_filename_base}_{agent_type}_{self.steps}"  # 0 represents initial scenes
        controller.save_img(snapshot_filename)
        snapshot_path = os.path.join(controller.image_dir, snapshot_filename)
        return snapshot_path
