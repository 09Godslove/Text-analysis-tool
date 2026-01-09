import base64
from io import BytesIO
from random_username.generate import generate_username
import re, nltk, json
from nltk.corpus import wordnet as wn, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from wordcloud import WordCloud
stopWords = set(stopwords.words('english'))
wordLamentizer = WordNetLemmatizer()
sentimentAnalyzer = SentimentIntensityAnalyzer()

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

# pos dictionary
postowordtag = {
    'J': wn.ADJ,
    'V': wn.VERB,
    'R': wn.ADV,
    'N': wn.NOUN
}
# convert treebank part of speech to wordnet part of speech
def treeBankPOStoWordnetPos(partOfSpech):
    """
    Map NLTK POS tags to WordNet POS tags for lemmatization.
    """
    POSsartwith = partOfSpech[0]
    if POSsartwith in postowordtag:
        return postowordtag[POSsartwith]
    return wn.NOUN

# filter tockinize words to only include actual words
def getWordsCleaned(POSWordTupes):
    cleansedList = []
    mathcedWordsPattern = '[^a-zA-z-+—]'
    for POSWordTuple in POSWordTupes:
        word = POSWordTuple[0]
        pos = POSWordTuple[1]
        cleansedword = word.replace('.', '').lower() 
        if ( not re.search(mathcedWordsPattern, cleansedword)) and len(cleansedword) > 1 and cleansedword not in stopWords:
            cleansedList.append(wordLamentizer.lemmatize(cleansedword,treeBankPOStoWordnetPos(pos)))
    return cleansedList


#Get text from file
articletextRaw = gettextfromfile()

def analyzeAticle(articleTobeAnalyzed):

    #Tokenize text
    articleSentences = tokinizeArticle(articleTobeAnalyzed)
    articleWords = tokinizeWords(articleSentences)
    articleWordsPOStag = nltk.pos_tag(articleWords)

    # get sentence analytics
    searchPattern = '[0-9]|[$%€£]|thousand|million|hundred|profit|loss'
    keySentences = getKeySentences(articleSentences, searchPattern)
    wordsPersentence = getWordsPerSentence(articleSentences)

    #get words analytics
    cleanedWordsList = getWordsCleaned(articleWordsPOStag)

    # Generate word cloud
    separator = ' '
    wordCloudPath = 'results/wordcloud.png'
    wordcloud = WordCloud(width = 1000, height = 200, 
                        background_color='grey', random_state = 1, colormap='Pastel1', collocations = False).generate(separator.join(cleanedWordsList))
    # wordcloud.to_file(wordCloudPath)
    img = wordcloud.to_image()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # find word sentiment
    sentimentResult = sentimentAnalyzer.polarity_scores(articleTobeAnalyzed)

    # collate analytics into one dictionary
    finalResult = {
        'data': {
            'KeySentences': keySentences,
            'Wordspersentences': round(wordsPersentence, 1),
            'sentiment': sentimentResult,
            'Word Cloud path': wordCloudPath,
            'EncodedWordcloud': img_base64
        },
        'metadata':{
            'TotalSentence': len(articleSentences),
            'TotalWords': len(cleanedWordsList)
        }
    }
    return finalResult

def runOnbegining():
        
    # greet the users
    username = getUsername()
    def greetUser(name):
        print('Welcome, ' + name)
    greetUser(username)