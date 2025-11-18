from random_username.generate import generate_username

def welcomeUser():
    print('\nWelcome to the text analysis tool, I will mine and analyze a body of text you send me')

#get username
def getUsername():
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        #enter username
        inputPrompt = ''
        if attempts == 0:
            inputPrompt = '\nTo begin please, Enter your Username: \n'
        elif attempts == maxAttempts -1:
            inputPrompt = '\nFinal attempt, please try again: \n'
        else:
            inputPrompt = '\nPlease try again: \n'
        userNameFromInput =input(inputPrompt)

        #Validating Username

        if  (len(userNameFromInput) < 5 or not userNameFromInput.isidentifier()):
            print('Your username has to be greater than 5 character, alphanumeric and not contain spaces')
            
        else:
            return userNameFromInput
        attempts += 1
    print("Maximum attempt exhausted, Assigning a default Username....")

    return generate_username()[0]

# get text from file
def gettextfromfile():
    f = open('files/article.txt', 'r')
    rawText = f.read()
    f.close()
    
    return rawText.replace('\n', ' ').replace('\r', '')

username = getUsername()

#greet the users
def greetUser(name):
    print('Welcome, ' + name)

greetUser(username)

articletextRaw = gettextfromfile()
print(articletextRaw)