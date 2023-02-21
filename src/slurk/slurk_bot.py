# SEE https://github.com/clp-research/slurk-bots FOR STRUCTURE OF SLURK BOTS
# THIS IS A SKELETON WITH THE USE CASE SPECIF FUNCTIONALITY MAPPED OUT
# IT'S LIKELY STILL INCOMPLETE (e.g., CREATING SEPARATE ROOMS FOR LEADER AND FOLLOWER)
class SlurkBot:
    def __init__(self, token, user, host, port, ithor_manager):
        self.token = token # THIS WILL COME FROM THE OUTPUT OF slurk_startup.sh
        self.user = user # ??? NOT SURE HOW THIS WORKS
        self.host = host # SHOULD BE 'http://localhost'
        self.port = port # SHOULD BE 5000
        
        self.ithor_manager = ithor_manager # WILL BE IMPORTED FROM ithor.py IN main.py

        self.register_callbacks()

    def run(self):
        self.sio.connect(
            self.host + ':' + self.port,
            headers={"Authorization": f"Bearer {self.token}", "user": str(self.user)},
            namespaces="/",
        )

        self._send_initial_scene_images()

        # wait until the connection with the server ends
        self.sio.wait()

    def register_callbacks(self):
        # FOR BELOW SEE SLURK DOCUMENTATION 7.3.1
        # REGISTERS text_message HANDLER 
        @self.sio.event
        def text_message(data):
            command = self._parse_message(data.message) # SEE PLACEHOLDER METHOD BELOW (STILL MISSING FUNCTIONALITY)
            if command:
                self.ithor_manager.update_ithor_scene(command)
                follower_image_url = self.ithor_manager.snapshot_scene("follower")
                # FOR BELOW SEE SLURK DOCUMENTATION 7.3.2
                self.sio.emit(
                    "image",
                    {
                        "url": follower_image_url,
                        "room": 2, # ID OF FOLLOWER ROOM
                        # ADD ANY ADDITIONAL KEY-VALUE PAIRS FOR THIS HERE
                    }
                )
    
    def _send_initial_scene_images(self):
        leader_image_url = self.ithor_manager.snapshot_scene("leader")
        # FOR BELOW SEE SLURK DOCUMENTATION 7.3.2
        # FOR LEADER'S ROOM
        self.sio.emit(
            "image",
            {
                "url": leader_image_url,
                "room": 1, # ID OF LEADER ROOM
                # ADD ANY ADDITIONAL KEY-VALUE PAIRS FOR THIS HERE
            }
        )
        # FOR FOLLOWER'S ROOM
        follower_image_url = self.ithor_manager.snapshot_scene("follower")
        self.sio.emit(
            "image",
            {
                "url": follower_image_url,
                "room": 2, # ID OF LEADER ROOM
                # # ADD ANY ADDITIONAL KEY-VALUE PAIRS FOR THIS HERE
            }
        )
    
    def _parse_message(self, data.message):
        command = None # UPDATE THIS TO RETURN THE USER COMMAND IF PATTERN "/\.*" (OR SIMILAR), ELSE RETURN None
        return command