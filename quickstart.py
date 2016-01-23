from gmailGetter import GmailGetter

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    x = GmailGetter('stepikmvk')
    print(*x.getMessagesList('152696e789999f1d'), sep='\n')
    x.getMessage('1515f387190791b6')
    #get_messages_list(service)


if __name__ == '__main__':
    main()
