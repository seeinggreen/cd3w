import copy
import json
import os
import random
import re
import sys
from datetime import date
from itertools import combinations

from numpy.random import default_rng

from ithor.utils.items import Items
from ithor.utils.table import HORIZONTAL_SLOTS, VERTICAL_SLOTS, Table

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)


class SceneConfigurator:
    def __init__(self, level):
        self.level = level
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
            self.same_type_same_colour_different_state,
            self.same_type_different_colour_same_state,
            self.same_type_different_colour_different_state,
        ) = self._generate_object_combos()
        self.position_combos_6_pos = self._generate_position_combos(6)
        self.position_combos_7_pos = self._generate_position_combos(7)
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
                    self._sample_from_positions(6),
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
                    self._sample_from_positions(6),
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
                    self._sample_from_positions(6),
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
                    self._sample_from_positions(6),
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
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_n_random_objects(4),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
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
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
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
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(3),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
                    self._only_empty_positions,
                ],
                "inclusion_rules": {
                    "leader": self._delete_object_notsliced,
                    "follower": self._delete_object_sliced,
                },
            },
            "l7": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
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
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(3),
                ],
                "position_rules": [
                    self._sample_from_positions(7),
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._delete_object,
                    "follower": self._keep_all_objects,
                },
            },
            "l9": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(2),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._keep_all_objects,
                    "follower": self._delete_object,
                },
            },
            "l10": {
                "mat_rules": [
                    self._sample_from_mats(self.mats_same_colour_different_type),
                    self._sample_from_mats(self.mats_similar_colour_same_type),
                    self._sample_from_mats(self.mats_same_colour_same_type),
                ],
                "object_rules": [
                    self._sample_from_objects(
                        self.same_type_different_colour_same_state
                    ),
                    self._sample_from_objects(
                        self.same_type_same_colour_different_state
                    ),
                    self._sample_n_random_objects(3),
                ],
                "position_rules": [
                    self._sample_from_positions(6),
                    self._include_mat_position,
                ],
                "inclusion_rules": {
                    "leader": self._delete_object,
                    "follower": self._delete_object,
                },  # when deleting object, also delete position
            },
        }

    # HELPER METHODS
    # ================
    def _get_type(self, asset):
        return re.sub(
            "\d+\w*", "", asset["name"]
        )  # Discard the number (and state - for objects only)

    def _get_state(self, asset):
        state = re.sub("\w*\d+", "", asset["name"])  # Discard the name and number
        if state == "":
            return "NotSliced"
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
                continue
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
        same_type_same_colour_different_state = []
        same_type_different_colour_same_state = []
        same_type_different_colour_different_state = []
        for t in types:
            objs_by_type[t] = [obj for obj in self.objects if self._get_type(obj) == t]
            combos = list(combinations(objs_by_type[t], 2))
            for i, combo in enumerate(combos):
                if combo[0]["colour"] == combo[1]["colour"]:
                    if not self._same_state(combo[0], combo[1]):
                        same_type_same_colour_different_state.append(combo)
                else:
                    if not self._same_state(combo[0], combo[1]):
                        same_type_different_colour_different_state.append(combo)
                    else:
                        same_type_different_colour_same_state.append(combo)

        return (
            same_type_same_colour_different_state,
            same_type_different_colour_same_state,
            same_type_different_colour_different_state,
        )

    # Positioning (for mats and leader objects)
    def _generate_position_combos(self, n_positions):
        available_positions = []
        for x in range(HORIZONTAL_SLOTS):
            for y in range(VERTICAL_SLOTS):
                if y == 2 and (x == 2 or x == 3):
                    continue
                else:
                    available_positions.append([x, y])

        return list(combinations(available_positions, n_positions))

    def _sample_from_mats(
        self, mat_combos
    ):  # TO DO INCLUDE CHECK FOR DUPLICATE OBJECTS
        def execute(selected_mats):
            sample = None
            while (
                sample is None
                or str(sample[0]["name"]) in str(selected_mats)
                or str(sample[1]["name"]) in str(selected_mats)
                or str(sample[0]["colour"]) in str(selected_mats)
                or str(sample[1]["colour"]) in str(selected_mats)
                or (
                    str(sample[0]["colour"]) in ["Violet", "Indigo", "Iris"]
                    and (
                        "Violet" in str(selected_mats)
                        or "Indigo" in str(selected_mats)
                        or "Iris" in str(selected_mats)
                    )
                )
                or (
                    str(sample[1]["colour"]) in ["Violet", "Indigo", "Iris"]
                    and (
                        "Violet" in str(selected_mats)
                        or "Indigo" in str(selected_mats)
                        or "Iris" in str(selected_mats)
                    )
                )
            ):
                random_id = self.rng.integers(len(mat_combos))
                sample = mat_combos[random_id]
            return sample

        return execute

    def _sample_n_random_mats(self, n_random):
        def execute(selected_mats):
            samples = []
            for i in range(n_random):
                sample = None
                # Catching exact duplicates
                while (
                    sample is None
                    or str(sample["name"]) in str(selected_mats)
                    or str(sample["name"]) in str(samples)
                    or str(sample["colour"]) in str(selected_mats)
                    or str(sample["colour"]) in str(samples)
                    or (
                        str(sample["colour"]) in ["Violet", "Indigo", "Iris"]
                        and (
                            "Violet" in str(selected_mats)
                            or "Violet" in str(samples)
                            or "Indigo" in str(selected_mats)
                            or "Indigo" in str(samples)
                            or "Iris" in str(selected_mats)
                            or "Iris" in str(samples)
                        )
                    )
                ):
                    random_id = self.rng.integers(len(self.mats))
                    sample = self.mats[random_id]
                samples.append(sample)
            return samples

        return execute

    def _sample_from_objects(self, object_combos):
        def execute(selected_objects):
            sample = None
            # Catching exact duplicates and unwanted sliced/not_sliced object combos
            while (
                not sample
                or str(sample[0]["name"]) in str(selected_objects)
                or str(sample[1]["name"]) in str(selected_objects)
                or str(self._get_type(sample[0])) in str(selected_objects)
                or str(self._get_type(sample[1])) in str(selected_objects)
            ):
                random_id = self.rng.integers(len(object_combos))
                sample = object_combos[random_id]
            return sample

        return execute

    def _sample_n_random_objects(self, n_random):
        def execute(selected_objects):
            samples = []
            for i in range(n_random):
                sample = None
                # Catching exact duplicates and unwanted sliced/not_sliced object combos
                while (
                    sample is None
                    or str(sample["name"]) in str(samples)
                    or str(sample["name"]) in str(selected_objects)
                    or str(self._get_type(sample)) in str(samples)
                    or str(self._get_type(sample)) in str(selected_objects)
                ):
                    random_id = self.rng.integers(len(self.objects))
                    sample = self.objects[random_id]
                samples.append(sample)
            return samples

        return execute

    def _sample_from_positions(self, n_positions):
        if n_positions == 6:
            position_combos = self.position_combos_6_pos
        else:
            position_combos = self.position_combos_7_pos
        random_id = self.rng.integers(len(position_combos))
        sample = position_combos[random_id]

        return sample

    def _get_empty_positions(self, selected_positions):
        empty_positions = []
        for x in range(HORIZONTAL_SLOTS):
            for y in range(VERTICAL_SLOTS):
                if y == 2 and (x == 2 or x == 3):
                    continue
                position = [x, y]
                if position in selected_positions:
                    continue
                else:
                    empty_positions.append([x, y])
        random.shuffle(empty_positions)
        return empty_positions[: len(selected_positions)]

    def _only_empty_positions(self, selected_positions):
        empty_positions = self._get_empty_positions(selected_positions)
        return empty_positions

    def _include_mat_position(self, selected_positions):
        empty_positions = self._get_empty_positions(selected_positions)
        random_id = self.rng.integers(len(empty_positions))
        positions_incl_mat = copy.deepcopy(empty_positions)
        positions_incl_mat[random_id] = selected_positions[random_id]
        return positions_incl_mat

    def _keep_all_objects(self, selected_objects):
        return selected_objects

    def _delete_object(self, selected_objects):
        random_id = None
        # The first two pairs of objects should be the same across leader and follower scenes
        # as these are the objects corresponding to the obj_prop skills
        while not random_id or random_id < 4:
            random_id = self.rng.integers(len(selected_objects))
        final_objects = copy.deepcopy(selected_objects)
        final_objects[random_id] = None
        return final_objects

    def _delete_object_sliced(self, selected_objects):
        final_objects = copy.deepcopy(selected_objects)
        for i, obj in enumerate(selected_objects):
            if "Slice" in obj and i in [2, 3]:
                final_objects.remove(obj)
            else:
                continue
        return final_objects

    def _delete_object_notsliced(self, selected_objects):
        final_objects = copy.deepcopy(selected_objects)
        for i, obj in enumerate(selected_objects):
            if not "Slice" in obj and i in [2, 3]:
                final_objects.remove(obj)
            else:
                continue
        return final_objects

    # EXTERNAL METHODS
    # ================

    def get_configs(self):
        level_rules = self.rules[self.level]

        selected_mats = []
        for funct in level_rules["mat_rules"]:
            selected_mats.extend(funct(selected_mats))
        self.selected_mats = [mat["name"] for mat in selected_mats]

        selected_objects = []
        for funct in level_rules["object_rules"]:
            selected_objects.extend(funct(selected_objects))
        selected_objects = [obj["name"] for obj in selected_objects]

        self.selected_leader_objects = level_rules["inclusion_rules"]["leader"](
            selected_objects
        )
        self.selected_follower_objects = level_rules["inclusion_rules"]["follower"](
            selected_objects
        )

        self.selected_positions = level_rules["position_rules"][0]
        self.selected_follower_object_positions = level_rules["position_rules"][1](
            self.selected_positions
        )

        # print("MATS")
        # print("LEADER -> FOLLOWER")
        # print(self.selected_mats)
        # print(self.selected_mats)

        # print("OBJECTS")
        # print("LEADER -> FOLLOWER")
        # print(self.selected_leader_objects)
        # print(self.selected_follower_objects)

        # print("POSITIONS")
        # print("LEADER -> FOLLOWER")
        # print(self.selected_positions)
        # print(self.selected_follower_object_positions)

    def make_table(self):
        mats = Table.get_empty_slots_list()
        for i, pos in enumerate(self.selected_positions):
            try:
                mats[pos[0]][pos[1]] = self.selected_mats[i]
            except:
                mats[pos[0]][pos[1]] = None

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


if __name__ == "__main__":
    config = {}
    levels = [f"l{i}" for i in range(0, 11)]
    variants = [f"v{j}" for j in range(1, 11)]
    for level in levels:
        print(f"Level {level}")
        config[level] = {}
        for variant in variants:
            print(f"Variant {variant}")
            scene_configurator = SceneConfigurator(level)
            scene_configurator.get_configs()
            current_config = None
            while current_config is None or str(current_config) in str(config):
                if current_config:
                    print("Created duplicate - trying again")
                current_config = scene_configurator.make_table()
            config[level][variant] = current_config

        print("==" * 5)

    # Returns the current local date
    today = date.today()

    with open(f"src/ithor/scene_configs{str(today)}.json", "w") as outfile:
        json.dump(config, outfile)
