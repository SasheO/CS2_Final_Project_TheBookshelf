class Book:
    def __init__(self, title: str, author: str, genre=None):
        self.title = title
        self.author = author
        self.genre = genre
        # todo: should also save in server
    
    def __del__(self):
        # todo: should also delete in server
        pass 