class User:
    def __init__(self, username, password):
        # should also save user in server
        self.username = username
        self.__password = password
        self.books_in_possession = None
    
    def add_book(book):
        if self.books_in_possession == None:
            self.books_in_possession = []
        self.books_in_possession.append(book)
    
    def update_password(password):
        if self.__password == password:
            return "choose a different password"
        self.__password = password
        return "password successfully changed"


    def __del__():
        # should also delete in server
        pass 