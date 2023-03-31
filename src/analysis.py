import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json


basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

bot_results = {}
bot_results_aggr = {}
bot_counts = {}
bot_counts_aggr = {}
for bot in ["b1", "b2", "b3"]:
    with open(
        f"{os.path.abspath('')}/results/success.json", encoding="utf-8"
    ) as json_file:
        results = json.load(json_file)[bot]
        bot_results[bot] = {}
        bot_results_aggr[bot] = []
        bot_counts[bot] = {}
        bot_counts_aggr[bot] = 0
    for level in ["l1", "l4", "l7"]:
        bot_results[bot][level] = np.mean([value for value in results[level].values()])
        bot_results_aggr[bot].extend([value for value in results[level].values()])
        bot_counts_aggr[bot] += len([value for value in results[level].values()])
        if level in bot_counts[bot]:
            bot_counts[bot][level] += len([value for value in results[level].values()])
        else:
            bot_counts[bot][level] = len([value for value in results[level].values()])

bot_results_aggr_means = {
    key: np.mean(value) for key, value in bot_results_aggr.items()
}

print(bot_results)
print(bot_results_aggr_means)
print(bot_counts)
print(bot_counts_aggr)


level_results = {}
level_results_aggr = {}
level_counts = {}
level_counts_aggr = {}
for level in ["l1", "l4", "l7"]:
    with open(
        f"{os.path.abspath('')}/results/success.json", encoding="utf-8"
    ) as json_file:
        results = json.load(json_file)[level]
        level_results[level] = {}
        level_results_aggr[level] = []
        level_counts[level] = {}
        level_counts_aggr[level] = 0
    for bot in ["b1", "b2", "b3"]:
        level_results[level][bot] = np.mean([value for value in results[bot].values()])
        level_results_aggr[level].extend([value for value in results[bot].values()])
        level_counts_aggr[level] += len([value for value in results[bot].values()])
        if bot in level_counts[level]:
            level_counts[level][bot] += len([value for value in results[bot].values()])
        else:
            level_counts[level][bot] = len([value for value in results[bot].values()])


level_results_aggr_means = {
    key: np.mean(value) for key, value in level_results_aggr.items()
}

print(level_results)
print(level_results_aggr_means)
print(level_counts)
print(level_counts_aggr)

user_results = {}
user_counts = {}
with open(f"{os.path.abspath('')}/results/success.json", encoding="utf-8") as json_file:
    results = json.load(json_file)
for level in ["l1", "l4", "l7"]:
    for bot in ["b1", "b2", "b3"]:
        for user in results[level][bot].keys():
            if user in user_results:
                user_results[user] += results[level][bot][user]
                user_counts[user] += 1
            else:
                user_results[user] = results[level][bot][user]
                user_counts[user] = 1

for user in user_results:
    user_results[user] = user_results[user] / user_counts[user]

print(user_results)
print(user_counts)


