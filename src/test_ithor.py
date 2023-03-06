import os
import sys

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from ithor.ithor_service import IthorService


ithor_service = IthorService()
ithor_service.initialise_scenes("t", "t")

url = ithor_service.snapshot_scene("follower")

commands = [
    "\\discard #6",
    "\\slice #12",
    "\\request #16",
    "\\put #22 on #V",
    "\\put #22 on #table",
    "\\done",
]

for c in commands:
    ithor_service.update_follower_ithor_scene(c)
    if "done" in c:
        continue
    ithor_service.snapshot_scene("follower")
    print("-" * 10)
print("*" * 20)
