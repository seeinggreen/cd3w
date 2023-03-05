import json
import os
import sys

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from argparsing import get_args
from ithor.ithor_service import IthorService
from slurk.bots.ithorbot.ithor_bot import IthorBot

if __name__ == "__main__":
    # Get the experiment arguments from the command line
    args = get_args()
    token = args["token"]
    user = args["user"]
    task = args["task"]
    level = args["level"]
    variant = args["variant"]

    ithor_service = IthorService()

    ithor_bot = IthorBot(
        token, user, "http://localhost", 5000, task, ithor_service, level, variant
    )
    ithor_bot.run()
