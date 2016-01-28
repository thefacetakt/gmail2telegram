from gmail2TelegramClient import Gmail2TelegramClient

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    Gmail2TelegramClient("1234") #a person
    Gmail2TelegramClient("-1234") #group chat

if __name__ == "__main__":
    main()
