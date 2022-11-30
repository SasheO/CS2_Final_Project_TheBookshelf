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

def book_search(): # for borrowers/not logged in
    title = input("What books are you searching for? ")
    book_search_data = {"book title": title}
    response = requests.get(BASE_URL + "book_search", json=book_search_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])


# l_or_s = input("Enter 'L' to login or 'S' to sign up:").lower().strip()

username = input("enter username: ")
password = input("enter password: ")

# logged_in = login_or_signup(username, password, l_or_s)

# if logged_in:
#     borrower_or_lender = input("Do you want to be a borrower or lender?\nEnter 'b' for borrower or 'l' for lender: ")

book_search()