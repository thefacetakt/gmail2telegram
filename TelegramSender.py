import config
from TelegramBotAPI.client.basic import BasicClient
from TelegramBotAPI.types.methods import sendMessage, getUpdates, sendDocument
from TelegramBotAPI.types.compound import Message, File
import os

client = BasicClient(config.TELEGRAM_TOKEN)

def sendWholeMessage(chatId, text):
    chunkSize = 1024
    for i in range(0, len(text), chunkSize):
        msg = sendMessage()
        msg.chat_id = chatId
        msg.text = text[i:i + chunkSize]
        client.post(msg)

def sendEmail(attachmentsFolder, messageId, chatId):
    attachmentsFolder = os.path.join(attachmentsFolder, messageId)
    files = os.listdir(attachmentsFolder)
    textFileName = messageId + "text.txt"
    if (textFileName in files):
        files.remove(textFileName)
        textFile = open(os.path.join(attachmentsFolder, textFileName), "r")
        text = "New email:\n" + textFile.read()
        textFile.close()
        sendWholeMessage(chatId, text)
    for fileItem in files:
        msg = sendDocument()
        msg.chat_id = chatId
        msg.document = os.path.join(attachmentsFolder, fileItem)
        client.post(msg)
