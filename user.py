from book import Book
class User:
    def __init__(self, username, password):
        # should also save user in server
        self.username = username
        self.__password = password
        self.books_in_possession = None # lisy book objects, not title
        self.chat_tokens_map = None

    def is_authenticated(): # needed for flask-login, rudimentary hardcoded
        return True 
    
    def is_active(): # needed for flask-login, rudimentary hardcoded
        return True

    def get_id(self): # needed for flask-login, rudimentary hardcoded
        return self.username
    
    def is_anonymous(): # needed for flask-login, rudimentary hardcoded
        return False

    def add_book(self, _book): # add book objects, not title
        if self.books_in_possession == None:
            self.books_in_possession = []
        self.books_in_possession.append(_book)
    
    def delete_book(self, book_title):
        if self.books_in_possession == None:
            return
        indx = 0
        for x in range(len(self.books_in_possession)):
            item = self.books_in_possession[indx]
            if item.title == book_title:
                self.books_in_possession.pop(indx)
                indx -= 1
            indx += 1
        if self.books_in_possession == []:
            self.books_in_possession = None
    
    def update_password(self, password):
        # returns boolean: true if password successfully changed, false otherwise
        if self.__password == password:
            return False
        self.__password = password
        return True
    
    def login_check_password(self, password_entered):
        if self.__password == password_entered:
            return True
        return False

    def new_chat(self, chat_token, other_person_in_chat):
        if self.chat_tokens_map:
            self.chat_tokens_map[chat_token] = other_person_in_chat
        else:
            self.chat_tokens_map = {chat_token: other_person_in_chat}

    def __del__(self):
        # should also delete in server
        pass 