from random_username.generate import generate_username
# import nltk
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import re

wordLamentizer = WordNetLemmatizer()

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

# Separate sentences
def tokinizeArticle(rawTest):
    return sent_tokenize(rawTest)

# sperate words
def tokinizeWords(sentence):
    listWord = []
    for sentences in sentence:
        listWord.extend(word_tokenize(sentences))
    return listWord

# get key sentences
def getKeySentences(sentences, patern):
    mathcedSentences = []
    for sentence in sentences:
        if re.search(patern, sentence.lower()):
            mathcedSentences.append(sentence)
    return mathcedSentences

# get the average words per sentence, excluding puct
def getWordsPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += (len(sentence.split(' ')))
    return totalWords/len(sentences)

# filter tockinize words to only include actual words
def getWordsCleaned(words):
    cleansedList = []
    mathcedWordsPattern = '[^a-zA-z-+—]'
    for word in words:
        cleansedword = word.replace('.', '').lower() 
        if ( not re.search(mathcedWordsPattern, cleansedword)) and len(cleansedword) > 1:
            cleansedList.append(wordLamentizer.lemmatize(cleansedword))
    return cleansedList

#greet the users
username = getUsername()
def greetUser(name):
    print('Welcome, ' + name)
greetUser(username)

#Get text from file
articletextRaw = gettextfromfile()

#Tokenize text
articleSentences = tokinizeArticle(articletextRaw)
articleWords = tokinizeWords(articleSentences)

# get sentence analytics
searchPattern = '[0-9]|[$%€£]|thousand|million|hundred|profit|loss'
keySentences = getKeySentences(articleSentences, searchPattern)
wordsPersentence = getWordsPerSentence(articleSentences)

#get words analytics
cleanedWordsList = getWordsCleaned(articleWords)

# print testing
print(cleanedWordsList)