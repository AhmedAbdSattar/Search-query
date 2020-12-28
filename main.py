from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import os
import math
import sys
import re
import operator
from math import log
import glob


# function to read lines from file
def ReadFunc(path):
    filename = open(path, 'r')
    FileLines = filename.readline()
    filename.close()
    return FileLines


# Function to remove Punctiuations

def PuncFunc(FileLines):
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for word in FileLines:
        if word in punc:
            FileLines = FileLines.replace(word, " ")

    return FileLines


# Function to provide uniformity(lowerCase)

def UniformityFunc(FileLines):
    FileLines = FileLines.lower()
    return FileLines


# Function to tokinize and remove stop words

def tokenizeFunc(FileLines):
    text_tokens = word_tokenize(FileLines)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    return tokens_without_sw


path = 'textFile//'
Files = os.listdir(path)
wordsList = []
list_of_dict = []
list_oflists = []
count = 0
query = input("Enter query:")
queryList = tokenizeFunc(UniformityFunc(PuncFunc(query)))
input = queryList
for eachF in Files:
    with open(path + eachF) as f:
        line = f.readline()
        wordsList = tokenizeFunc(UniformityFunc(PuncFunc(line)))
        fileIndex = {}
        for index, word in enumerate(wordsList):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
    list_of_dict.append(fileIndex)
#print(list_of_dict)

for word_to_search in input:
    count = 0
    dict_of_lists = {}
    for i in range(len(Files)):
        dict_of_lists[i] = 0
    file_num = 0

    for file in list_of_dict:
        for key, value in file.items():
            if word_to_search == key:
                count += len(value)
                temp = value
                dict_of_lists[file_num] = temp
        file_num += 1

    print(word_to_search, " = ", count)
    i = 0
    for i in range(file_num):
        if dict_of_lists[i] == 0:
            continue
        else:
            print("D", i, dict_of_lists[i])
    print('---------------------')
def readfn(path):
    filename = open(path,'r')
    dataline=filename.readline()
    filename.close()
    return dataline
documents=[]
for i in glob.glob(r'textFile/*'):
     line =readfn(i) #read line from the file
     documents.append(line)
     text_tokens = word_tokenize(line) # take a list of words (tokens)
     StringOftokens =''
     for word in text_tokens:
        if not word in stopwords.words(): #remove stop words from list
             StringOftokens += word+' ' #add words to a string called string of tokens which tokens without stop words
#-------------------------------------------------------------
# ---------------------calc term freq-------------------------
#-------------------------------------------------------------

# 1-tokenize--------------------------------------------------
dictOfWord = {}
for index, sentance in enumerate(documents):
    tokenizedWords = sentance.split(' ')
    dictOfWord[index] = [(word,tokenizedWords.count(word)) for word in tokenizedWords]
   # print (dictOfWord[index])
# 2-remove deblicate------------------------------------------
termFreqency = {}

for i in range(0, len(documents)) :
    UndeblicateList = []
    for wordfreq in dictOfWord[i] :
        if wordfreq not in UndeblicateList :
            UndeblicateList.append(wordfreq)
            termFreqency[i] = UndeblicateList
#print(termFreqency)                   #remove # to show it يسطا

# 3-normalize freqency-----------------------------------------
normalizeTermfrequency = {}
for i in range(0, len(documents)):
    sentance = dictOfWord[i]
    LenOfSentance = len(sentance)
    listOfNormalized = []
    for wordfreq in termFreqency[i] :
        normalizedfrequency = wordfreq[1]/LenOfSentance
        listOfNormalized.append((wordfreq[0], normalizedfrequency))
    normalizeTermfrequency[i] = listOfNormalized
#print(normalizeTermfrequency)            #remove # to show it يسطا


#-----------------------------------------------------------------
# -------------calc Inverse Document Frequency--------------------
#-----------------------------------------------------------------

# 1-put all sentance together and tokanze words-------------------
allDoc =  ''
for sentance in documents :
    allDoc += sentance + ' '
allDocTokenised = allDoc.split(' ')
#print(allDocTokenised)                  #remove # to show it يسطا

allDocNonDeplicated =[]
for word in allDocTokenised:
    if word not in allDocNonDeplicated:
         allDocNonDeplicated.append(word)
#print(allDocNonDeplicated)              #remove # to show it يسطا

# 2-calc all docs where term T appear------------------------------
dictOfNumOfDocWithTermInside = {}
for index, vec in enumerate(allDocNonDeplicated):
    count = 0
    for sentance in documents :
        if vec in sentance :
            count += 1
        dictOfNumOfDocWithTermInside[index] = (vec,count)
#print(dictOfNumOfDocWithTermInside)    #remove # to show it يسطا


#--------------------------------------------------------------------
#---------------------------calc IDF---------------------------------
#--------------------------------------------------------------------
dictOfIDFNonDeplicted = {}
for i in range(0, len(normalizeTermfrequency)) :
    IDF = []
    for word in normalizeTermfrequency[i] :
        for x in range (0, len(dictOfNumOfDocWithTermInside)) :
            if word[0] == dictOfNumOfDocWithTermInside[x][0] :
                IDF.append((word[0],math.log(len(documents)/dictOfNumOfDocWithTermInside[x][1])))
    dictOfIDFNonDeplicted[i] = IDF
#print(dictOfIDFNonDeplicted)           #remove # to show it يسطا


#--------------------------------------------------------------------
#---------------------calc DF-IDF = DF*IDF---------------------------
#--------------------------------------------------------------------

dictOfTF_IDF = {}
for i in range (0, len(normalizeTermfrequency)) :
    listOfTF_IDF = []
    TFsentance = normalizeTermfrequency[i]
    IDFsentance = dictOfIDFNonDeplicted[i]
    for x in range (0, len(TFsentance)) :
        listOfTF_IDF.append((TFsentance[x][0],TFsentance[x][1]*IDFsentance[x][1]))
    dictOfTF_IDF[i] = listOfTF_IDF

print("TF_IDF =",dictOfTF_IDF)

# similarity
from difflib import SequenceMatcher
with open('textFile/New York.txt', errors='ignore') as file_1,open('textFile/London.txt', errors='ignore') as file_2:
    file_1_data = file_1.read()
    file_2_data = file_2.read()
    similarity = SequenceMatcher(None, file_1_data,file_2_data).ratio()
    print("similarity between files  ",file_1.name,"and",file_2.name,"=",similarity*100)
