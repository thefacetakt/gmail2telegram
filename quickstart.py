from gmailGetter import GmailGetter
import TelegramSender
import os
import threading
from time import sleep

class Gmail2TelegramClient:
    def initLastUpdateAndMessageId(self):
        updateFileName = os.path.join(self.getter.currentPath, "lastUpdate")
        if not os.path.exists(updateFileName):
            updateFile = open(updateFileName, "w")
            updateFile.write("0\n\n")
            updateFile.close()
            self.lastUpdate = 0
            self.lastMessageId = ""
            return 0
        updateFile = open(updateFileName, "r")
        self.lastUpdate = int(updateFile.readline())
        self.lastMessageId = updateFile.readline()[:-1]
        updateFile.close()

    def updateLasts(self):
        updateFileName = os.path.join(self.getter.currentPath, "lastUpdate")
        updateFile = open(updateFileName, "w")
        updateFile.write(str(self.lastUpdate) + "\n"
            + self.lastMessageId + "\n")
        updateFile.close()

    def __init__(self, chatId):
        self.getter = GmailGetter(chatId)
        self.chatId = chatId
        self.initLastUpdateAndMessageId()
        print(self.lastMessageId)
        self.run()
        t = threading.Thread(target=self.run)
        t.start()


    def processMessage(self, messageId):
        if self.getter.getMessage(messageId):
            TelegramSender.sendEmail(self.getter.ATTACHMENTS_FOLDER, messageId,
                self.chatId)

    def run(self):
        while True:
            try:
                messages = self.getter.getMessagesList(self.lastMessageId)
                messages = messages[::-1]
                print(messages)
                for i in messages:
                    print(i["id"])
                    self.processMessage(i["id"])
                    self.lastMessageId = i["id"]
                    self.updateLasts()
                    print("Updated")
                sleep(5)
            except Exception as e:
                print(e)

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    Gmail2TelegramClient("78426908")

if __name__ == "__main__":
    main()
