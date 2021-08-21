# FriendsCord
A Discord bot helping you to see what your friends are playing!

# Installation
1. Install all the requirements listed in `requirements.txt` using `pip install -r requirements.txt`.
2. Set up a bot application at the Discord developer and create a bot account. Copy the token and invite the bot to a guild/server by opening the `oAuth2`-tab and selecting the `bot` checkbot in the middle of the `scopes` field, generating a URL (`Copy`) and finally opening it. Finally, activate all intents by turning both the switches in the `Bot` tab under the `Privileged Gateway Intents` section on.
3. Create a `.env` in the same directory as the Python files (`\src\.env`) with the content:
```bash
DISCORD_TOKEN=put_the_bot_token_you_just_copied_in_here
```