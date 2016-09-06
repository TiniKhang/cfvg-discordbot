# cfvg-discordbot (Version: 0.4)
Discord Bot for Cardfight Vanguard

### Running locally

\*Running locally means you have to keep the python window open else the bot dies. Run on heroku to keep it alive.

1. Install Python 3.5 or higher
2. Install [discord.py](https://github.com/Rapptz/discord.py) (python -m pip install -U discord.py)
3. Follow [reactiflux's instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
4. Clone or Download then extract this repository
5. Create a new file called "token.key", then paste the token generated from step 3 into the file (one line only)
6. The vanguard database is not installed by default. Run this to get the most recent:
   
   ```python
   import getcardinfo
   getcardinfo.updatedb(True)
   ```

7. Run cfvgbot.py and enjoy!

### Running on heroku

1. Install Python 3.5 or higher
2. Sign up for a free [heroku account](https://www.heroku.com/)
3. run "pip install virtualenv"
4. Download and install the [heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)
5. Command line stuff. Mostly from the [tutorials](https://devcenter.heroku.com/articles/getting-started-with-python#prepare-the-app):

	```sh
	heroku login

	git clone https://github.com/NanoSmasher/cfvg-discordbot.git
	cd cfvg-discordbot
	```

6. Follow [reactiflux's instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
7. Create a new file called "token.key", then paste the token generated from step 3 into the file (one line only)
8. The vanguard database is not installed by default. Run this to get the most recent:
   
   ```python
   import getcardinfo
   getcardinfo.updatedb(True)
   ```

9. Try this:

	```sh
	heroku create
	git push heroku master
	heroku ps:scale web=1
	```

##### Troubleshooting 

You should see your app on the [dashboard](https://dashboard.heroku.com/apps). I had to turn on the free dyno feature. If you did some edits you'll need to update with:

```sh
git commit -a
git push heroku master
```

you can find logs in that specific app with:

```sh
heroku logs -n 20
heroku logs -t
```

### Features

 - Hypergeometric Calculator for calculating card probabilities
   - accepts BEDMAS operations using a shunting yard algorithm and reverse polish notation (rpn) interpreter, with custom operators
   - avoids standard "eval" for safety
 - Card Effects
   - ~~submits a search request to cf-vanguard.com/cardlist~~ DEPRECIATED
   - ~~pulls data from the cf-vanguard card page~~
   - pulls data from the cardfight wiki
   
### Commands

vbot cascadeodds
vbot hgcc
vbot quickodds
vbot eval

\* \[\[card name]] \*