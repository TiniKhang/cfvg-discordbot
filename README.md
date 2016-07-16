# cfvg-discordbot (Version: 0.2)
Discord Bot for Cardfight Vanguard

### Running locally

1. Install Python 3.5 or higher
2. Install [discord.py](https://github.com/Rapptz/discord.py) (python -m pip install -U discord.py)
2. Follow [reactiflux's instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
3. Clone or Download then extract this repository
4. Create a new file called "token.key", then paste the token generated from step 3 into the file (one line only).
5. Run cfvgbot.py
6. The vanguard database is not installed by default. Run this to get the most recent:
   '''
   import getcardinfo
   getcardinfo.updatedb(True)
   '''

### Features

 - Hypergeometric Calculator for calculating card probabilities
   - accepts BEDMAS operations using a shunting yard algorithm and reverse polish notation (rpn) interpreter, with custom operators
   - avoids standard "eval" for safety
 - Card Effects
   - submits a search request to cf-vanguard.com/cardlist
   - pulls data from the cf-vanguard card page