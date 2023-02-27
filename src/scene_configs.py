import json
import os
import re
import sys
from itertools import combinations
import numpy as np
from numpy.random import default_rng

from ithor.utils.items import Items
from ithor.utils.table import Table, VERTICAL_SLOTS, HORIZONTAL_SLOTS

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)


class Scene:
    def __init__(self, level, n_scenes=10):
        self.level = level
        self.n_scenes = n_scenes
        self.items = Items()
        self.assets = self.items.assets
        self.mats = [asset for asset in self.assets if self.items.is_mat(asset["name"])]
        self.objects = [
            asset for asset in self.assets if self.items.is_object(asset["name"])
        ]
        (
            self.mats_same_colour_same_type,
            self.mats_same_colour_different_type,
            self.mats_similar_colour_same_type,
        ) = self._generate_mat_combos()
        (
            self.obj_same_colour_different_state,
            self.obj_same_type_different_colour,
            self.obj_same_type_different_colour_state,
        ) = self._generate_object_combos()
        self.n_positions = 6
        self.position_combos = self._generate_position_combos()
        self.rng = default_rng()
        self.selected_mats = None
        self.selected_leader_objects = None
        self.selected_follower_objects = None
        self.selected_positions = None
        self.selected_follower_object_positions = None
        self.rules = {
            "l0": {
                "mat_rules": [self._sample_n_random_mats(6)],
                "object_rules": [self._sample_n_random_objects(6)],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l1": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_n_random_mats(4),
                ],
                "object_rules": [self._sample_n_random_objects(6)],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l2": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_n_random_mats(2),
                ],
                "object_rules": [self._sample_n_random_objects(6)],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l3": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [self._sample_n_random_objects(6)],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l4": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_n_random_objects(4),
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l5": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l6": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(
                        3
                    ),  # need to account for this by adding 1 position (7 objects)
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._delete_whole_object,
                    "follower": self._delete_sliced_object,
                },  # need to implement this
            },
            "l7": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._keep_all_objects,
                },
            },
            "l8": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(
                        3
                    ),  # need to account for this by adding 1 position (7 objects)
                ],
                "position_rules": [
                    self._generate_position_combos(7),
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._delete_object,
                    "follower": self._keep_all_objects,
                },  # when deleting object, also delete position
            },
            "l9": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._delete_object,
                },  # when deleting object, also delete position
            },
            "l10": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(self.obj_same_type_different_colour),
                    self._sample_from_objects(self.obj_same_colour_different_state),
                    self._sample_n_random_objects(
                        3
                    ),  # need to account for this by adding 1 position (7 objects)
                ],
                "position_rules": [
                    self._generate_position_combos,
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._delete_object,
                    "follower": self._delete_object,
                },  # when deleting object, also delete position
            },
        }

    # Helper functions
    # ================
    def _get_type(self, asset):
        return re.sub(
            "\d+\w*", "", asset["name"]
        ).lower()  # Discard the number (and state - for objects only)

    def _get_state(self, asset):
        state = re.sub(
            "\w*\d+", "", asset["name"]
        ).lower()  # Discard the name and number
        if state == "":
            return "whole"
        else:
            return state

    def _same_type(self, asset1, asset2):
        asset1_type = self._get_type(asset1)
        asset2_type = self._get_type(asset2)
        return asset1_type == asset2_type

    def _same_state(self, asset1, asset2):
        asset1_state = self._get_state(asset1)
        asset2_state = self._get_state(asset2)
        return asset1_state == asset2_state

    # Mats
    def _generate_mat_combos(self):
        colours = {mat["colour"] for mat in self.mats}
        mats_by_colour = {}
        same_colour_same_type = []
        same_colour_different_type = []
        temp_similar_colour_same_type = []
        for colour in colours:
            mats_by_colour[colour] = [
                mat for mat in self.mats if mat["colour"] == colour
            ]
            combos = list(combinations(mats_by_colour[colour], 2))
            # Check if colour is one of the purple colours
            if len(combos) == 1:
                for mat in mats_by_colour[colour]:
                    temp_similar_colour_same_type.append(mat)
            counter = 0
            for combo in combos:
                if self._same_type(combo[0], combo[1]):
                    same_colour_same_type.append(combo)
                else:
                    if counter == 0:
                        same_colour_different_type.append(combo)
                        counter += 1

        similar_colour_same_type = [
            combo
            for combo in combinations(temp_similar_colour_same_type, 2)
            if self._same_type(combo[0], combo[1])
        ]

        return (
            same_colour_same_type,
            same_colour_different_type,
            similar_colour_same_type,
        )

    # Objects
    def _generate_object_combos(self):
        types = {self._get_type(obj) for obj in self.objects}
        objs_by_type = {}
        same_colour_different_state = []
        same_type_different_colour = []
        same_type_different_colour_state = []
        for t in types:
            objs_by_type[t] = [obj for obj in self.objects if self._get_type(obj) == t]
            combos = list(combinations(objs_by_type[t], 2))
            for i, combo in enumerate(combos):
                if combo[0]["colour"] == combo[1]["colour"]:
                    same_colour_different_state.append(combo)
                else:
                    if self._same_state(combo[0], combo[1]):
                        same_type_different_colour.append(combo)
                    else:
                        same_type_different_colour_state.append(combo)
        return (
            same_colour_different_state,
            same_type_different_colour,
            same_type_different_colour_state,
        )

    # Positioning (for mats and leader objects)
    def _generate_position_combos(self, n_positions=6):
        available_positions = []
        for x in range(HORIZONTAL_SLOTS):
            for y in range(VERTICAL_SLOTS):
                if y == 2 and (x == 2 or x == 3):
                    continue
                else:
                    available_positions.append([x, y])

        return list(combinations(available_positions, n_positions))

    def _sample_from_mats(self, mat_combos):
        def execute(selected_mats):
            sample = np.random.choice(mat_combos, 1)
            while sample in selected_mats:
                sample = np.random.choice(mat_combos, 1)
            return sample

        return execute

    def _sample_n_random_mats(self, n_random):
        def execute(selected_mats):
            samples = []
            for i in range(n_random):
                sample = np.random.choice(self.mats, 1)
                while sample in selected_mats:
                    sample = np.random.choice(self.mat, 1)
                samples.append(sample)
            return samples

        return execute

    def _sample_from_objects(self, object_combos):
        def execute(selected_objects):
            sample = np.random.choice(object_combos, 1)
            while sample in selected_objects:
                sample = np.random.choice(object_combos, 1)
            return sample

        return execute

    def _sample_n_random_objects(self, n_random):
        def execute(selected_objects):
            samples = []
            for i in range(n_random):
                sample = np.random.choice(self.objects, 1)
                while sample in selected_objects:
                    sample = np.random.choice(self.objects, 1)
                samples.append(sample)
            return samples

        return execute

    def _sample_from_positions(self):
        sample = np.random.choice(self.position_combos, 1)

        return sample

    def _get_empty_positions(self, selected_positions):
        empty_positions = []
        for x in range(HORIZONTAL_SLOTS):
            for y in range(VERTICAL_SLOTS):
                if y == 2 and (x == 2 or x == 3):
                    continue
                if [x, y] in selected_positions:
                    continue
                else:
                    empty_positions.append([x, y])
        return empty_positions

    def _only_empty_positions(self):
        def execute(selected_positions):
            empty_positions = self._get_empty_positions(selected_positions)
            return empty_positions

        return execute

    def _include_mat_position(self):
        def execute(selected_positions):
            empty_positions = self._get_empty_positions(selected_positions)
            random_mat_position = np.random.choice(selected_positions, 1)
            random_id = self.rng.randint(len(empty_positions))
            positions_incl_mat = empty_positions
            positions_incl_mat[random_id] = random_mat_position
            return positions_incl_mat

        return execute

    def _keep_all_objects(self):
        def execute(selected_objects):
            return selected_objects

        return execute

    def _delete_object(self):
        def execute(selected_objects):
            random_id = self.rng.randint(len(selected_objects))
            final_objects = selected_objects
            final_objects[random_id] = None
            return final_objects

        return execute

    # ================

    def get_configs(self):
        leve_rules = self.rules[self.level]

        selected_mats = []
        for funct in level_rules["mat_rules"]:
            selected_mats.append(funct(selected_mats))
        self.selected_mats = selected_mats

        selected_objects = []
        for funct in level_rules["object_rules"]:
            selected_objects.append(funct(selected_objects))
        self.selected_leader_objects = level_rules["inclusion_rules"]["leader"](
            selected_objects
        )
        self.selected_follower_objects = level_rules["inclusion_rules"]["follower"](
            selected_objects
        )

        self.selected_positions = level_rules["position_rules"][0]
        self.selected_follower_object_positions = level_rules["positions_rules"][1](
            self.selected_positions
        )

    def make_table(self):
        mats = Table.get_empty_slots_list()
        for i, pos in enumerate(self.selected_positions):
            mats[pos[0]][pos[1]] = self.selected_mats[i]

        # Get an empty list and specify goal object positions
        leader_objects = Table.get_empty_slots_list()
        for i, pos in enumerate(self.selected_positions):
            leader_objects[pos[0]][pos[1]] = self.selected_leader_objects[i]

        follower_objects = Table.get_empty_slots_list()
        for i, pos in enumerate(self.selected_follower_object_positions):
            follower_objects[pos[0]][pos[1]] = self.selected_follower_objects[i]

        # Create a Table object with the mats and objects specified
        leader_config = {"mats": mats, "objects": leader_objects}
        follower_config = {"mats": mats, "objects": follower_objects}

        self.configs = {"leader": leader_config, "follower": follower_config}
        return self.configs


config = {}
for level in ["l1", "l2"]:
    config[level] = {}
    for variant in range(2):
        scene = Scene(level)
        scene.get_configs()
        config[level][variant] = scene.make_table()

with open(f"src/ithor/configs.json", "w") as outfile:
    json.dump(config, outfile)
