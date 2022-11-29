class MessageNode:
    '''
    arguments for initialization:
    message- string of what the user is sending
    sender - username of who is sending the message
    '''
    def __init__(self, message, sender):
        self.sender = sender
        self.message = message
        self.next = None
        self.seen = False

    def mark_as_seen(self):
        self.seen = True

class ChatLinkedList:
    '''
    arguments for initialization:
    usernames: a list of size 2 (for now) containing usernames of the people in the chat
    '''
    def __init__(self, usernames):
        self.head = None
        self.messengers = usernames # a list of usernames of those in the chat

    def add_message(self, message):
        message.next = self.head
        self.head = message

    def str_messages(self):
        # return a list of all string messages
        messages_string = ''
        current = self.head
        while current:
            messages_string = current.sender + ": " + current.message + "\n" + messages_string
            current = current.next
        return messages_string