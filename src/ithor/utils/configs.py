from table import Table
import json

# TO DO: Implement for experiments (permutations) to save in scene_configs.json

def save_test_configs():
    # Get an empty list of positions and specify which mats go where
    mats = Table.get_empty_slots_list()
    mats[0][0] = "Circle1"
    mats[0][2] = "Circle11"
    mats[1][0] = "Square12"
    mats[1][1] = "Circle13"
    mats[1][2] = "Circle7"
    mats[3][0] = "Square3"

    # Get an empty list and specify goal object positions
    leader_objects = Table.get_empty_slots_list()
    leader_objects[0][0] = "Vase1"
    leader_objects[0][2] = "Plate1"
    leader_objects[1][0] = "Cup1"
    leader_objects[1][1] = "Cup2"
    leader_objects[1][2] = "Apple1"
    leader_objects[3][0] = "Bread2Slice"

    follower_objects = Table.get_empty_slots_list()
    leader_objects[0][1] = "Vase1"
    leader_objects[2][0] = "Plate1"
    leader_objects[2][1] = "Cup1"
    leader_objects[3][1] = "Cup2"
    leader_objects[4][0] = "Apple1"
    leader_objects[4][1] = "Bread2Slice"

    # Create a Table object with the mats and objects specified
    leader_config = {"mats": mats, "objects": leader_objects}
    follower_config = {"mats": mats, "objects": follower_objects}

    configs = {"leader": leader_config, "follower": follower_config}

    with open("src/test_configs.json", "w") as outfile:
        json.dump(configs, outfile)