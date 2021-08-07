import logging
import sys
import time

import yaml
from psnawp_api import psnawp

from const import *
from integration import Integration


class PlaystationDiscordStatus:

    def __init__(self):

        # Init logging
        self.log = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)

        # Load config
        with open("config.yml") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        # Config variables
        self.NPSSO_KEY = self.config["NPSSO_KEY"]
        self.PLAYSTATION_ONLINE_ID = self.config["PLAYSTATION_ONLINE_ID"]
        self.CLIENT_APP_ID = self.config["CLIENT_APP_ID"]

        # System (PS4, PS5)
        self.system = None

        # Integration helper
        self.integration = Integration(self)

    def run(self):

        psnawp_client = psnawp.PSNAWP(self.NPSSO_KEY)

        previous_presence = None
        previous_status = None

        while True:

            user_online_id = psnawp_client.user(online_id=self.PLAYSTATION_ONLINE_ID)
            presence = user_online_id.get_presence()

            # Timer to give to Discord
            start_time = int(time.time())

            online_status = presence["primaryPlatformInfo"]["onlineStatus"]
            if online_status == "offline":
                self.integration.clear_presence()
                self.log.info("User is offline.")

            elif presence != previous_presence:

                if online_status != previous_status:

                    # Display correct system in presence
                    platform = presence["primaryPlatformInfo"]["platform"]
                    if platform == "PS5":
                        self.system = "ps5_main"
                    elif platform == "PS4":
                        self.system = "ps4_main"
                    self.integration.connect_presence(self.CLIENT_APP_ID)

                if "gameTitleInfoList" not in presence:

                    # User isn't playing a game
                    self.integration.online_not_ingame(start_time)
                    self.log.info("User is online but not in-game.")

                else:

                    game_info = presence["gameTitleInfoList"][0]
                    self.integration.online_ingame(start_time, game_info)
                    self.log.info(f"User is playing {game_info['titleName']}.")

            time.sleep(15)
            previous_presence = presence
            previous_status = online_status


if __name__ == "__main__":
    psd_status = PlaystationDiscordStatus()
    psd_status.run()
