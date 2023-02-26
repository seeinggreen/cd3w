import os
import re
import sys
from itertools import combinations

from ithor.utils.items import Items

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

items = Items()
assets = items.assets


def get_type(asset):
    return re.sub(
        "\d+\w*", "", asset["name"]
    ).lower()  # Discard the number (and state - for objects only)


def get_state(asset):
    state = re.sub("\w*\d+", "", asset["name"]).lower()  # Discard the name and number
    if state == "":
        return "whole"
    else:
        return state


def same_type(asset1, asset2):
    asset1_type = get_type(asset1)
    print("Asset type (1)")
    print(asset1_type)
    asset2_type = get_type(asset2)
    print("Asset type (2)")
    print(asset2_type)
    return asset1_type == asset2_type


def same_state(asset1, asset2):
    asset1_state = get_state(asset1)
    print("Asset state (1)")
    print(asset1_state)
    asset2_state = get_state(asset2)
    print("Asset state (2)")
    print(asset2_state)
    return asset1_state == asset2_state


# Mats
# mats = [asset for asset in assets if items.is_mat(asset["name"])]
# colours = {mat["colour"] for mat in mats}
# mats_by_colour = {}
# same_colour_same_type = []
# same_colour_different_type = []
# temp_similar_colour_same_type = []
# for colour in colours:
#     mats_by_colour[colour] = [mat for mat in mats if mat["colour"] == colour]
#     combos = list(combinations(mats_by_colour[colour], 2))
#     # Check if colour is one of the purple colours
#     if len(combos) == 1:
#         for mat in mats_by_colour[colour]:
#             temp_similar_colour_same_type.append(mat)
#     counter = 0
#     for i, combo in enumerate(combos):
#         if same_type(combo[0], combo[1]):
#             same_colour_same_type.append(combo)
#         else:
#             if counter == 0:
#                 same_colour_different_type.append(combo)
#                 counter += 1

# similar_colour_same_type = [
#     combo
#     for combo in combinations(temp_similar_colour_same_type, 2)
#     if same_type(combo[0], combo[1])
# ]


# Mats
objs = [asset for asset in assets if items.is_object(asset["name"])]
types = {get_type(obj) for obj in objs}
objs_by_type = {}
same_colour_different_state = []
same_type_different_colour = []
same_type_different_colour_state = []
for type in types:
    objs_by_type[type] = [obj for obj in objs if get_type(obj) == type]
    print(f"{type}s")
    combos = list(combinations(objs_by_type[type], 2))
    for i, combo in enumerate(combos):
        print(f"Combination {i}")
        if combo[0]["colour"] == combo[1]["colour"]:
            print("Same colour different state")
            print((combo[0]["name"], combo[1]["name"]))
            print((combo[0]["colour"], combo[1]["colour"]))
            same_colour_different_state.append(combo)
        else:
            if same_state(combo[0], combo[1]):
                same_type_different_colour.append(combo)
                print("Same type different colour")
                print((combo[0]["name"], combo[1]["name"]))
                print((combo[0]["colour"], combo[1]["colour"]))
            else:
                same_type_different_colour_state.append(combo)
                print("Same type different colour + state")
                print((combo[0]["name"], combo[1]["name"]))
                print((combo[0]["colour"], combo[1]["colour"]))

print("==" * 10)

print("Same colour different state")
print([(tup[0]["name"], tup[1]["name"]) for tup in same_colour_different_state])
print("Same type different colour")
print([(tup[0]["name"], tup[1]["name"]) for tup in same_type_different_colour])
print("Same type different colour + state")
print([(tup[0]["name"], tup[1]["name"]) for tup in same_type_different_colour_state])


# # n_mat = 6 # There will always be 6 mats
# # selected_mats = []

# # for i in range(n-m)
# #     get_unique_random(assets, selected):
# #         colours = set([asset.colour for asset in selected])
# #         possible_asset = [asset for asset in assets if asset.colour not in colours]
# #         random_idx = ...
# #         select.append(possible_assets[random_idx])
