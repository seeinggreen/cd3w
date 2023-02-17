class IthorManager:
    def __init__(self, leader_controller, follower_controller, level, variant):
        self.leader_controller = leader_controller
        self.follower_controller = follower_controller
        self.follower_path = f'follower_{level}_{variant}'
        self.follower_path = f'leader_{level}_{variant}'
        self.steps = 0

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
        
def initialise_ithor_scenes(level, variant):
    leader_controller = None # ADAPT THE CODE IN THE CURRENT main.py FOR THIS
    follower_controller = None # ADAPT THE CODE IN THE CURRENT main.py FOR THIS
    ithor_manager = IthorManager(leader_controller, follower_controller, level, variant)
    return ithor_manager