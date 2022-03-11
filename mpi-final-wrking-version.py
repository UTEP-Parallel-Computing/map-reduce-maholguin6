#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:36:35 2022

@author: general
"""

import new, time

from mpi4py import MPI


filesToRead = ['files/shakespeare1.txt','files/shakespeare2.txt',
                  'files/shakespeare3.txt','files/shakespeare4.txt',
                  'files/shakespeare5.txt','files/shakespeare6.txt',
                  'files/shakespeare7.txt','files/shakespeare8.txt']


def displayArray( array ):
    for k,v in array.items():
        print(f'{k} {v}')

def updateDict(shared, local):
    for key in local:
        if key in shared:
            shared[key] += local[key]
        else: 
            shared[key] = local[key]

# get the world communicator
comm = MPI.COMM_WORLD
# get our rank (process #)
rank = comm.Get_rank()
# get the size of the communicator in # processes
size = comm.Get_size()

localList = []
tmp = new.wordCount()
globalDict = {}

docsPerThread = len(filesToRead) / size

for process in range(0, size):
    #start and end of slice we're sending
    startOfSlice = int( docsPerThread * process )
    endOfSlice = int( docsPerThread * (process + 1) )
    sliceToSend = filesToRead[startOfSlice:endOfSlice]
    
    comm.send(sliceToSend, dest=process, tag=0)

start = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )

if rank == 0:
    localDict = {}
    recv_list = comm.recv(source=0, tag=0)
    for index in recv_list:
        local = tmp.find(tmp.lowerCase(tmp.openFile(index)))
        updateDict(localDict, local)

    for process in range(1,size):
        loca_recv = comm.recv(source=process, tag=1)
        updateDict(localDict, loca_recv)
else:
    localDict = {}
    recv_list = comm.recv(source=0, tag=0)
    for index in recv_list:
        local = tmp.find(tmp.lowerCase(tmp.openFile(index)))
        updateDict(localDict, local)
    comm.send(localDict, dest=0, tag = 1)

end = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
print(f'total time: {end - start}')
tmp.writeToFile('mpi-output.txt', localDict)
print(localDict)
