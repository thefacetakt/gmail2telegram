from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

ATTACHMENTS_FOLDER = 'attachments/'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def downloadAttachment(service, part, messageId):
    attachmentId = part["body"]["attachmentId"]
    result = service.users().messages().attachments().get(userId='me',
        messageId=messageId, id=attachmentId).execute()
    directory = ATTACHMENTS_FOLDER + messageId + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    outFile = open(directory + part['filename'], 'wb')
    outFile.write(base64.urlsafe_b64decode(result["data"].encode('UTF-8')))
    outFile.close()

def printParts(service, parted, messageId):
    for i in parted:
        if ("parts" in i):
            printParts(service, i["parts"], messageId)
        elif "data" in i["body"]:
            if (i["mimeType"] == "text/plain"):
                print(base64.urlsafe_b64decode(i["body"]["data"].encode('UTF-8')).decode("UTF-8"))
        elif "attachmentId" in i["body"]:
            print(i["filename"])
            downloadAttachment(service, i, messageId)

def get_message(service, id):
    result = service.users().messages().get(userId='me', id=id).execute()
    parts = result['payload']["parts"]
    printParts(service, parts, id)

def get_messages_list(service):
    response = service.users().messages().list(userId='me').execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me',
                                         pageToken=page_token).execute()
        print(response['messages'])
        messages.extend(response['messages'])
    print(messages)
    return messages



def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    get_message(service, '1515f387190791b6')
    get_messages_list(service)
    #get_messages_list(service)


if __name__ == '__main__':
    main()
