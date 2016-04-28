import smtplib
import os
from getpass import getpass

path = os.getcwd()
print(path)

# Get a username and password safely


def get_credentials():
    username = input("Enter gmail address: \n")
    password = ""
    while True:
        password_1 = getpass("Enter password: ")
        password_2 = getpass("Confirm password: ")
        if password_1 == password_2:
            password = password_1
            break
        else:
            print("Passwords do not match")

    if "@gmail.com" not in username.lower():
        username += "@gmail.com"

    print("Trying to create an account for", username)

    return username, password


# create a secrets module with the stored uname and password


def create_secrets():
    username, password = get_credentials()
    code = "username = " + "\'" + username + "\'" + "\n" +\
           "password = " + "\'" + password + "\'"

    file_path = "backend/secrets.py"
    if "raspberry-automation/backend" in path:
        file_path = "secrets.py"

    print("creating a secrets.py file at", file_path)
    with open(file_path, "w+") as module:
        module.write(code)

    module.close()


def import_secrets():
    global username
    global password

    if "raspberry-automation/backend" in path:
        from secrets import username, password
    else:
        from backend.secrets import username, password


def create_and_import():
    create_secrets()
    print("created secrets.py file, trying to import again")
    import_secrets()

try:
    import_secrets()
except ImportError:
    print("There is no secrets.py file hosting the username or password")
    create_and_import()


def send_email(addresses):
    msg = "The house door has been opened!\n www.metcalfeautomate.tk"
    try:
        s = smtplib.SMTP("smtp.gmail.com:587")
        s.starttls()
        s.login(username, password)
        s.sendmail(username, addresses, msg)
        print("sent an email to", addresses)
        s.quit()
    except smtplib.SMTPAuthenticationError:
        msg = "invalid username or password, please double check secrets.py"
        raise RuntimeError(msg)

if __name__ == "__main__":
    send_email(["viraj3f@gmail.com"])
