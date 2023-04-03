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
        "nlu_examples",
        "naturalness",
        "unnaturalness_examples",
        "helpfulness",
        "unhelpfulness_examples",
        "satisfaction",
        "improvements",
    ],
    usecols=[1, 2, 5, 6, 8, 10, 12],
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

# NLU
questionnaire_quant_merged_nlu_df = (
    questionnaire_quant_merged_df[["bot", "level", "nlu"]]
    .groupby(["bot", "level"], as_index=False)
    .agg({"nlu": ["mean", "std"]})
)
questionnaire_quant_merged_nlu_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_nlu_df.columns
]
print(questionnaire_quant_merged_nlu_df)
plt.figure()
plot7 = sns.barplot(
    data=questionnaire_quant_merged_nlu_df.drop(["nlu_std"], axis=1),
    x="bot",
    y="nlu_mean",
    hue="level",
)
plt.savefig(f"{os.path.abspath('')}/results/nlu.pdf")

questionnaire_quant_merged_nlu_aggr_bot_df = (
    questionnaire_quant_merged_df[["bot", "level", "nlu"]]
    .groupby(["bot"], as_index=False)
    .agg({"nlu": ["mean", "std"]})
)
questionnaire_quant_merged_nlu_aggr_bot_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_nlu_aggr_bot_df.columns
]
print(questionnaire_quant_merged_nlu_aggr_bot_df)
plt.figure()
plot8 = sns.barplot(
    data=questionnaire_quant_merged_nlu_aggr_bot_df.drop(["nlu_std"], axis=1),
    x="bot",
    y="nlu_mean",
)
plt.savefig(f"{os.path.abspath('')}/results/nlu_aggr.pdf")

questionnaire_quant_merged_nlu_aggr_level_df = (
    questionnaire_quant_merged_df[["bot", "level", "nlu"]]
    .groupby(["level"], as_index=False)
    .agg({"nlu": ["mean", "std"]})
)
questionnaire_quant_merged_nlu_aggr_level_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_nlu_aggr_level_df.columns
]
print(questionnaire_quant_merged_nlu_aggr_level_df)

# Naturalness
questionnaire_quant_merged_naturalness_df = (
    questionnaire_quant_merged_df[["bot", "level", "naturalness"]]
    .groupby(["bot", "level"], as_index=False)
    .agg({"naturalness": ["mean", "std"]})
)
questionnaire_quant_merged_naturalness_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_naturalness_df.columns
]
print(questionnaire_quant_merged_naturalness_df)
plt.figure()
plot9 = sns.barplot(
    data=questionnaire_quant_merged_naturalness_df.drop(["naturalness_std"], axis=1),
    x="bot",
    y="naturalness_mean",
    hue="level",
)
plt.savefig(f"{os.path.abspath('')}/results/naturalness.pdf")

questionnaire_quant_merged_naturalness_aggr_bot_df = (
    questionnaire_quant_merged_df[["bot", "level", "naturalness"]]
    .groupby(["bot"], as_index=False)
    .agg({"naturalness": ["mean", "std"]})
)
questionnaire_quant_merged_naturalness_aggr_bot_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_naturalness_aggr_bot_df.columns
]
print(questionnaire_quant_merged_naturalness_aggr_bot_df)
plot10 = sns.barplot(
    data=questionnaire_quant_merged_naturalness_aggr_bot_df.drop(
        ["naturalness_std"], axis=1
    ),
    x="bot",
    y="naturalness_mean",
)
plt.savefig(f"{os.path.abspath('')}/results/naturalness_aggr.pdf")

questionnaire_quant_merged_naturalness_aggr_level_df = (
    questionnaire_quant_merged_df[["bot", "level", "naturalness"]]
    .groupby(["level"], as_index=False)
    .agg({"naturalness": ["mean", "std"]})
)
questionnaire_quant_merged_naturalness_aggr_level_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_naturalness_aggr_level_df.columns
]
print(questionnaire_quant_merged_naturalness_aggr_level_df)


