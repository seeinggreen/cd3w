from src.ithor_controller import IthorController
from src.table import Table

class IthorManager:
    def __init__(self, config, root_path):
        self.leader_controller, self.follower_controller = self.initialise_scenes()
        self.config = config
        self.root_path = root_path
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
            controller = self.leader_controller
        else:
            controller = self.follower_controller     
        snapshot_path = f'{self.root_path}_{agent_type}_{self.steps}' # 0 represents initial scenes       
        # IMPLEMENT CREATION OF IMAGE USING SOME OF THE CODE IN THE CURRENT main.py
        return snapshot_path