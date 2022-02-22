#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:38:18 2022

@author: general
"""
import time, pymp, re, os, sys

def dictOfItems(itemsToIterate=[]):
    # create a shared dict
    sharedDict = pymp.shared.dict()
    

    with pymp.Parallel() as p:
        listOfItems = []
        sumLock = p.lock
 
        # iterate over the list of items
        for item in p.iterate(itemsToIterate):
            # for each item take that item and
            # add thread_num of these to the dict
            
            listOfItems.append(item * p.thread_num)
            
        # add the list to the dict
        sumLock.acquire()
        sharedDict[p.thread_num] = listOfItems
        sumLock.release()
    return sharedDict





sum[0] = sum[0] + 1

# removing just the release will result in
# deadlock
sumLock.release()