# Helpfulness
questionnaire_quant_merged_helpfulness_df = (
    questionnaire_quant_merged_df[["bot", "level", "helpfulness"]]
    .groupby(["bot", "level"], as_index=False)
    .agg({"helpfulness": ["mean", "std"]})
)
questionnaire_quant_merged_helpfulness_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_helpfulness_df.columns
]
print(questionnaire_quant_merged_helpfulness_df)
plt.figure()
plot11 = sns.barplot(
    data=questionnaire_quant_merged_helpfulness_df.drop(["helpfulness_std"], axis=1),
    x="bot",
    y="helpfulness_mean",
    hue="level",
)
plt.savefig(f"{os.path.abspath('')}/results/helpfulness.pdf")

questionnaire_quant_merged_helpfulness_aggr_bot_df = (
    questionnaire_quant_merged_df[["bot", "level", "helpfulness"]]
    .groupby(["bot"], as_index=False)
    .agg({"helpfulness": ["mean", "std"]})
)
questionnaire_quant_merged_helpfulness_aggr_bot_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_helpfulness_aggr_bot_df.columns
]
print(questionnaire_quant_merged_helpfulness_aggr_bot_df)
plt.figure()
plot12 = sns.barplot(
    data=questionnaire_quant_merged_helpfulness_aggr_bot_df.drop(
        ["helpfulness_std"], axis=1
    ),
    x="bot",
    y="helpfulness_mean",
)
plt.savefig(f"{os.path.abspath('')}/results/helpfulness_aggr.pdf")

questionnaire_quant_merged_helpfulness_aggr_level_df = (
    questionnaire_quant_merged_df[["bot", "level", "helpfulness"]]
    .groupby(["level"], as_index=False)
    .agg({"helpfulness": ["mean", "std"]})
)
questionnaire_quant_merged_helpfulness_aggr_level_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_helpfulness_aggr_level_df.columns
]
print(questionnaire_quant_merged_helpfulness_aggr_level_df)


# Satisfaction
questionnaire_quant_merged_satisfaction_df = (
    questionnaire_quant_merged_df[["bot", "level", "satisfaction"]]
    .groupby(["bot", "level"], as_index=False)
    .agg({"satisfaction": ["mean", "std"]})
)
questionnaire_quant_merged_satisfaction_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_satisfaction_df.columns
]
print(questionnaire_quant_merged_satisfaction_df)
plot13 = sns.barplot(
    data=questionnaire_quant_merged_satisfaction_df.drop(["satisfaction_std"], axis=1),
    x="bot",
    y="satisfaction_mean",
    hue="level",
)
plt.savefig(f"{os.path.abspath('')}/results/satisfaction.pdf")

questionnaire_quant_merged_satisfaction_aggr_bot_df = (
    questionnaire_quant_merged_df[["bot", "level", "satisfaction"]]
    .groupby(["bot"], as_index=False)
    .agg({"satisfaction": ["mean", "std"]})
)
questionnaire_quant_merged_satisfaction_aggr_bot_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_satisfaction_aggr_bot_df.columns
]
print(questionnaire_quant_merged_satisfaction_aggr_bot_df)
plot14 = sns.barplot(
    data=questionnaire_quant_merged_satisfaction_aggr_bot_df.drop(
        ["satisfaction_std"], axis=1
    ),
    x="bot",
    y="satisfaction_mean",
)
plt.savefig(f"{os.path.abspath('')}/results/satisfaction_aggr.pdf")

questionnaire_quant_merged_satisfaction_aggr_level_df = (
    questionnaire_quant_merged_df[["bot", "level", "satisfaction"]]
    .groupby(["level"], as_index=False)
    .agg({"satisfaction": ["mean", "std"]})
)
questionnaire_quant_merged_satisfaction_aggr_level_df.columns = [
    "_".join(col_name).rstrip("_")
    for col_name in questionnaire_quant_merged_satisfaction_aggr_level_df.columns
]
print(questionnaire_quant_merged_satisfaction_aggr_level_df)
