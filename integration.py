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

    def clear_presence(self):
        if self.rpc:
            self.rpc.clear()

    def connect_presence(self, app_id):
        if self.rpc:
            self.rpc.clear()
        self.rpc = Presence(app_id)
        self.rpc.connect()

    def online_not_ingame(self, start_time):
        opts = {
            "state": "Online",
            "start": start_time,
            "small_image": self.controller.system,
            "large_image": self.controller.system,
            "small_text": system_names[self.controller.system],
            "large_text": "Not in-game"
        }
        self.rpc.update(**opts)

    def online_ingame(self, start_time, game_info):

        game_id = game_info["npTitleId"]
        game_title = game_info.get("titleName")
        if game_info.get("gameStatus"):
            game_title += ", " + game_info.get("gameStatus")

        opts = {
            "state": game_title,
            "start": start_time,
            "small_image": self.controller.system,
            "large_image": game_id.lower() if game_id in supported_games else self.controller.system,
            "small_text": system_names[self.controller.system],
            "large_text": game_title
        }
        self.rpc.update(**opts)
