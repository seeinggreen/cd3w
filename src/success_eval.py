import json
import os
import re
import sys
from abc import ABC, abstractmethod

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from rasa_srv.service import BOT_VARIANT_MAPPING


class Metric(ABC):
    def __init__(self, goal_scene, final_scenes, state_change):
        self.goal_scene = goal_scene
        self.final_scenes = final_scenes
        self.state_change = state_change
        self.expected_changes = 7 if state_change else 6
        self.missing_pos_changes = 0
        self.missing_state_changes = 0
        self.results = []
        self.result_type = ""

    def _get_state(self, object):
        state = re.sub("\w*\d+", "", object)  # Discard the name and number
        if state == "":
            return "NotSliced"
        else:
            return state

    def _get_type(self, object):
        return re.sub("\d+\w*", "", object)

    def _count_changes(self):
        goal_objects = {}
        final_objects = {}

        def rearrange(double_nested_list):
            rearranged_list = []
            for i in range(len(double_nested_list[0])):
                rearranged_list.append([l[i] for l in double_nested_list])
            return rearranged_list

        for final_scene in self.final_scenes.values():
            scenes_zipped = zip(self.goal_scene, final_scene["objects"])
            for i, rows in enumerate(scenes_zipped):
                rows_rearranged = rearrange(rows)
                for j, objects in enumerate(rows_rearranged):
                    if objects[0]:
                        goal_objects[f"{i}{j}"] = {
                            "name": objects[0],
                            "type": self._get_type(objects[0]),
                            "state": self._get_state(objects[0]),
                        }
                    if objects[1]:
                        final_objects[f"{i}{j}"] = {
                            "name": objects[1],
                            "type": self._get_type(objects[1]),
                            "state": self._get_state(objects[1]),
                        }

            for pos, object in goal_objects.items():
                print(pos)
                print(object)
                if pos in final_objects:
                    print("in final")
                    if final_objects[pos]["name"] != object["name"]:
                        print("different name in pos")
                        if self.state_change:
                            if final_objects[pos]["type"] != object["type"]:
                                self.missing_pos_changes += 1
                                print(final_objects[pos])
                                print(object)
                                print(f"missing pos change {self.missing_pos_changes}")
                                print("==" * 10)
                            elif final_objects[pos]["state"] != object["state"]:
                                print(final_objects[pos])
                                print(object)
                                self.missing_state_changes += 1
                                print(
                                    f"missing state change {self.missing_state_changes}"
                                )
                                print("==" * 10)
                        else:
                            print(final_objects[pos])
                            print(object)
                            self.missing_pos_changes += 1
                            print(f"missing state change {self.missing_state_changes}")
                            print("==" * 10)
                else:
                    print("Final state has nothing in this position")
                    print(pos)
                    print(final_objects.keys())
                    self.missing_pos_changes += 1
                    print(f"missing pos change {self.missing_pos_changes}")
                    print("==" * 10)

    @abstractmethod
    def compute_metric(self):
        raise NotImplementedError


class Success(Metric):
    def __init__(self, *args):
        super().__init__(*args)
        self.result_type = "success"

    def compute_metric(self):
        self._count_changes()
        if self.missing_pos_changes or self.missing_state_changes:
            self.results.append(float(0))
        else:
            self.results.append(float(1))


class SuccessGC(Metric):
    def __init__(self, *args):
        super().__init__(*args)
        self.result_type = "success_gc"

    def compute_metric(self):
        self._count_changes()
        correct_changes = self.expected_changes - (
            self.missing_pos_changes + self.missing_state_changes
        )
        changes_made_relative = correct_changes / self.expected_changes
        self.results.append(changes_made_relative)


class Results:
    def __init__(self, level, variant, result_type, save_level_first):
        self.level = level
        self.state_change = True if self.level == 6 else False
        self.variant = variant
        self.result_type = result_type
        self.experiment_date = "2023-03-08"  # change to eval date
        self.goal_scene = self._get_goal_scene()
        self.final_scenes = self._get_final_scenes()
        self.results = self._get_results()
        self.save_level_first = save_level_first
        # self.bot_variant = f"b{BOT_VARIANT_MAPPING["v5"]}"
        self.bot_variant = f"b{BOT_VARIANT_MAPPING['v5']}"  # change to above line
        self.results_dir = f"{os.path.abspath('')}/results"

    def _get_goal_scene(self):
        with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
            goal_scene = json.load(json_file)[self.level][self.variant]["leader"][
                "objects"
            ]

        return goal_scene

    def _get_final_scenes(self):
        with open(
            f"output/train_final_states/{self.level}_{self.variant}.json",
            encoding="utf-8",
        ) as json_file:
            final_scenes = json.load(json_file)[self.experiment_date]

        return final_scenes

    def _get_results(self):
        if self.result_type == "success":
            metric = Success(self.goal_scene, self.final_scenes, self.state_change)
        else:
            metric = SuccessGC(self.goal_scene, self.final_scenes, self.state_change)
        metric.compute_metric()
        return metric.results

    def save(self):
        if self.save_level_first:
            level_1 = self.level
            level_2 = self.bot_variant
        else:
            level_1 = self.bot_variant
            level_2 = self.level
        if not os.path.exists(self.results_dir):
            os.mkdir(self.results_dir)
        results_path = f"{self.results_dir}/{self.result_type}.json"
        if os.path.exists(results_path):
            with open(results_path, encoding="utf-8") as json_file:
                existing_results_data = json.load(json_file)
            if level_1 in existing_results_data:
                if level_2 in existing_results_data[level_1]:
                    existing_results_data[level_1][level_2] = self.results
                else:
                    existing_results_data[level_1].update({level_2: self.results})
            else:
                existing_results_data.update({level_1: {level_2: self.results}})
            with open(results_path, "w+") as outfile:
                json.dump(existing_results_data, outfile)
        else:
            with open(results_path, "w+") as outfile:
                json.dump({level_1: {level_2: self.results}}, outfile)


if __name__ == "__main__":
    # for result_type in ["success", "success_gc", "misplaced", "fixed_strict"]:
    #     for fn in os.listdir(f"{os.path.abspath('')}/output/train_final_states"):
    #         print(fn)
    #         level, variant = fn.replace(".json", "").split("_")
    #         print(level)
    #         print(variant)
    #         try:
    #             results = Results(level, variant, result_type, True)
    #             results.save()
    #         except:
    #             pass
    results = Results("l7", "v3", "success_gc", True)
    results.save()
