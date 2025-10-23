from random_username.generate import generate_username

def welcomeUser():
    print('\nWelcome to the text analysis tool, I will mine and analyze a body of text you send me')

#get username
def getUsername():
    userNameFromInput =input('\nTo begin please, Enter your name: \n')

    if  (len(userNameFromInput) < 5 or not userNameFromInput.isidentifier()):
        print('Your username has to be greater than 5 character, alphanumeric and not contain spaces')
        userNameFromInput = generate_username()[0]
        print('Assigning a default Username....')


    return userNameFromInput

username= getUsername()

#greet the users
def greetUser(name):
    print('Welcome, ' + name)

greetUser(username)