def welcomeUser():
    print('\nWelcome to the text analysis tool, I will mine and analyze a body of text you send me')

#get username
def getUsername():
    userNameFromInput =input('\nTo begin please, Enter your name: \n')
    return userNameFromInput

username= getUsername()

#greet the users
def greetUser(name):
    print('Welcome, ' + name)

greetUser(username)