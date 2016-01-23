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
    def get_credentials(path):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = os.path.join(path, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail2telegram.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.CLIENT_SECRET_FILE,
                config.SCOPES)
            flow.user_agent = config.APPLICATION_NAME
            print('Storing credentials to ' + credential_path)
        return credentials

    def __init__(self, currentClient):
        currennt_path = os.path.join(os.getcwd(), currentClient)
        if not os.path.exists(currennt_path):
            os.makedirs(currennt_path)
        credentials = GmailGetter.get_credentials(currennt_path)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)
        self.ATTACHMENTS_FOLDER = os.path.join(currennt_path, 'attachments/')

    @staticmethod
    def addMessagesFromRespone(response, messages, sinceId):
        if 'messages' in response:
            for i in range(len(response['messages'])):
                if response['messages'][i]['id'] == sinceId:
                    messages.extend(response['messages'][:i + 1])
                    return True
            messages.extend(response['messages'])
        return False

    def get_messages_list(self, sinceId=None):
        response = self.service.users().messages().list(userId='me').execute()
        messages = []
        if GmailGetter.addMessagesFromRespone(response, messages, sinceId):
            return messages

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId='me',
                                             pageToken=page_token).execute()
            if GmailGetter.addMessagesFromRespone(response, messages, sinceId):
                return messages
        return messages

    def downloadAttachment(self, part, messageId):
        attachmentId = part['body']['attachmentId']
        result = self.service.users().messages().attachments().get(userId='me',
            messageId=messageId, id=attachmentId).execute()
        directory = self.ATTACHMENTS_FOLDER + messageId + '/'

        if not os.path.exists(directory):
            os.makedirs(directory)

        outFile = open(directory + part['filename'], 'wb')
        outFile.write(base64.urlsafe_b64decode(result["data"].encode('UTF-8')))
        outFile.close()

    def printParts(self, parted, messageId):
        for i in parted:
            if ("parts" in i):
                self.printParts(i["parts"], messageId)
            elif "data" in i["body"]:
                if (i["mimeType"] == "text/plain"):
                    print(base64.urlsafe_b64decode(i["body"]["data"]
                        .encode('UTF-8')).decode("UTF-8"))
            elif "attachmentId" in i["body"]:
                print(i["filename"])
                self.downloadAttachment(i, messageId)

    def get_message(self, id):
        result = self.service.users().messages().get(userId='me', id=id).execute()
        parts = result['payload']["parts"]
        self.printParts(parts, id)
