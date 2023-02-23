import os
import re

from ithor.utils.items import Items


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
            print("successfully stopped experiment")
        else:
            item_slurk_id = re.findall("#\d+", command)
            assert (
                len(item_slurk_id) == 1
            ), "Used an incorrect identifier, please try again"
            item_slurk_id = item_slurk_id[0]
            item = Items().get_name_by_slurkid(item_slurk_id)
            if "discard" in command.lower():
                self.follower_controller.hide_asset(item)
                print(f"successfully discarded {item}")
            elif "request" in command.lower():
                self.follower_controller.place_asset_at_empty_location(item)
                print(f"successfully requested {item}")
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
                    assert (
                        len(mat_slurk_id) == 1
                    ), "Used an incorrect identifier, please try again"
                    mat_slurk_id = mat_slurk_id[0]
                    mat = Items().get_name_by_slurkid(mat_slurk_id)
                    self.follower_controller.place_object_on_mat(item, mat)
                    print(f"successfully placed {item} on {mat}")

    def snapshot_scene(self, agent_type):
        if agent_type == "leader":
            controller = self.leader_controller
        else:
            controller = self.follower_controller
        snapshot_filename = f"{self.image_filename_base}_{agent_type}_{self.steps}.jpg"  # 0 represents initial scenes
        controller.save_img(snapshot_filename)
        snapshot_path = os.path.join(controller.image_dir, snapshot_filename)
        return snapshot_path
