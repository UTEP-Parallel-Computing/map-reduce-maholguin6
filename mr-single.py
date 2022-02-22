#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:38:18 2022

@author: general
"""
import time, pymp, re, os, sys

itemsToIterate = ['shakespeare1.txt','shakespeare2.txt','shakespeare3.txt','shakespeare4.txt','shakespeare5.txt','shakespeare6.txt','shakespeare7.txt','shakespeare8.txt']

def dictOfItems(itemsToIterate=[]):
    # create a shared dict
    sharedDict = {}
    listOfItems = ['hate','love','death','night',
              'sleep','time','henry','hamlet',
              'you','my','blood','poison',
              'macbeth','king','heart','honest']
    
    for i in listOfItems:
        if i not in sharedDict:
            sharedDict[i] = 1

    with pymp.Parallel() as p:
        
        

        unwanted = '[\W]'
        # iterate over the list of items
        start = time.clock_gettime( time.CLOCK_PROCESS_CPUTIME_ID )
        for item in itemsToIterate:
            #print('inside first loop')
            # for each item take that item and
            # add thread_num of these to the dict
            with open(item, 'r') as text:
                for line in text:
                    line1 = line.lower()
                    line = re.sub(unwanted, ' ', line1)
                    for i in listOfItems:
                        if i in line:
                            sharedDict[i] += 1
            
        # add the list to the dict
        end = time.clock_gettime( time.CLOCK_PROCESS_CPUTIME_ID )
        completed = end - start
       
    return sharedDict, completed
    

dic, tim = dictOfItems(itemsToIterate)
print(f'dittionary: {dic}')
print(f'duration time: {tim}')

