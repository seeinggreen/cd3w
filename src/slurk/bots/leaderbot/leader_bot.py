import requests
import socketio


class LeaderBot:
    def __init__(self, token, user, host, port, rasa_service, level, variant):
        self.token = token
        self.user = user
        self.host = host
        self.port = port

        self.rasa_service = rasa_service

        self.level = level
        self.variant = variant

        self.follower = None

        self.sio = socketio.Client(logger=True)

        self.sio.on("new_task_room", self.join_task_room())

        self.register_join_get_scene_handler()
        self.register_command_handler()
        self.register_message_handler()

    def join_task_room(self):
        """Let the bot join an assigned task room."""

        def join(data):
            response = requests.post(
                f"{self.host}:{self.port}/slurk/api/users/{self.user}/rooms/{data['room']}",
                headers={"Authorization": f"Bearer {self.token}"},
            )

        return join

    def register_join_get_scene_handler(self):
        @self.sio.event
        def status(data):
            if data["type"] == "join" and data["user"]["id"] == self.user:
                self.rasa_service.get_scene()

    def register_command_handler(self):
        @self.sio.event
        def command(data):
            if data["user"]["id"] == self.user:
                return

            if data["command"].lower() == "ready":
                if not self.follower:
                    self.follower = data["user"]
                self.sio.emit(
                    "message_command",
                    {
                        "room": data["room"],
                        "command": "ready",
                    },
                )
            elif (
                data["command"].lower() == "done"
                and data["user"]["id"] == self.follower["id"]
            ):
                self.rasa_service.reset()
                self.follower = None

    def register_message_handler(self):
        @self.sio.event
        def text_message(data):
            if not self.follower or data["user"]["id"] != self.follower["id"]:
                return

            leader_message = self.rasa_service.get_response(data["message"])

            self.sio.emit(
                "text",
                {
                    "room": data["room"],
                    "message": leader_message,
                },
            )

    def run(self):
        self.sio.connect(
            f"{self.host}:{self.port}",
            headers={"Authorization": f"Bearer {self.token}", "user": str(self.user)},
            namespaces="/",
        )

        # wait until the connection with the server ends
        self.sio.wait()
