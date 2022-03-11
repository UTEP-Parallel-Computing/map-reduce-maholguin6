#!/usr/bin/env python3

import sys, re, os
        
        
        
# filesToRead = ['files/shakespeare1.txt','files/shakespeare2.txt',
#                   'files/shakespeare3.txt','files/shakespeare4.txt',
#                   'files/shakespeare5.txt','files/shakespeare6.txt',
#                   'files/shakespeare7.txt','files/shakespeare8.txt']



class wordCount:
    
    def __init__(self):
        self.localArray = {}
        self.wordList = ["hate", "love", "death", "night", "sleep",
                         "time", "henry", "hamlet", "you", "my", "blood",
                         "poison", "macbeth", "king", "heart", "honest"]
        self.test = ['you']
    
    def openFile(self, filesToRead):
        return open(filesToRead, 'r').read().split()
    
    def lowerCase(self, listOfWords):
        lowerCaselist = []
        for word in listOfWords:
            lowerCaselist.append(word.lower())
        return lowerCaselist
    
    
    def reduce(self, newList):
        stripList = []
        for i in newList:
            stripList.append(re.sub(r'[^a-z]', ' ', i))
        return stripList
            
    
    def find(self, newList):
        result = {}
        for item in newList:
            for i in self.wordList:
                 if re.findall(i, item):
                    if i not in result:
                        result[i] = 1
                    else:
                        result[i] += 1
        return result
    
    
    def writeToFile(self, fileName, result):
        with open(fileName, "w") as file:
            for k,v in result.items():
                file.write("{} {}\n".format(k,v))
                
    
    def displayArray(self, array):
        for k,v in array.items():
            print(f'{k} {v}')
        
        
    def updateDict(self, shared, local):
        for key in local:
            if key in shared:
                shared[key] += local[key]
            else: 
                shared[key] = local[key]
