import sys
import os
from threading import Thread

basepath = os.path.dirname(os.path.dirname(os.path.abspath("")))
if not basepath in sys.path:
    sys.path.append(basepath)

import requests
import json

from ithor.ithor_service import IthorService
from rasa.rasa_service import RasaService
from slurk.bots.ithorbot.ithor_bot import IthorBot
from slurk.bots.leaderbot.leader_bot import LeaderBot

from argparsing import get_args

base_url = "http://localhost"
headers = {
    "Authorization": "Bearer 00000000-0000-0000-0000-000000000000",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

layout_file = "src/slurk/layouts/task_room_layout.json"
ithor_bot_file = "src/slurk/permissions/ithor_bot_permissions.json"
leader_bot_file = "src/slurk/permissions/leader_bot_permissions.json"
human_user_file = "src/slurk/permissions/user_permissions.json"


class MissingInfoError(Exception):
    pass


class Tokens:
    def __init__(self, port):
        self.port = port

        self.get_layout_id()
        self.create_room()
        self.get_ithor_token()
        self.create_ithor_user()
        self.get_leader_bot_token()
        self.create_leader_bot_user()
        self.get_human_user_tokens()

        print(f"{self.user1}\n{self.user2}")

    def get_url(self, sub_url):
        return f"{base_url}:{self.port}/slurk/api/{sub_url}"

    def req(self, url, data):
        return requests.post(url, headers=headers, data=json.dumps(data))

    def get_layout_id(self):
        with open(layout_file) as f:
            layout_data = json.load(f)
        url = self.get_url("layouts")
        r = self.req(url, layout_data)
        self.layout_id = r.json()["id"]

    def create_room(self):
        if not self.layout_id:
            raise MissingInfoError("Layout ID is missing.")
        data = {"layout_id": self.layout_id}
        url = self.get_url("rooms")
        r = self.req(url, data)
        self.room_id = r.json()["id"]

    def get_user_token(self, permission_data):
        if not self.room_id:
            raise MissingInfoError("Room ID is missing.")
        url = self.get_url("permissions")
        r = self.req(url, permission_data)
        permissions_id = r.json()["id"]

        url = self.get_url("tokens")
        data = {"permissions_id": permissions_id, "room_id": self.room_id}
        r = self.req(url, data)
        return r.json()["id"]

    def create_ithor_user(self):
        if not self.ithor_token:
            raise MissingInfoError("IThor token is missing.")
        data = {"name": "IthorBot", "token_id": self.ithor_token}
        url = self.get_url("users")
        r = self.req(url, data)
        self.ithor_user = r.json()["id"]

    def get_ithor_token(self):
        with open(ithor_bot_file) as f:
            permission_data = json.load(f)
        self.ithor_token = self.get_user_token(permission_data)

    def create_leader_bot_user(self):
        if not self.leader_bot_token:
            raise MissingInfoError("LeaderBot token is missing.")
        data = {"name": "LeaderBot", "token_id": self.leader_bot_token}
        url = self.get_url("users")
        r = self.req(url, data)
        self.leader_bot_user = r.json()["id"]

    def get_leader_bot_token(self):
        with open(leader_bot_file) as f:
            permission_data = json.load(f)
        self.leader_bot_token = self.get_user_token(permission_data)

    def get_human_user_tokens(self):
        with open(human_user_file) as f:
            permission_data = json.load(f)
        self.user1 = self.get_user_token(permission_data)
        self.user2 = self.get_user_token(permission_data)


if __name__ == "__main__":
    args = get_args()
    port = args["port"]

    tokens = Tokens(port)

    ithor_token = tokens.ithor_token
    ithor_user = tokens.ithor_user
    # Need to implement this in Tokens class
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

    rasa_service = RasaService()

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
