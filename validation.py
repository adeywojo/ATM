def account_number_validation(account_number):
    if account_number:

        try:
            int(account_number)
            if len(str(account_number)) == 10:
                return True
        except ValueError:
            return False
        except TypeError:
            return False

    return False


def user_input_validation(have_account):
    try:
        if int(have_account):
            return True
    except TypeError:
        print("Invalid Input. Please choose between options 1 & 2.")
        return False
