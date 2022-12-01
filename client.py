import requests

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

def login_or_signup(username, password, l_or_s):
    if l_or_s == "l":
        l_or_s = "login"
    else:
        l_or_s = "signup"
    login_data = {"username": username, "password": password}
    response = requests.post(BASE_URL + l_or_s, json=login_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])
    if output['msg'] == f"welcome back, {username}":
        return True
    return False
    
def my_books(username): # for lenders only
    print("-"*15)
    print("My Books")
    options = ["view", "add", "delete","delete all"]
    for indx in range(len(options)):
        print(str(indx+1) + ". " + options[indx])

    exxit = False
    while exxit == False:
        option_chosen = input("Enter 1, 2, 3 or 4 to pick an option: ")
        try:
            option_chosen = options[int(option_chosen)-1]
            exxit = True
        except:
            print("Invalid option chosen")
    my_books_data = {"option": option_chosen,"username": username}

    if option_chosen == "add" or option_chosen == "delete":
        my_books_data['titles'] = []
        exxit = False
        while exxit == False:
            title = input(f"Enter titles you wish to {option_chosen}: ")
            my_books_data['titles'].append(title)
            more = input("Add more? Enter 'y' or 'n': ").lower().strip()
            if more == "n":
                exxit = True
    response = requests.post(BASE_URL + "my_books", json=my_books_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])

def book_search(username=None): # for borrowers/not logged in
    print("-"*15)
    title = input("What books are you searching for? ")
    book_search_data = {"book title": title}
    response = requests.get(BASE_URL + "book_search", json=book_search_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])
    return title

def borrow_request(username): # for borrowers
    print("-"*15)
    book = input("Which book do you want to borrow? ")
    lender = input("Who do you want to get it from? ")
    borrow_request_data = {"borrower username" : username, "book": book,    "lender username" : lender}
    response = requests.get(BASE_URL + "borrow_request", json=borrow_request_data)
    print(response.json()['msg'])

def view_my_requests(username): # for lenders only
    print("-"*15)
    # TODO: make view my requests more user friendly in server
    view_my_requests_data = {"lender username" : username}
    response = requests.get(BASE_URL + "view_my_requests", json=view_my_requests_data)
    if response.status_code != 200:
        print(f"Error encountered viewing the borrow requests sent to you. Error code: {response.status_code}")
        return
    print(response.json()['msg'])

def grant_book_request(username): # lenders only
    print("-"*15)
    book = input("What book? ")
    borrower = input("Whose request are you deciding? Type in username: ")
    decision = input("Enter 'y' to accept or 'n' to decline: ").lower().strip()
    if decision == 'y':
        decision = True
    else:
        decision = False
    grant_book_request_data = {
    "lender username" : username,
    "book" : book,
    "borrower username" : borrower,
    "decision" : decision
    } 
    response = requests.get(BASE_URL + "grant_book_request", json=grant_book_request_data)
    if response.status_code != 200:
        print(f"Error encountered viewing the borrow requests sent to you. Error code: {response.status_code}")
        return
    print(response.json())

def my_chats(username): # for borrowers and lenders
    print("-"*15)
    print("My Chats")
    options = ["view chats", "view messages", "send messages"]
    for indx in range(len(options)):
        print(str(indx+1) + ". " + options[indx])

    exxit = False
    while exxit == False:
        option_chosen = input("Enter 1, 2 or 3 to pick an option: ")
        try:
            option_chosen = options[int(option_chosen)-1]
            exxit = True
        except:
            print("Invalid option chosen")
    my_chats_data = {"option": option_chosen,"username": username}

    if option_chosen == "view chats":
        response = requests.get(BASE_URL + "my_chats", json=my_chats_data)
        if response.status_code != 200:
            print(f"Error encountered viewing your chats. Error code: {response.status_code}")
            return
        if 'chats' in response.json():
            print(response.json()['chats'])
        else:
            print(response.json()['msg'])
        return

    chat_with = input("Enter the name of the person the chat is with: ")
    my_chats_data["with"] = chat_with
    if option_chosen == "send messages":
        message = input("Type message: ")
        my_chats_data["message"] = message
    response = requests.get(BASE_URL + "my_chats", json=my_chats_data)

    if response.status_code != 200:
        print(f"Error encountered {option_chosen[:4]}ing message to {chat_with}. Error code: {response.status_code}")
        return
    print("-"*15)
    if 'chat' in response.json():
        print(response.json()['chat'])
    else:
        print(response.json()['msg'])

def lender_options(username):
    options = {"1": ("My Books", my_books), "2": ("My Chats", my_chats), "3": ("View book requests sent to me", view_my_requests), "4":("Make decision on book request", grant_book_request)}
    for indx in options:
        print(indx + ". " + options[indx][0])

    exxit = False
    while exxit == False:
        option_chosen = input("Enter 1, 2 or 3 to pick an option: ").strip()
        if option_chosen in options:
            exxit = True
        else:
            print("Invalid option chosen")
    func = options[option_chosen][1]
    func(username)

def borrower_options(username):
    options = {"1": ("Search the Bookshelf for a title", book_search), "2": ("My Chats", my_chats), "3": ("Ask to borrow a book", borrow_request)}
    for indx in options:
        print(indx + ". " + options[indx][0])

    exxit = False
    while exxit == False:
        option_chosen = input("Enter 1, 2 or 3 to pick an option: ").strip()
        if option_chosen in options:
            exxit = True
        else:
            print("Invalid option chosen")
    func = options[option_chosen][1]
    func(username)

if __name__=="__main__":
    l_or_s = input("Enter 'L' to login or 'S' to sign up or 'B' to search the Bookshelf for a title: ").lower().strip()
    if l_or_s == 'b':
        book_search()
    else:
        username = input("enter username: ")
        password = input("enter password: ")

        logged_in = login_or_signup(username, password, l_or_s)

        if logged_in:
            borrower_or_lender = input("Do you want to be a borrower or lender?\nEnter 'b' for borrower or 'l' for lender: ").lower().strip()
            while borrower_or_lender not in ["b","l"]:
                print("Invalid option chosen.")
                borrower_or_lender = input("Do you want to be a borrower or lender?\nEnter 'b' for borrower or 'l' for lender: ").lower().strip()
            while True:
                print("-"*15)
                if borrower_or_lender == "b":
                    borrower_options(username)
                else:
                    lender_options(username)
                logout = input("Do you want to logout? Enter 'y' or 'n': ").lower().strip()
                if logout == "y":
                    break


