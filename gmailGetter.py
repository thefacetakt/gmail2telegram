from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64

import config

class GmailGetter:
    @staticmethod
    def getCredentials(path):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credentialDir = os.path.join(path, ".credentials")
        if not os.path.exists(credentialDir):
            os.makedirs(credentialDir)
        credentialPath = os.path.join(credentialDir,
                                       "gmail2telegram.json")

        store = oauth2client.file.Storage(credentialPath)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE,
                config.SCOPES)
            flow.user_agent = config.APPLICATION_NAME
            print("Storing credentials to " + credentialPath)
        return credentials

    def __init__(self, currentClient):
        currentPath = os.path.join(config.WORKING_DIRECTORY, currentClient)
        if not os.path.exists(currentPath):
            os.makedirs(currentPath)
        credentials = GmailGetter.getCredentials(currentPath)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build("gmail", "v1", http=http)
        self.ATTACHMENTS_FOLDER = os.path.join(currentPath, "attachments/")

    @staticmethod
    def addMessagesFromRespone(response, messages, sinceId):
        if "messages" in response:
            for i in range(len(response["messages"])):
                if response["messages"][i]["id"] == sinceId:
                    messages.extend(response["messages"][:i + 1])
                    return True
            messages.extend(response["messages"])
        return False

    def getMessagesList(self, sinceId=None):
        response = self.service.users().messages().list(userId="me").execute()
        messages = []
        if GmailGetter.addMessagesFromRespone(response, messages, sinceId):
            return messages

        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = self.service.users().messages().list(userId="me",
                                             pageToken=page_token).execute()
            if GmailGetter.addMessagesFromRespone(response, messages, sinceId):
                return messages
        return messages

    def writeDownloadedPart(self, body, name, messageId):
        directory = self.ATTACHMENTS_FOLDER + messageId + "/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        outFile = open(directory + name, "wb")
        outFile.write(base64.urlsafe_b64decode(body.encode("UTF-8")))
        outFile.close()

    def downloadAttachment(self, part, messageId):
        attachmentId = part["body"]["attachmentId"]
        result = self.service.users().messages().attachments().get(userId="me",
            messageId=messageId, id=attachmentId).execute()
        directory = self.ATTACHMENTS_FOLDER + messageId + "/"

        self.writeDownloadedPart(result["data"], part["filename"], messageId)

    def printParts(self, parted, messageId):
        for i in parted:
            if ("parts" in i):
                self.printParts(i["parts"], messageId)
            elif "data" in i["body"]:
                if (i["mimeType"] == "text/plain"):
                    self.writeDownloadedPart(i["body"]["data"],
                            messageId + "text.txt", messageId)
            elif "attachmentId" in i["body"]:
                print(i["filename"])
                self.downloadAttachment(i, messageId)

    def getMessage(self, id):
        result = self.service.users().messages().get(userId="me",
            id=id).execute()
        parts = result["payload"]["parts"]
        self.printParts(parts, id)
