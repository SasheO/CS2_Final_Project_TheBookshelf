from book import Book
from flask_app import save_book_requests_to_server, load_book_requests_from_server
class User:
    def __init__(self, username, password):
        # should also save user in server
        self.username = username
        self.__password = password
        self.books_in_possession = None

    def is_authenticated(): # needed for flask-login, rudimentary hardcoded
        return True 
    
    def is_active(): # needed for flask-login, rudimentary hardcoded
        return True

    def get_id(self): # needed for flask-login, rudimentary hardcoded
        return self.username
    
    def is_anonymous(): # needed for flask-login, rudimentary hardcoded
        return False

    def add_book(self, book):
        if self.books_in_possession == None:
            self.books_in_possession = []
        self.books_in_possession.append(book)
    
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

    def book_requests(self, borrower, book):    #a dictionary containing all the book requests the user has gotten
        #How do i store the created dictionary in the pkl file book_requests?
        #and how do I initialise the users requests dictionary as the dictionary in the pkl file?
        #NOT TESTED
        '''
        It stores the name of the user as the key of the dictionary.
        Each user is mapped to another dictionary containing the book titles 
        and the users that have requested too borrow the book
        It also contains a boolean you can set to true to indicate that you want to 
        borrow the book out to a specific user
        '''
        BOOK_REQUESTS = {}
        load_book_requests_from_server()

        if self.username not in BOOK_REQUESTS:
            BOOK_REQUESTS[self.username] = {}
        if book not in BOOK_REQUESTS[self.username]:
            BOOK_REQUESTS[self.username][book] ={}

        requests_count = 1
        for value in range(0,len(BOOK_REQUESTS[self.username][book]), step=2):
            requests_count += 1
        # borrower_count = 'borrower ' + str(requests_count)
        BOOK_REQUESTS[self.username][book][borrower] = False

        save_book_requests_to_server()


    def __del__(self):
        # should also delete in server
        pass 