from src.ithor_controller import IthorController
from src.table import Table

class IthorManager:
    def __init__(self, level, variant):
        self.leader_controller, self.follower_controller = self.initialise_scenes()
        self.level = level
        self.variant = variant
        self.follower_path = f'images/follower_{level}_{variant}'
        self.follower_path = f'images/leader_{level}_{variant}'
        self.steps = 0

    def initialise_scenes(self):
        # IMPLEMENT THIS METHOD
        leader_controller = None
        follower_controller = None
        return leader_controller, follower_controller

    def update_follower_ithor_scene(self, command):
        self.steps += 1
        # IMPLEMENT THIS METHOD

    def snapshot_scene(self, agent_type):
        if agent_type == 'leader':
            base_path = self.leader_path
            controller = self.leader_controller
        else:
            base_path = self.follower_path
            controller = self.follower_controller            
        # IMPLEMENT CREATION OF IMAGE USING SOME OF THE CODE IN THE CURRENT main.py
        image_url = f'{base_path}_{self.steps}'
        return image_url