import random  # For random account number generation
import database  # User database for storing user info
import validation  # For User input validation
import os
from getpass import getpass
from database import delete_auth_session


# Initialize the system

def init():
    print("Welcome to Bank Python!")
    have_account = input("Do you have an account with us? 1: Yes, 2: No \n")
    is_valid_user_input = validation.user_input_validation(have_account)
    if is_valid_user_input:

        if int(have_account) == 1:
            login()
        elif int(have_account) == 2:
            register()
        else:
            print("You have entered an invalid option. Please try again.")
            init()
    else:
        init()


def login():
    print("****** Login ******")

    account_number_from_user = input("Enter your account number: \n")
    is_valid_account_number = validation.account_number_validation(account_number_from_user)
    if is_valid_account_number:
        password = getpass("Enter your password: \n")
        user = database.authenticated_user(account_number_from_user, password)

        if user:
            database.create_auth_session(account_number_from_user)
            bank_operations(user)

        print("Invalid account or password. Please try again.")
        login()
    else:
        print("Account number invalid.")
        init()
    return account_number_from_user


def register():
    print("****** Register ******")

    email = input("Enter your email address: \n")
    first_name = input("Enter your Firstname: \n")
    last_name = input("Enter your Lastname: \n")
    password = getpass("Create a Password: \n")
    account_balance = int(input("How much do you want to Deposit? \n"))
    try:
        account_number = generate_account_number()
    except TypeError:
        print("An exception occurred. Account Generation failed.")
        init()
    # accepted_user_details = first_name + "," + last_name + "," + email + "," + password + "," + str(account_balance)
    is_user_created = database.create(account_number, first_name, last_name, email, password, account_balance)
    # account_number = (f"PY{generate_account_number()}") -- This method can be used if a string prefix is required.
    if is_user_created:
        print(f"Registration Completed Successfully! \n Your account number is {account_number}")
        login()
    else:
        print("Something went wrong. Please try again.")
        register()


def bank_operations(user):
    print(f"Welcome {user[1]} , {user[2]}")
    selected_option = int(
        input("What would you like to do today? 1. Deposit 2. Make a Withdrawal 3. Logout 4. Exit \n"))

    if selected_option == 1:
        deposit_operation(user)
    elif selected_option == 2:
        withdrawal_operation(user)
    elif selected_option == 3:
        logout()
    elif selected_option == 4:
        exit()
    else:
        print("Invalid option selected.")
        bank_operations(user)


def withdrawal_operation(user):
    print("Withdrawal")
    current_balance = int(get_current_balance(user))
    print(f" Your current balance is {current_balance}")
    amount_to_withdraw = int(input("How much do you want to withdraw? \n"))
    if amount_to_withdraw > current_balance:
        print("Insufficient Balance!")
    else:
        current_balance = current_balance - amount_to_withdraw
        print("Please take your cash.")
    set_current_balance(user, current_balance)
    print(f" Your current balance is {current_balance}")
    user_input = int(input("Do you want to perform another operation? 1. Yes 2.No \n"))
    if user_input == 1:
        bank_operations(user)
    elif user_input == 2:
        logout()
    else:
        print("Invalid option selected.")
        exit()


def deposit_operation(user):
    print(type(user))
    print(user)
    print("Deposit Operations")
    current_balance = get_current_balance(user)
    amount_to_deposit = int(input("How much do you want to deposit? \n"))
    current_balance = int(current_balance) + amount_to_deposit
    set_current_balance(user, current_balance)
    print("Deposit Successful.")
    print(f" Your current balance is {current_balance}")
    user_input = int(input("Do you want to perform another operation? 1. Yes 2.No \n"))
    if user_input == 1:
        bank_operations(user)
    elif user_input == 2:
        exit()
    else:
        print("Invalid option selected.")
        exit()
    return user


def generate_account_number():
    return random.randrange(1111111111, 9999999999)
    # learn to to generate a user sequence account number


def get_current_balance(user_details):
    return user_details[5]


def set_current_balance(user, balance):
    user[5] = balance
    print(type(user))
    print(database.user_db_path + str(user[0]) + ".txt")
    if os.path.exists(database.user_db_path + str(user[0]) + ".txt"):
        try:
            f = open(database.user_db_path + str(user[0]) + ".txt", "w")
            f.write(user)
            f.close()
        except FileNotFoundError:
            print("File does not exist.")
    else:
        print("No such file.")


def logout():
    if login():
        delete_auth_session(login())

    # login()


init()
