from table import Table


class Scene:
    def __init__(self, mission) -> None:
        self.mission = mission
        self.permutations = dict()

    def generate_permutations(self):
        pass

    def get_config(self):
        if self.mission == "Test":
            mats = Table.get_empty_slots_list()
            mats[0][0] = "Circle1"
            mats[0][2] = "Circle11"
            mats[1][0] = "Square12"
            mats[1][1] = "Circle13"
            mats[1][2] = "Circle7"
            mats[3][0] = "Square3"

            objects = Table.get_empty_slots_list()
            objects[0][0] = "Apple1Slice"
            objects[0][2] = "Apple3"
            objects[1][0] = "Cup1"
            objects[3][0] = "Bread2Slice"
        return mats, objects

    def update_scene(self):
        pass
