from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64
from gmailGetter import GmailGetter

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    x = GmailGetter('stepikmvk')
    print(*x.get_messages_list('152696e789999f1d'), sep='\n')
    x.get_message('1515f387190791b6')
    #get_messages_list(service)


if __name__ == '__main__':
    main()
