import re
import os


class IthorService:
    def __init__(self, leader_controller, follower_controller, image_filename_base):
        self.leader_controller = leader_controller
        self.follower_controller = follower_controller
        self.image_filename_base = image_filename_base
        self.steps = 0

    def update_follower_ithor_scene(self, command):
        self.steps += 1

        # Examples of expected commands:
        # "\done", "\discard Cup2", "\request Apple1", "\put Apple2 on Circle9"

        if "done" in command.lower():
            self.follower_controller.stop()
        else:
            asset_slurk_ids = [o.capitalize() for o in re.findall("#.*", command)]
            assets = 
            if "discard" in command.lower():
                self.follower_controller.hide_asset(assets[0])
            if "request" in command.lower():
                self.follower_controller.place_asset_at_empty_location(assets[0])
            else:
                # Pick up the specified object
                self.follower_controller.pickup(assets[0])
                # Place object on the specified mat's slot or the table
                if "table" in command.lower():
                    self.follower_controller.place_asset_at_empty_location(assets[0])
                else:
                    assert (
                        len(assets) == 2
                    ), "Specify the object and where you want to put it"
                    self.follower_controller.place_asset_on_mat(assets[0], assets[1])

    def snapshot_scene(self, agent_type):
        if agent_type == "leader":
            controller = self.leader_controller
        else:
            controller = self.follower_controller
        snapshot_filename = f"{self.image_filename_base}_{agent_type}_{self.steps}"  # 0 represents initial scenes
        controller.save_img(snapshot_filename)
        snapshot_path = os.path.join(controller.image_dir, snapshot_filename)
        return snapshot_path
