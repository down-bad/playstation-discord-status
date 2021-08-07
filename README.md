# playstation-discord-status

Displays your current activity on your PlayStation®4 or PlayStation®5 as a Discord rich presence.

![screenshot image](https://raw.githubusercontent.com/voidel/playstation-discord-status/main/screenshots/screenshot_01.png)

## Getting started

1. Sign in to your PlayStation account at [https://www.playstation.com/](https://www.playstation.com/).
2. After signing in, navigate
   to [https://ca.account.sony.com/api/v1/ssocookie](https://ca.account.sony.com/api/v1/ssocookie).
3. Copy the 64-character key (not the whole cookie displayed) and enter that in config.yml as the NPSSO_KEY.
    ```yaml
    NPSSO_KEY: H5MYhQKS3UwcHm6HQmWzYjwCm7bjgarfWPglQ9Zz7XdzTZ0FLFNsPUvxOnRPRlab
    ```
   Note: this isn't a valid NPSSO_KEY, this is just an example. Don't share your key with anyone.
4. Enter your PlayStation Online ID as PLAYSTATION_ONLINE_ID. This is your unique PlayStation username, not your email or
   your real name.
   ```yaml
   PLAYSTATION_ONLINE_ID: CookieMonster
   ```
5. Run the `main.py` file.
   ```commandline
   python main.py
   ```

## Third-party libraries used

* [PSNAWP](https://github.com/isFakeAccount/psnawp) - PlayStation Network API Wrapper in Python
* [pypresence](https://github.com/qwertyquerty/pypresence) - Discord IPC and Rich Presence wrapper library in Python

## Development notes

* You can replace the Discord Application Client ID if you want to build your own with your own game images.
    * Navigate [here](https://discord.com/developers/applications) to set up your own, replacing the App ID in the
      config.

## Limitations

* My original goal was to containerise this and run it 24/7 on a remote server. Unfortunately you can only update rich
  presence for a Discord user account using RPC on the local machine.
* Most game icons are unsupported, unless they are added to the Discord App Client.
* PSNAWP doesn't support game session time, it won't know for how long you were playing the game prior to starting the
  program.
* Untested on Linux, but there's nothing platform-specific in the code and the third party libraries support Linux.
