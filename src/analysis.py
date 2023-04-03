import csv
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

# user_results = {}
# user_counts = {}
# all_results = {}
# all_results_aggr = {}
# all_results_aggr_means = {}
# all_counts = {}
# all_counts_aggr = {}
# for metric in ["success", "success_gc"]:
#     with open(
#         f"{os.path.abspath('')}/results/{metric}.json", encoding="utf-8"
#     ) as json_file:
#         results = json.load(json_file)
#     user_results[metric] = {}
#     user_counts[metric] = {}
#     all_results[metric] = {}
#     all_results_aggr[metric] = {}
#     all_results_aggr_means[metric] = {}
#     all_counts[metric] = {}
#     all_counts_aggr[metric] = {}
#     for level_0 in results:
#         if "b" in level_0:
#             type = "bots"
#         else:
#             type = "levels"
#         if type in all_results[metric]:
#             all_results[metric][type].update({level_0: {}})
#             all_results_aggr[metric][type].update({level_0: []})
#             all_counts[metric][type].update({level_0: {}})
#             all_counts_aggr[metric][type].update({level_0: 0})
#         else:
#             all_results[metric][type] = {level_0: {}}
#             all_results_aggr[metric][type] = {level_0: []}
#             all_counts[metric][type] = {level_0: {}}
#             all_counts_aggr[metric][type] = {level_0: 0}
#         for level_1 in results[level_0]:
#             if "b" in level_0:
#                 for user in results[level_0][level_1]:
#                     if user in user_results[metric]:
#                         user_results[metric][user] += results[level_0][level_1][user]
#                         user_counts[metric][user] += 1
#                     else:
#                         user_results[metric][user] = results[level_0][level_1][user]
#                         user_counts[metric][user] = 1
#             all_results[metric][type][level_0][level_1] = np.mean(
#                 [value for value in results[level_0][level_1].values()]
#             )
#             all_results_aggr[metric][type][level_0].extend(
#                 [value for value in results[level_0][level_1].values()]
#             )
#             all_counts_aggr[metric][type][level_0] += len(
#                 [value for value in results[level_0][level_1].values()]
#             )
#             if level_1 in all_counts[metric][type][level_0]:
#                 all_counts[metric][type][level_0][level_1] += len(
#                     [value for value in results[level_0][level_1].values()]
#                 )
#             else:
#                 all_counts[metric][type][level_0][level_1] = len(
#                     [value for value in results[level_0][level_1].values()]
#                 )
#         all_results_aggr_means[metric][type] = {
#             key: np.mean(value) for key, value in all_results_aggr[metric][type].items()
#         }
#     for user in user_results[metric]:
#         user_results[metric][user] = (
#             user_results[metric][user] / user_counts[metric][user]
#         )

# user_to_id = {
#     "adam": "A",
#     "bart": "B",
#     "ben": "D",
#     "laurent": "C",
#     "malek": "E",
#     "mike": "F",
#     "peter": "G",
#     "rishav": "H",
# }

# for metric, types in all_results.items():
#     metric_col = (
#         f"average {'goal-conditioned succcess' if 'gc' in metric else 'binary success'}"
#     )
#     df_users = (
#         pd.DataFrame.from_dict(user_results[metric], orient="index")
#         .reset_index()
#         .rename(
#             columns={
#                 "index": "userID",
#                 0: metric_col,
#             }
#         )
#         .sort_values(by=["userID"])
#         .replace(user_to_id)
#     )
#     plt.figure()
#     plot1 = sns.barplot(
#         data=df_users,
#         x="userID",
#         y=metric_col,
#     )
#     plt.savefig(f"{os.path.abspath('')}/results/{metric}_users.pdf")

#     df_user_counts = (
#         pd.DataFrame.from_dict(user_counts[metric], orient="index")
#         .reset_index()
#         .rename(
#             columns={
#                 "index": "userID",
#                 0: "experiment count",
#             }
#         )
#         .sort_values(by=["userID"])
#         # .replace(user_to_id)
#     )
#     plt.figure()
#     plot2 = sns.barplot(data=df_user_counts, x="userID", y="experiment count")
#     plt.savefig(f"{os.path.abspath('')}/results/counts_users.pdf")

#     for level_0 in types:
#         if level_0 == "bots":
#             level_1 = "levels"
#         else:
#             level_1 = "bots"
#         df_results = (
#             pd.DataFrame.from_dict(all_results[metric][level_0], orient="index")
#             .stack()
#             .reset_index(name=metric_col)
#             .rename(columns={"level_0": level_0, "level_1": level_1})
#             .sort_values(by=[level_0, level_1])
#         )
#         plt.figure()
#         plot3 = sns.barplot(
#             data=df_results,
#             x=level_0,
#             y=metric_col,
#             hue=level_1,
#         )
#         plt.savefig(f"{os.path.abspath('')}/results/{metric}_{type}.pdf")

#         df_results_aggr_means = (
#             pd.DataFrame.from_dict(
#                 all_results_aggr_means[metric][level_0], orient="index"
#             )
#             .reset_index()
#             .rename(
#                 columns={
#                     "index": level_0,
#                     0: metric_col,
#                 }
#             )
#             .sort_values(by=[level_0])
#         )
#         plt.figure()
#         plot4 = sns.barplot(
#             data=df_results_aggr_means,
#             x=level_0,
#             y=metric_col,
#         )
#         plt.savefig(f"{os.path.abspath('')}/results/{metric}_{type}_aggr.pdf")

