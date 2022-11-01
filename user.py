class User:
    def __init__(self, username, password):
        # should also save user in server
        self.username = username
        self.__password = password
        self.books_in_possession = None
    
    def add_book(self, book):
        if self.books_in_possession == None:
            self.books_in_possession = []
        self.books_in_possession.append(book)
    
    def update_password(self, password):
        # returns boolean: true if password successfully changed, false otherwise
        if self.__password == password:
            return False
        self.__password = password
        return True


    def __del__(self):
        # should also delete in server
        pass 