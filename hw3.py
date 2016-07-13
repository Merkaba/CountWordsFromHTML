# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 15:57:56 2016
Using Python 3.5

@author:  Flavio Bayer X0947373
Kevin Ho 30441608
Lance Lee 75935072
Munish Juneja 82377245

"""

import json
import string
import time
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk import FreqDist

'''
This requires NLTK and BeautifulSoup. BeautifulSoup is used for scrubbing the
HTML markup from the files and getting plaintext. This is inherent in my IDE
(anaconda) but you may need to download it! 
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
From NLTK debug info:
"To remove HTML markup, use BeautifulSoup's get_text() function."

NLTK is used for Frequency Distributions
https://blogs.princeton.edu/etc/files/2014/03/Text-Analysis-with-NLTK-Cheatsheet.pdf
'''

'''
TODO:
most likely have to bake the totalWordDict into a class so we can have
both the frequency per page AND total frequency. right now it's too messy. this
is super easy to implement but i didnt do it yet

need to write the totalWordFreq to disk
need to time how long we took to make the index
'''

class freqDict:
    def __init__(self):
        '''
        index is the mapping of words to tuple of (websiteID, freq on website)
        freqCount is the mapping of words to int of their total frequency
        '''
        
        self.index = defaultdict(list)
        self.freqCount = defaultdict(int)
        self.docMapping = dict()        
        
    def addDict(self, smallIndex):
        for each in smallIndex.items():
            self.index[each[0]].extend(each[1])
            for eachTuple in each[1]:
                self.freqCount[each[0]] += eachTuple[1]
    
    def addMapping(self, docIDPair):
        self.docMapping[docIDPair[0]]=docIDPair[1]
        
        
def loadJson(filename):

    with open(filename+"\html_test.json") as dataset:
        return json.loads(dataset.read())

def processData(path, jsonDict, writeToFile = 0, maxFiles = 0):
    '''
    Usage:
    
    Path: the folder ABOVE /html, which you used for loadJson
    jsonDict: the json dict from loadJson
    writeToFile: writes RAW DATA to file under the name "data.txt". optional arg
    maxFiles: max "good" files to try up to. good for debugging    
    
    returns a dict of words 
    '''
    counter = 0 #number of files read so far
    unparsed = 0 #number of files failed to read
    uniqueWords = 0
    
    '''
    I use list for the defaultdict instead of int or tuple because I want to
    keep track of the wordcount ASSOCIATED to each file. so it will be a list
    of tuples of the format [(websiteID, freq)...]
    
    so defaultdict is of the form
    KEY: word
    VALUE: list of tuples, of the format (websiteID, frequency in this file)
    '''
    totalWordDict = defaultdict(list) #this is wordDict across ALL files
    
    indexer = freqDict()
    
    if(writeToFile == 1):
            f = open(path + '\data.txt', 'w', encoding='utf-8')

    for jsonData in jsonDict.items():
        #print(path+"\Html\\"+ fileName["file"])
        try:    
            file = open(path+"\Html\\"+ jsonData[1]["file"], encoding='utf-8').read()
            counter+=1
            #print(path+"\Html\\"+ jsonData[1]["file"])
            indexer.addMapping((jsonData[0], jsonData[1]["url"]))
            
        except Exception as e:
            print(e)
            unparsed +=1            
            continue           

        
        
        scrubbed = BeautifulSoup(file, "lxml").get_text().lower()

        goodChars = string.ascii_letters + string.digits
        textHolder = ""
        '''this probably would have been easier with Regular Expressions..'''
        for each in scrubbed: #each is each CHAR in the scrubbed HTML file
            if each in (string.whitespace + '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'):
                textHolder += " " #need this to change newline to a space, etc
            elif each == "'":
                continue #need this to specifically remove apostraphes 
            elif each in goodChars: #also gets rid of weird characters
                textHolder += each
                
        #textHolder = (textHolder + "\n\n\n\n\n").encode(sys.stdout.encoding, errors='replace').decode()
        if(writeToFile == 1):        
            f.write(jsonData[1]["url"] + "\n")
            f.write(textHolder + "\n\n\n")
                     
        
        '''
        examples of FreqDist:
        
        >>> print(fdist1)
        <FreqDist with 19317 samples and 260819 outcomes>
        >>> fdist1.most_common(50)
        [(',', 18713), ('the', 13721), ('.', 6862), ('of', 6536), ('and', 6024),
        ('a', 4569), ('to', 4542), (';', 4072), ('in', 3916), ('that', 2982),
        ("'", 2684), ('-', 2552), ('his', 2459), ('it', 2209), ('I', 2124),
        ('s', 1739), ('is', 1695), ('he', 1661), ('with', 1659), ('was', 1632),
        ('as', 1620), ('"', 1478), ('all', 1462), ('for', 1414), ('this', 1280),
        ('!', 1269), ('at', 1231), ('by', 1137), ('but', 1113), ('not', 1103),
        ('--', 1070), ('him', 1058), ('from', 1052), ('be', 1030), ('on', 1005),
        ('so', 918), ('whale', 906), ('one', 889), ('you', 841), ('had', 767),
        ('have', 760), ('there', 715), ('But', 705), ('or', 697), ('were', 680),
        ('now', 646), ('which', 640), ('?', 637), ('me', 627), ('like', 624)]
        >>> fdist1['whale']
        906
        
        '''
        fdist = FreqDist(textHolder.split())
        #print(fdist.most_common())
        #print(fdist.items())
        for each in fdist.items():
            if each[0] not in totalWordDict:
                uniqueWords +=1
            '''
            each[0] is the word found, each[1] is the freq
            we're appending a tuple of the website it appeared on and how
            many times it appeared
            '''
            #print(each)
            totalWordDict[each[0]].append((jsonData[0], each[1]))
            
        
        if counter >= maxFiles and maxFiles != 0:
            print("Reached Max Files\n")
            break
        if counter%100 == 0:
            print("Files Completed: " + str(counter))             
    
    print("\n-----------------------------------------------")
    print("Total number of files processed: " + str(counter))
    print("Number of files unable to be parsed: " + str(unparsed))
    print("Unique Words: " + str(uniqueWords))
    print("-----------------------------------------------\n")

    indexer.addDict(totalWordDict)

    
    return indexer

def writeIndexToFile(path, indexer):
    try:
        f = open(path + '\data.txt', 'w', encoding='utf-8')
    except Exception as e:
        print(e)
        return
    
    f.write("Index items\n")
    f.write("-----------------------------------------------\n")
    f.write(str(indexer.index.items()))
    f.write("\n-----------------------------------------------\n\n")

    f.write("Frequency\n")
    f.write("-----------------------------------------------\n")
    f.write(str(indexer.freqCount.items()))
    f.write("\n-----------------------------------------------\n\n")
    
    
    f.write("Document Mapping\n")
    f.write("-----------------------------------------------\n")
    f.write(str(indexer.docMapping.items()))
    f.write("\n-----------------------------------------------\n\n")
    
if __name__ == "__main__":
    path = "D:\workspace\class121\hw3"
    print("Starting to load Json....")
    timer = time.time()
    jsonDict = loadJson(path)
    indexer = processData(path, jsonDict, maxFiles = 1)
    print("Total time taken: {0:.2f} seconds".format(time.time() - timer))
    
    writeIndexToFile(path, indexer)
    print("Size of Index (with Document Map and Frequency Count): {0:.2f}KB"\
    .format(os.path.getsize(path + '\data.txt')/1024))
    
    
    #print("Len of totalWordDict: " + str(len(indexer.index)))    
#    print([x for x in indexer.index.items()][:10])
#    print([x for x in indexer.docMapping.items()][:10])
#    print([x for x in indexer.freqCount.items()][:10])
#
#counter = 0
#for each in jsonDict.items():
#    print(each)
#    counter+=1
#    if counter == 20:
#        break
#