#         df_counts = (
#             pd.DataFrame.from_dict(all_counts[metric][level_0], orient="index")
#             .stack()
#             .reset_index(name="experiment count")
#             .rename(columns={"level_0": level_0, "level_1": level_1})
#             .sort_values(by=[level_0, level_1])
#         )
#         plt.figure()
#         plot5 = sns.barplot(
#             data=df_counts, x=level_0, y="experiment count", hue=level_1
#         )
#         plt.savefig(f"{os.path.abspath('')}/results/counts.pdf")

#         df_counts_aggr = (
#             pd.DataFrame.from_dict(
#                 all_counts_aggr[metric][level_0],
#                 orient="index",
#                 columns=["experiment count"],
#             )
#             .reset_index()
#             .rename(columns={"index": level_0})
#             .sort_values(by=[level_0])
#         )
#         plt.figure()
#         plot6 = sns.barplot(data=df_counts_aggr, x=level_0, y="experiment count")
#         plt.savefig(f"{os.path.abspath('')}/results/counts_aggr.pdf")

experiment_schedule_df = (
    pd.read_csv(
        f"{os.path.abspath('')}/experiment_schedule.csv",
        names=["gameID", "level", "variant"],
    )
    .drop([0], axis=0)
    .set_index("gameID")
)

questionnaire_quant_df = pd.read_csv(
    f"{os.path.abspath('')}/output/questionnaire.csv",
    names=[
        "questID",
        "start",
        "finish",
        "email",
        "name",
        "gameID",
        "nlu",
        "not_understood_examples",
        "naturalness",
        "unnaturalness_examples",
        "helpfulness",
        "unhelpfulness_examples",
        "satisfaction",
        "improvements",
    ],
    usecols=[1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13],
).drop([0], axis=0)

questionnaire_quant_df = questionnaire_quant_df.astype(
    {
        "nlu": np.int32,
        "naturalness": np.int32,
        "helpfulness": np.int32,
        "satisfaction": np.int32,
    }
)

questionnaire_quant_df["userID"] = questionnaire_quant_df["gameID"].apply(
    lambda x: list(x)[0]
)

questionnaire_quant_df["start"] = pd.to_datetime(questionnaire_quant_df["start"])
questionnaire_quant_df["finish"] = pd.to_datetime(questionnaire_quant_df["finish"])
questionnaire_quant_df["duration"] = (
    questionnaire_quant_df["finish"] - questionnaire_quant_df["start"]
).astype("timedelta64[s]")

questionnaire_quant_merged_df = questionnaire_quant_df.set_index("gameID").join(
    experiment_schedule_df, on="gameID", how="inner"
)

questionnaire_quant_merged_df["bot"] = questionnaire_quant_merged_df["variant"].apply(
    lambda x: "b1" if x in ["5", "6"] else ("b2" if x in ["7", "8"] else "b3")
)


def aggr_multi_col(df):
    df.columns = ["_".join(col_name).rstrip("_") for col_name in df.columns]
    return df


def make_stats_df(df, metric, agg, bot):
    df_cols = ["bot", "level", metric]
    if agg:
        if bot:
            groupby_cols = ["bot"]
        else:
            groupby_cols = ["level"]
    else:
        groupby_cols = ["bot", "level"]
    stats_df = (
        df[df_cols].groupby(groupby_cols, as_index=False).agg({metric: ["mean", "std"]})
    )
    return aggr_multi_col(stats_df)


def plot_results(df, metric, agg, bot):
    if agg:
        x = "bot"
        hue = None
    else:
        if bot:
            x = "bot"
            hue = "level"
        else:
            x = "level"
            hue = "bot"

    plt.figure()
    plot = sns.barplot(
        data=df.drop([f"{metric}_std"], axis=1), x=x, y=f"{metric}_mean", hue=hue
    )
    plt.savefig(f"{os.path.abspath('')}/results/{metric}{'_aggr' if agg else ''}.pdf")


for metric in ["nlu", "naturalness", "helpfulness", "satisfaction", "duration"]:
    for agg in [True, False]:
        if agg:
            for bot in [True, False]:
                stats_df = make_stats_df(
                    questionnaire_quant_merged_df, metric, agg, bot
                )
                if bot:
                    plot_results(stats_df, metric, agg, bot)
                print(stats_df)
        else:
            stats_df = make_stats_df(questionnaire_quant_merged_df, metric, agg, bot)
            plot_results(stats_df, metric, agg, bot)
            print(stats_df)


def make_filtered_grouped_df(df, category):
    return df[["bot", category]].groupby(by="bot").apply(lambda x: x[category]).dropna()


def save_json(df, category):
    df.to_json(f"{os.path.abspath('')}/results/{category}.json")


for category in [
    "not_understood_examples",
    "unnaturalness_examples",
    "unhelpfulness_examples",
    "improvements",
]:
    grouped_df = make_filtered_grouped_df(questionnaire_quant_merged_df, category)
    save_json(grouped_df, category)
