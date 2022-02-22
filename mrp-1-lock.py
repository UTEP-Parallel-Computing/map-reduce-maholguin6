#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:38:18 2022

@author: general
"""
import time, pymp, re, os, sys

itemsToIterate = [  'shakespeare1.txt',
                    'shakespeare2.txt',
                    'shakespeare3.txt',
                    'shakespeare4.txt',
                    'shakespeare5.txt',
                    'shakespeare6.txt',
                    'shakespeare7.txt',
                    'shakespeare8.txt']

sharedDict = pymp.shared.dict()
listOfItems = ['hate','love','death','night',
                'sleep','time','henry','hamlet',
                'you','blood','poison','macbeth',
                'king','heart','honest']

for i in listOfItems:
    if i not in sharedDict:
        sharedDict[i] = 1

def dictOfItems(listOfItems, itemsToIterate, sharedDict):
    # create a shared dict
    with pymp.Parallel() as p:
        sumLock = p.lock
        # iterate over the list of items
        start = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
        for item in p.iterate(itemsToIterate):
            with open(item, 'r') as text:
                for line in text:
                    for i in listOfItems:
                            if re.search(i, line, re.IGNORECASE):
                                sumLock.acquire()
                                sharedDict[i] += 1
                                sumLock.release()
           
         # add the list to the dict
        end = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
        completed = end - start
      
    return sharedDict, completed
   

dic, tim = dictOfItems(listOfItems, itemsToIterate, sharedDict)
print(f'dittionary: {dic}')
print(f'duration time: {tim}')

