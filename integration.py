import time
from pypresence import Presence

system_names = {
    "ps4_main": "PlayStation®4",
    "ps5_main": "PlayStation®5",
}

class Integration:

    def __init__(self, controller):

        # Controller to access vars
        self.controller = controller

        # RPC client
        self.rpc = None

        # Current activity
        self.current_activity = None

        # Start time of activity
        self.start_time = None

    def clear_presence(self):
        if self.rpc:
            self.rpc.clear()
        self.current_activity = None
        self.start_time = None
        self.controller.log.info("User is now offline.")

    def connect_presence(self, app_id):
        if self.rpc:
            self.rpc.clear()
        self.rpc = Presence(app_id, pipe=0)
        self.rpc.connect()

    def online_not_ingame(self):

        if "online" != self.current_activity:
            start_time = int(time.time())
        else:
            start_time = self.start_time

        opts = {
            "state": "Online",
            "start": start_time,
            "large_image": self.controller.system,
            "large_text": "Not in-game"
        }
        self.rpc.update(**opts)
        self.current_activity = "online"
        self.start_time = start_time
        self.controller.log.info("User is online but not in-game.")

    def online_ingame(self, game_info):

        # print(game_info)

        game_id = game_info["npTitleId"]
        
        if game_info.get("npTitleIconUrl"):
            game_image = game_info["npTitleIconUrl"]
        elif game_info.get("conceptIconUrl"):
            game_image = game_info["conceptIconUrl"]

        game_title = game_info.get("titleName")

        game_status = None
        if game_info.get("gameStatus"):
            game_status = game_info['gameStatus']

        if game_id != self.current_activity:
            start_time = int(time.time())
        else:
            start_time = self.start_time

        if game_image:
            large_image = game_image

        opts = {
            "details": game_title,
            "start": start_time,
            "large_image": large_image,
            "large_text": game_title
        }

        # if game_status exists, add it to the presence
        if game_status:
            opts["state"] = game_status

        self.rpc.update(**opts)
        self.current_activity = game_id
        self.start_time = start_time
        self.controller.log.info(f"User is playing {game_title}.")
