# User database for storing Account information
import os
import validation
from datetime import datetime

user_db_path = "data/user_record/"
session_data_path = "data/auth_session/"
f = None


def create(user_account_number, first_name, last_name, email, password, account_balance):
    global f
    user_data = str(
        user_account_number) + "," + first_name + "," + last_name + "," + email + "," + password + "," + str(
        account_balance)
    if does_account_number_exist(user_account_number):
        return False
    if does_email_exist(email):
        print("User already exists.")
        return False
    completion_state = False
    try:
        print("Creating a new user record.")
        f = open(user_db_path + str(user_account_number) + ".txt", "x")

    except FileExistsError:
        does_file_contain_data = read(user_db_path + str(user_account_number) + ".txt")
        if not does_file_contain_data:
            delete(user_account_number)
    else:
        f.write(str(user_data))
        completion_state = True
    finally:
        f.close()
        return completion_state


def read(user_account_number):
    is_valid_account_number = validation.account_number_validation(user_account_number)
    try:
        if is_valid_account_number:
            t = open(user_db_path + str(user_account_number) + ".txt", "r")
        else:
            t = open(user_db_path + user_account_number, "r")
    except FileNotFoundError:
        print("User not found.")
    except FileExistsError:
        print("User does not exist.")
    except TypeError:
        print("Invalid account number format.")
    else:
        return t.readline()
    return False


def delete(user_account_number):
    is_delete_successful = False
    if os.path.exists(user_db_path + str(user_account_number) + ".txt"):
        try:
            os.remove(user_db_path + str(user_account_number) + ".txt")
            is_delete_successful = True
        except FileNotFoundError:
            print("File does not exist.")
        finally:
            return is_delete_successful


def does_email_exist(email):
    all_users = os.listdir(user_db_path)
    for user in all_users:
        user_list = str.split(read(user), ',')
        if email in user_list:
            return True
    return False


def does_account_number_exist(account_number):
    all_users = os.listdir(user_db_path)
    for user in all_users:
        if user == str(account_number) + ".txt":
            return True
    return False


def authenticated_user(account_number, password):
    if does_account_number_exist(account_number):
        user = str.split(read(account_number), ',')
        if password == user[4]:
            return user
    return False


def create_auth_session(user_account_number):
    global f
    is_session_started = False
    session_data = str(user_account_number) + "," + str(datetime.now()) + "\n"
    try:
        f = open(session_data_path + str(user_account_number) + ".txt", "a")
    except FileExistsError:
        does_file_contain_data = read(session_data_path + str(user_account_number) + ".txt")
        if not does_file_contain_data:
            delete(user_account_number)
    else:
        f.write(str(session_data))
        is_session_started = True
    finally:
        f.close()
        return is_session_started


def delete_auth_session(account_number_from_user):
    try:
        if os.path.exists(session_data_path + str(account_number_from_user) + ".txt"):
            os.remove(session_data_path + str(account_number_from_user) + ".txt")
    except FileExistsError:
        print("Session could not be deleted.")
