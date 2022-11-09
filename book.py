class Book:
    def __init__(self, title: str, author: str, genre=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.available_for_lending = True
        # todo: should also save in server
    
    def lend(self):
        self.available_for_lending = False

    def unlend(self):
        self.available_for_lending = True

    def __del__(self):
        # todo: should also delete in server
        pass 