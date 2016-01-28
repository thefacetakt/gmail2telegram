## Gmail2Telegram
----------------
A server tool (basically, a Telegram bot), which redirects your gmail messages (with attachments) to your telegram accounts

NOTE: it is a very raw version.

NOTE: your e-mails will be stored on a computer, where you'll run a script.

How to install:

* I used python3, [google gmail api](https://developers.google.com/gmail/api/quickstart/python) and [pyTelegramBotAPI](https://github.com/sourcesimian/pyTelegramBotAPI), so you might want to install them:

    ```pip3 install --upgrade google-api-python-client```

    ```pip3 install TelegramBotAPI```

* [Get yourself a telegram bot](https://core.telegram.org/bots)

* ```git clone https://github.com/thefacetakt/gmail2telegram.git```

* Fill ```config.py``` with your working directory (a place where quickstart.py is stored) and Telegram Bot token

* Set a chat you want to collect your e-mail in ```quickstart.py```, in ```main``` function: ```Gmail2TelegramClient("1234567")```, where ```1234567``` is your chat id.

How to use:

* ```python3 quickstart.py```

* If you are running a tool for the very first time for particular chat, there will be a link you need to follow in stdout (in order to pass oauth)

* Good luck!


Known bugs:
* E-mails with only html content (no plain text) are ignored
* If you delete your last e-mail, everything will go nuts
* No proper logging -- only ugly debug output
