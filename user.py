from book import Book
class User:
    def __init__(self, username, password):
        # should also save user in server
        self.username = username
        self.__password = password
        self.books_in_possession = None
        self.my_requests = {}   #TODO: Is this something i need ot save in a file so we don't loose each users data

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
        #NOT TESTED
        '''
        It stores the book requested as the key of the dictionary.
        Each book maps to another dictionary containing all the requests for a specific book 
        received form various users.
        It also contains a boolean you can set to true to indicate that you want to borrow the book out.
        '''
        if book not in self.myrequests:
            self.my_requests[book] ={}
        requests_count = 1
        for value in range(0,len(self.myrequests), step=2):
            requests_count += 1
        username = 'borrower' + str(requests_count)
        lend = 'Lend to user' + str(requests_count)
        self.my_requests[book][username] = borrower
        self.my_requests[book][lend] = False


    def __del__(self):
        # should also delete in server
        pass 