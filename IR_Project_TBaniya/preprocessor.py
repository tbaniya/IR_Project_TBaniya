import os
from os import path
import re
from nltk.stem import PorterStemmer
from tokenCounter import *

file1 = open('stop-words.txt','r')
text = file1.read()
file1.close()
text = text.replace('\n', ' ')
stopwords = set(text.split(" "))

# using porterStemmer to remove morphological variations
stemmer = PorterStemmer()

def findLink(file):
    f = open(file,'r')
    lines = f.readlines()[:1]
    return lines[0]
    
def readWordsinFile(file):
    wordlist = []
    for i in range(1):
            file.readline()
    for line in file:
        line = re.sub('<.*?>', '', line)
        # the regular expression removes puntuation, and converts to lowercase
        words = re.findall('[a-z]+',line.lower())
        wordlist.extend(words)
    return wordlist
 
# reads each file in loop , preprocessed it and stored the result in files
# 'processedFiles' is the directory to stored all preprossed files
def processfile(objfile):

    firstline = ""
    body = ""

    return firstline, body


def preprocess(filepath):
    n = 1
    filelist = []
    fileid = -1
    filelist = os.listdir(filepath)
    for filename in filelist:
        if filename.endswith('.txt'): 
            fileid += 1
            #file = open(filepath +filename,'r',encoding="utf8")
            file = open(filepath + filename,'r')
            print("Now processing:    " + filename)
            #count the total tokens of each file and only process file with > 50 tokens
            file_length = countTokens(filepath + filename)
            if file_length > 50:
                wordlist = readWordsinFile(file)
                tmp_file = open("processedFiles/"+"Doc-"+str(n) + ".txt",'w')
                n += 1
                #wrie link to page on first line of each page
                tmp_file.write(findLink(filepath + filename))
                #tmp_file.write("\n")
                for word in wordlist:
                    if word not in stopwords:
                        if len(word)> 2:
                            # using porter stemmer to stem word
                            word = stemmer.stem(word)
                            tmp_file.write(word + " ")
                            tmp_file.write("\n")
                tmp_file.flush()
                tmp_file.close()
            file.close()       
    print("Successully preprocessed all files")


# The input files are stored at dirctory 'collection'   
filepath = "./collection/"
preprocess(filepath)
