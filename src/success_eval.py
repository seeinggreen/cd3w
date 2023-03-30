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
    def __init__(self, goal_scene, final_scenes, state_change, variant):
        self.goal_scene = goal_scene
        self.final_scenes = final_scenes
        self.state_change = state_change
        self.expected_changes = 7 if state_change else 6
        self.variant = variant
        self.missing_changes = {}
        self.results = {}
        self.result_type = ""
        self.error_logs = {self.variant: {}}

    def _get_state(self, object):
        state = re.sub("\w*\d+", "", object)  # Discard the name and number
        if state == "":
            return "NotSliced"
        else:
            return state

    def _get_type(self, object):
        return re.sub("\d+\w*", "", object)

    def _log_append(self, info, state_change=False):
        log = ["===" * 10]
        for item in info:
            log.append(item)
        if not info[-1]:
            log.append("final state has nothing in this position")
        else:
            log.append("different name in pos")
        if state_change:
            log.append("missing state change")
        else:
            log.append("missing pos change")
        return log

    def _count_changes(self):
        goal_objects = {}
        final_objects = {}

        for user, final_scene in self.final_scenes.items():
            if user == "E5":
                user == "malek"
            else:
                user = user.lower()
            error_log = []
            missing_pos_changes = 0
            missing_state_changes = 0
            final_objects[user] = {}
            for i, rows in enumerate(self.goal_scene):
                for j, object in enumerate(rows):
                    if object:
                        goal_objects[f"{i}{j}"] = {
                            "name": object,
                            "type": self._get_type(object),
                            "state": self._get_state(object),
                        }
                    if final_scene["objects"][i][j]:
                        final_objects[user][f"{i}{j}"] = {
                            "name": final_scene["objects"][i][j],
                            "type": self._get_type(final_scene["objects"][i][j]),
                            "state": self._get_state(final_scene["objects"][i][j]),
                        }

            for pos, object in goal_objects.items():
                if pos in final_objects[user]:
                    info = [
                        f"{pos[0]}-{pos[1]}",
                        object["name"],
                        final_objects[user][pos]["name"],
                    ]
                    if final_objects[user][pos]["name"] != object["name"]:
                        if self.state_change:
                            if final_objects[user][pos]["type"] != object["type"]:
                                missing_pos_changes += 1
                                error_log.append(self._log_append(info))
                            elif final_objects[user][pos]["state"] != object["state"]:
                                missing_state_changes += 1
                                error_log.append(
                                    self._log_append(info, state_change=True)
                                )
                        else:
                            missing_pos_changes += 1
                            error_log.append(self._log_append(info))
                else:
                    info = [pos, object, ""]
                    missing_pos_changes += 1
                    error_log.append(self._log_append(info))

            self.missing_changes[user] = [missing_pos_changes, missing_state_changes]
            self.error_logs[self.variant][user] = error_log

    @abstractmethod
    def compute_metric(self):
        raise NotImplementedError


class Success(Metric):
    def __init__(self, *args):
        super().__init__(*args)
        self.result_type = "success"

    def compute_metric(self):
        self._count_changes()
        for user, counts in self.missing_changes.items():
            if counts[0] or counts[1]:
                self.results[user] = float(0)
            else:
                self.results[user] = float(1)


class SuccessGC(Metric):
    def __init__(self, *args):
        super().__init__(*args)
        self.result_type = "success_gc"

    def compute_metric(self):
        self._count_changes()
        for user, count in self.missing_changes.items():
            correct_changes = self.expected_changes - sum(count)
            changes_made_relative = correct_changes / self.expected_changes
            self.results[user] = changes_made_relative


class Evaluator:
    def __init__(self, level, variant, result_type, save_bot_first, eval_date):
        self.level = level
        self.state_change = True if self.level == 6 else False
        self.variant = variant
        self.result_type = result_type
        self.experiment_date = eval_date
        self.goal_scene = self._get_goal_scene()
        self.final_scenes = self._get_final_scenes()
        self.save_bot_first = save_bot_first
        self.bot_variant = f"b{BOT_VARIANT_MAPPING[self.variant]}"
        self.results_dir = f"{os.path.abspath('')}/results"

    def _get_goal_scene(self):
        with open("src/ithor/scene_configs.json", encoding="utf-8") as json_file:
            goal_scene = json.load(json_file)[self.level][self.variant]["leader"][
                "objects"
            ]

        return goal_scene

    def _get_final_scenes(self):
        with open(
            f"output/final_states/{self.level}_{self.variant}.json",
            encoding="utf-8",
        ) as json_file:
            final_scenes = json.load(json_file)[self.experiment_date]

        return final_scenes

    def get_results(self):
        if self.result_type == "success":
            metric = Success(
                self.goal_scene, self.final_scenes, self.state_change, self.variant
            )
        else:
            metric = SuccessGC(
                self.goal_scene, self.final_scenes, self.state_change, self.variant
            )
        metric.compute_metric()
        return metric.results, metric.error_logs

    def save(self, data, logs=False):
        if self.save_bot_first or logs:
            level_1 = self.bot_variant
            level_2 = self.level
        else:
            level_1 = self.level
            level_2 = self.bot_variant
        if not os.path.exists(self.results_dir):
            os.mkdir(self.results_dir)
        if logs:
            fn = f"{self.results_dir}/{self.result_type}_logs.json"
        else:
            fn = f"{self.results_dir}/{self.result_type}.json"
        existing_data = {}
        if os.path.exists(fn):
            with open(fn, encoding="utf-8") as json_file:
                existing_data = json.load(json_file)
            if level_1 in existing_data:
                existing_data[level_1][level_2] = data
            else:
                existing_data[level_1] = {level_2: data}
        else:
            existing_data[level_1] = {level_2: data}
        with open(fn, "w+") as outfile:
            json.dump(existing_data, outfile)


if __name__ == "__main__":
    for result_type in ["success", "success_gc"]:
        for fn in os.listdir(f"{os.path.abspath('')}/output/final_states"):
            level, variant = fn.replace(".json", "").split("_")
            if level in ["l1", "l4", "l7"] and variant in [
                f"v{i}" for i in range(5, 11)
            ]:
                print(level)
                print(variant)
                for bot_first_bool in [True, False]:
                    evaluator = Evaluator(
                        level, variant, result_type, bot_first_bool, "2023-03-29"
                    )
                    results, error_logs = evaluator.get_results()
                    evaluator.save(error_logs, logs=True)
                    evaluator.save(results)
