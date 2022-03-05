#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:38:18 2022

@author: general
"""
import time, re, os, sys
from mpi4py import MPI





            
# simple example to show sending and receiving messages

# get the world communicator
comm = MPI.COMM_WORLD

# get our rank (process #)
rank = comm.Get_rank()

# get the size of the communicator in # processes
size = comm.Get_size()


globalListOfDocs = ['shakespeare1.txt','shakespeare2.txt',
                  'shakespeare3.txt','shakespeare4.txt',
                  'shakespeare5.txt','shakespeare6.txt',
                  'shakespeare7.txt','shakespeare8.txt']


listOfWords = ['hate','love','death','night',
          'sleep','time','henry','hamlet',
          'you','my','blood','poison',
          'macbeth','king','heart','honest']
numCount = {}
for i in listOfWords:
    numCount[i] = 0

localList = []
localDict = {}
def operation(items):
    unwanted = '[\W]'
    start = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
    for item in items:
        with open(item, 'r') as text:
            for line in text:
                line1 = line.lower()
                line = re.sub(unwanted, ' ', line1)
                for i in listOfWords:
                    if i in line:
                        if i in localDict:
                            localDict[i] += 1
                        else:
                            localDict[i] = 1
        end = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
        total = end - start
    return localDict, total
    


# thread 0 distributes the work
if rank == 0:
    print('Thread 0 distributing')

    docsPerThread = len(globalListOfDocs) / size

    # first setup thread 0s slice of the list
    localList = globalListOfDocs[:int( docsPerThread )]

    for process in range(1, size):
        #start and end of slice we're sending
        startOfSlice = int( docsPerThread * process )
        endOfSlice = int( docsPerThread * (process + 1) )

        sliceToSend = globalListOfDocs[startOfSlice:endOfSlice]
        comm.send(sliceToSend, dest=process, tag=0)
#everyone else receives that message
else:
    # receive a message from thread 0 with tag of 0
    localList = comm.recv(source=0, tag=0)
    comm.send(operation(localList), dest=0, tag=0)
    
    
if rank == 0:
    for process in range(1,size):
        localDict, total = comm.recv(source=process, tag=0)
        for name, value in localDict.items():
            numCount[name] += value
        print(f'Thread {rank} has {localDict} total time:{total} ')
