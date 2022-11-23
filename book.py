class Book:
    def __init__(self, title: str, owner_username, author=None, genre=None):
        self.title = title
        self.owner_username = owner_username
        self.author = author
        self.genre = genre
        self.available_for_lending = True
    
    def lend(self):
        self.available_for_lending = False

    def unlend(self):
        self.available_for_lending = True

    def __del__(self):
        # todo: should also delete in server
        pass 