import keyring

def get_gmail_credentials():
    username = 'your.email@gmail.com'
    password = keyring.get_password('gmail', username)
    return (username, password)
