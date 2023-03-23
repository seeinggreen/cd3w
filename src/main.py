import os
import sys

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

from argparsing import get_args
from ithor.ithor_service import IthorService
from rasa_srv.service import RasaService
from slurk.bots.ithorbot.ithor_bot import IthorBot
from slurk.bots.leaderbot.leader_bot import LeaderBot
from tokens import Tokens
from threading import Thread

if __name__ == "__main__":
    args = get_args()
    port = args["port"]

    tokens = Tokens(port)

    ithor_token = tokens.ithor_token
    ithor_user = tokens.ithor_user
    leader_bot_token = tokens.leader_bot_token
    leader_bot_user = tokens.leader_bot_user
    level = args["level"]
    variant = args["variant"]

    ithor_service = IthorService()

    ithor_bot = IthorBot(
        ithor_token,
        ithor_user,
        "http://localhost",
        port,
        ithor_service,
        level,
        variant,
    )

    rasa_service = RasaService(port, level, variant)

    print("running main")
    print(rasa_service.get_scene())

    leader_bot = LeaderBot(
        leader_bot_token,
        leader_bot_user,
        "http://localhost",
        port,
        rasa_service,
        level,
        variant,
    )

    Thread(target=ithor_bot.run).start()
    Thread(target=leader_bot.run).start()
