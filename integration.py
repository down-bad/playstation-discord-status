import time

from pypresence import Presence

supported_games = [
    "CUSA08519_00",
]

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
        self.controller.log.info("User is now offline.")

    def connect_presence(self, app_id):
        if self.rpc:
            self.rpc.clear()
        self.rpc = Presence(app_id)
        self.rpc.connect()

    def online_not_ingame(self):

        if "online" != self.current_activity:
            start_time = int(time.time())
        else:
            start_time = self.start_time

        opts = {
            "state": "Online",
            "start": start_time,
            "small_image": self.controller.system,
            "large_image": self.controller.system,
            "small_text": system_names[self.controller.system],
            "large_text": "Not in-game"
        }
        self.rpc.update(**opts)
        self.current_activity = "online"
        self.start_time = start_time
        self.controller.log.info("User is online but not in-game.")

    def online_ingame(self, game_info):

        game_id = game_info["npTitleId"]
        game_title = game_info.get("titleName")
        if game_info.get("gameStatus"):
            game_title = f"{game_title}: {game_info['gameStatus']}"

        if game_id != self.current_activity:
            start_time = int(time.time())
        else:
            start_time = self.start_time

        if game_id in supported_games:
            large_image = game_id.lower()
        else:
            large_image = self.controller.system
            self.controller.log.debug(f"Unsupported game, game icon can be added from: {game_info['npTitleIconUrl']}")

        opts = {
            "state": game_title,
            "start": start_time,
            "small_image": self.controller.system,
            "large_image": large_image,
            "small_text": system_names[self.controller.system],
            "large_text": game_title
        }
        self.rpc.update(**opts)
        self.current_activity = game_id
        self.start_time = start_time
        self.controller.log.info(f"User is playing {game_title}.")
