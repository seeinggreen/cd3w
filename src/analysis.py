import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import json


basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

user_results = {}
user_counts = {}
all_results = {}
all_results_aggr = {}
all_results_aggr_means = {}
all_counts = {}
all_counts_aggr = {}
for metric in ["success", "success_gc"]:
    with open(
        f"{os.path.abspath('')}/results/{metric}.json", encoding="utf-8"
    ) as json_file:
        results = json.load(json_file)
    user_results[metric] = {}
    user_counts[metric] = {}
    all_results[metric] = {}
    all_results_aggr[metric] = {}
    all_results_aggr_means[metric] = {}
    all_counts[metric] = {}
    all_counts_aggr[metric] = {}
    for level_0 in results:
        if "b" in level_0:
            type = "bots"
        else:
            type = "levels"
        if type in all_results[metric]:
            all_results[metric][type].update({level_0: {}})
            all_results_aggr[metric][type].update({level_0: []})
            all_counts[metric][type].update({level_0: {}})
            all_counts_aggr[metric][type].update({level_0: 0})
        else:
            all_results[metric][type] = {level_0: {}}
            all_results_aggr[metric][type] = {level_0: []}
            all_counts[metric][type] = {level_0: {}}
            all_counts_aggr[metric][type] = {level_0: 0}
        for level_1 in results[level_0]:
            for user in results[level_0][level_1]:
                if user in user_results[metric]:
                    user_results[metric][user] += results[level_0][level_1][user]
                    user_counts[metric][user] += 1
                else:
                    user_results[metric][user] = results[level_0][level_1][user]
                    user_counts[metric][user] = 1
            all_results[metric][type][level_0][level_1] = np.mean(
                [value for value in results[level_0][level_1].values()]
            )
            all_results_aggr[metric][type][level_0].extend(
                [value for value in results[level_0][level_1].values()]
            )
            all_counts_aggr[metric][type][level_0] += len(
                [value for value in results[level_0][level_1].values()]
            )
            if level_1 in all_counts[metric][type][level_0]:
                all_counts[metric][type][level_0][level_1] += len(
                    [value for value in results[level_0][level_1].values()]
                )
            else:
                all_counts[metric][type][level_0][level_1] = len(
                    [value for value in results[level_0][level_1].values()]
                )
        all_results_aggr_means[metric][type] = {
            key: np.mean(value) for key, value in all_results_aggr[metric][type].items()
        }
    for user in user_results[metric]:
        user_results[metric][user] = (
            user_results[metric][user] / user_counts[metric][user]
        )

user_to_id = dict(
    zip(
        sorted(user_results["success"].keys()),
        np.arange(0, len(user_results["success"].keys())),
    )
)

for metric, types in all_results.items():
    metric_col = (
        f"average {'goal-conditioned succcess' if 'gc' in metric else 'binary success'}"
    )
    df_users = (
        pd.DataFrame.from_dict(user_results[metric], orient="index")
        .reset_index()
        .rename(
            columns={
                "index": "userID",
                0: metric_col,
            }
        )
        .sort_values(by=["userID"])
        .replace(user_to_id)
    )
    plt.figure()
    plot1 = sns.barplot(
        data=df_users,
        x="userID",
        y=metric_col,
    )
    plt.savefig(f"{os.path.abspath('')}/results/{metric}_users.pdf")

    df_user_counts = (
        pd.DataFrame.from_dict(user_counts[metric], orient="index")
        .reset_index()
        .rename(
            columns={
                "index": "userID",
                0: "experiment count",
            }
        )
        .sort_values(by=["userID"])
        .replace(user_to_id)
    )
    plt.figure()
    plot2 = sns.barplot(data=df_user_counts, x="userID", y="experiment count")
    plt.savefig(f"{os.path.abspath('')}/results/counts_users.pdf")

    for level_0 in types:
        if level_0 == "bots":
            level_1 = "levels"
        else:
            level_1 = "bots"
        df_results = (
            pd.DataFrame.from_dict(all_results[metric][level_0], orient="index")
            .stack()
            .reset_index(name=metric_col)
            .rename(columns={"level_0": level_0, "level_1": level_1})
            .sort_values(by=[level_0, level_1])
        )
        plt.figure()
        plot3 = sns.barplot(
            data=df_results,
            x=level_0,
            y=metric_col,
            hue=level_1,
        )
        plt.savefig(f"{os.path.abspath('')}/results/{metric}_{type}.pdf")

        df_results_aggr_means = (
            pd.DataFrame.from_dict(
                all_results_aggr_means[metric][level_0], orient="index"
            )
            .reset_index()
            .rename(
                columns={
                    "index": level_0,
                    0: metric_col,
                }
            )
            .sort_values(by=[level_0])
        )
        plt.figure()
        plot4 = sns.barplot(
            data=df_results_aggr_means,
            x=level_0,
            y=metric_col,
        )
        plt.savefig(f"{os.path.abspath('')}/results/{metric}_{type}_aggr.pdf")

        df_counts = (
            pd.DataFrame.from_dict(all_counts[metric][level_0], orient="index")
            .stack()
            .reset_index(name="experiment count")
            .rename(columns={"level_0": level_0, "level_1": level_1})
            .sort_values(by=[level_0, level_1])
        )
        plt.figure()
        plot5 = sns.barplot(
            data=df_counts, x=level_0, y="experiment count", hue=level_1
        )
        plt.savefig(f"{os.path.abspath('')}/results/counts.pdf")

        df_counts_aggr = (
            pd.DataFrame.from_dict(
                all_counts_aggr[metric][level_0],
                orient="index",
                columns=["experiment count"],
            )
            .reset_index()
            .rename(columns={"index": level_0})
            .sort_values(by=[level_0])
        )
        plt.figure()
        plot6 = sns.barplot(data=df_counts_aggr, x=level_0, y="experiment count")
        plt.savefig(f"{os.path.abspath('')}/results/counts_aggr.pdf")
