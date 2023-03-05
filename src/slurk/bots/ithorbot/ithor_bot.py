import json
import logging
import os
from datetime import date

import requests
import socketio


class IthorBot:
    def __init__(self, token, user, host, port, task, ithor_service, level, variant):
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

        self.task_id = task
        self.sio.on("new_task_room", self.join_task_room())

        self.register_command_handler()
        self.register_message_handler()

        self.message_log = []

    def join_task_room(self):
        """Let the bot join an assigned task room."""

        def join(data):
            if self.task_id is None or data["task"] != self.task_id:
                return

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
                if "leader" in data["user"]["name"].lower():
                    self.leader = data["user"]
                if "follower" in data["user"]["name"].lower():
                    self.follower = data["user"]
                if self.leader and self.follower:
                    if self.round_in_progress:
                        return

                    self.round_in_progress = True
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "message": f"It's level {self.level.replace('l', '')}. Hold on a sec while I get things set up. This might take a little while...",
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
                            "message": f"Okay, here's the target scene >>>",
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
                            "message": f"Okay, here's the initial scene...",
                        },
                    )
                    self.sio.emit(
                        "image",
                        {
                            "room": data["room"],
                            "receiver_id": self.follower["id"],
                            "url": self.ithor_service.snapshot_scene("follower"),
                            "width": 700,
                            "height": 350,
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
                except Exception as e:
                    self.sio.emit(
                        "text",
                        {
                            "room": data["room"],
                            "receiver_id": data["user"]["id"],
                            "message": f"Oops, that didn't work: {e}",
                        },
                    )
                self.sio.emit(
                    "image",
                    {
                        "room": data["room"],
                        "url": self.ithor_service.snapshot_scene("follower"),
                        "receiver_id": self.follower["id"],
                        "width": 700,
                        "height": 350,
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
