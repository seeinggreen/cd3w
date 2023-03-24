import json
import os
from datetime import date

import requests
import socketio


class IthorBot:
    def __init__(self, token, user, host, port, ithor_service, level, variant):
        self.token = token
        self.user = user
        self.host = host
        self.port = port

        self.ithor_service = ithor_service

        self.level = level
        self.variant = variant

        self.leader = None
        self.follower = None
        self.round_in_progress = False

        self.sio = socketio.Client(logger=True)

        self.sio.on("new_task_room", self.join_task_room())

        self.register_user_welcome_handler()
        self.register_command_handler()
        self.register_message_handler()

        self.message_log = []

    def join_task_room(self):
        """Let the bot join an assigned task room."""

        def join(data):
            response = requests.post(
                f"{self.host}:{self.port}/slurk/api/users/{self.user}/rooms/{data['room']}",
                headers={"Authorization": f"Bearer {self.token}"},
            )

        return join

    def run(self):
        self.sio.connect(
            f"{self.host}:{self.port}",
            headers={"Authorization": f"Bearer {self.token}", "user": str(self.user)},
            namespaces="/",
        )

        # wait until the connection with the server ends
        self.sio.wait()

    def register_user_welcome_handler(self):
        @self.sio.event
        def status(data):
            if data["type"] == "join":
                self.sio.emit(
                    "text",
                    {
                        "message": f"### Hello and welcome! "
                        "Are you ready to play The Imitation Game? "
                        "To win the game, a leader and a follwer need to collaborate with one another for the follower to recreate the leader's scene. "
                        f"You are the follower."
                        "Neither of you can see what the other's scene looks like, so to achieve this, you'll have to talk talk talk... "
                        "You can assume that your tables have the same placemats, in the same positions. "
                        "However, the objects you can see may be different, and they're most likely in different positions on the table.",
                        "receiver_id": data["user"]["id"],
                        "room": data["room"],
                    },
                )
                self.sio.emit(
                    "text",
                    {
                        "message": "READY???? Then type /ready to start the game",
                        "receiver_id": data["user"]["id"],
                        "room": data["room"],
                    },
                )

    def register_command_handler(self):
        @self.sio.event
        def command(data):
            if data["user"]["id"] == self.user:
                return

            if self.round_in_progress:
                self.message_log.append(
                    {"user": data["user"]["name"], "command": data["command"]}
                )
            if data["command"].lower() == "ready":
                if not self.follower:
                    self.follower = data["user"]
                elif not self.leader:
                    self.leader = data["user"]
                if self.leader and self.follower:
                    if self.round_in_progress:
                        return

                    self.round_in_progress = True
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "message": f"We're playing level {self.level.replace('l', '')}. Hold on a sec while I get things set up. This might take a little while...",
                        },
                    )

                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "receiver_id": self.follower["id"],
                            "message": "Meanwhile, here are the rules: "
                            "1. You can type messages to your chat partner, "
                            "2. You can type one of the following commands to change your table: "
                            "/put -> for putting objects on mats, "
                            "/request -> for requesting objects you don't currently have, "
                            "/discard -> for throwing away objects you don't need, "
                            "/slice -> for slicing an object, "
                            "/done ->  at the end of the game, if you think you have successfully recreated your chat partner's table. "
                            "You can specify mats and objects using the lookup sheet (e.g., in the format /put #2 on #V, /request #2, /slice #2). "
                            "If you want to put something on the table, use #table (e.g., /put #2 on #table).",
                        },
                    )

                    self.ithor_service.initialise_scenes(
                        level=self.level, variant=self.variant
                    )

                    requests.patch(
                        f"{self.host}:{self.port}/slurk/api/rooms/{data['room']}/attribute/id/current-image",
                        headers={"Authorization": f"Bearer {self.token}"},
                        json={
                            "receiver_id": self.leader["id"],
                            "value": self.ithor_service.snapshot_scene("leader"),
                            "attribute": "src",
                        },
                    )
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "receiver_id": self.leader["id"],
                            "message": f"Okay, here's what your table looks like >>>",
                        },
                    )
                    self.ithor_service.leader_controller.stop()  # We only need this for the initial snapshop

                    requests.patch(
                        f"{self.host}:{self.port}/slurk/api/rooms/{data['room']}/attribute/id/current-image",
                        headers={"Authorization": f"Bearer {self.token}"},
                        json={
                            "receiver_id": self.follower["id"],
                            "value": self.ithor_service.get_follower_lookup_sheet(),
                            "attribute": "src",
                        },
                    )
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "receiver_id": self.follower["id"],
                            "message": f"Okay, here's what your table looks like...",
                        },
                    )
                    self.sio.emit(
                        "image",
                        {
                            "room": data["room"],
                            "receiver_id": self.follower["id"],
                            "url": self.ithor_service.snapshot_scene("follower"),
                            "width": 525,
                            "height": 296,
                        },
                    )
                return
            elif (
                data["command"].lower() == "done"
                and data["user"]["id"] == self.follower["id"]
            ):
                self.ithor_service.follower_controller.save_table_state(
                    self.level, self.variant
                )
                with open(
                    f"{os.path.abspath('')}/output/dialogues/{self.level}_{self.variant}.json",
                    "w+",
                ) as outfile:
                    json.dump({str(date.today()): self.message_log}, outfile)
                self.message_log = []
                self.ithor_service.follower_controller.stop()
                self.leader = None
                self.follower = None
                self.round_in_progress = False
                self.sio.emit(
                    "text",
                    {"room": data["room"], "message": "Thanks for playing!"},
                )
            elif data["user"]["id"] == self.follower["id"]:
                try:
                    self.ithor_service.update_follower_ithor_scene(
                        f"\\\\{data['command']}"
                    )

                    self.sio.emit(
                        "image",
                        {
                            "room": data["room"],
                            "url": self.ithor_service.snapshot_scene("follower"),
                            "receiver_id": self.follower["id"],
                            "width": 525,
                            "height": 296,
                        },
                    )
                except Exception as e:
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "receiver_id": data["user"]["id"],
                            "message": f"Oops, that didn't work: {e}",
                        },
                    )

    def register_message_handler(self):
        @self.sio.event
        def text_message(data):
            if data["user"]["id"] == self.user:
                return

            if self.round_in_progress:
                self.message_log.append(
                    {"user": data["user"]["name"], "message": data["message"]}
                )
