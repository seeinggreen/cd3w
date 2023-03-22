import os
import sys
from sqlalchemy.sql.elements import True_

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from argparsing import get_args
from ithor.ithor_service import IthorService
from rasa_srv.service import RasaService
from slurk.bots.ithorbot.ithor_bot import IthorBot
from slurk.bots.leaderbot.leader_bot import LeaderBot

if __name__ == "__main__":
    # Get the experiment arguments from the command line
    args = get_args()
    token = args["token"]
    user = args["user"]
    task = args["task"]
    level = args["level"]
    variant = args["variant"]
    
    port = args["port"]

    ithor_service = IthorService()

    ithor_bot = IthorBot(
        token, user, "http://localhost", port, task, ithor_service, level, variant
    )
    ithor_bot.run()

    rasa_service = RasaService(port, level, variant)

    leader_bot = LeaderBot(
        token, user, "http://localhost", port, task, rasa_service, level, variant
    )
    leader_bot.run()
