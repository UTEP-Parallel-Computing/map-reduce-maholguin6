#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:28:30 2022

@author: general
"""

import re
import pymp
import time

FILES = ('shakespeare1.txt', 'shakespeare2.txt', 'shakespeare3.txt',
        'shakespeare4.txt', 'shakespeare5.txt', 'shakespeare6.txt',
        'shakespeare7.txt' ,'shakespeare8.txt')

WORDS = ('hate', 'love', 'death', 'night', 'sleep', 'time', 'henry', 'hamlet',
        'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart', 'honest')

def words_in_file(word, file):
    count = 0
    with open(file, 'r') as f:
        for line in f:
            count += len(re.findall(word, line, re.IGNORECASE))
    return count

def main(thread_num = 1):
    global_result = pymp.shared.dict()
    for word in WORDS:
        global_result[word] = 0

    #splittings
    with pymp.Parallel(thread_num) as p:
        local_result = dict()
        for word in WORDS:
            local_result[word] = 0

        #mapping
        for i in p.range(len(FILES)):
            for word in WORDS:
                local_result[word] += words_in_file(word, FILES[i])

        #shuffling
        lock = p.lock
        for word in WORDS:
            lock.acquire()
            global_result[word] += local_result[word]
            lock.release()

    print(global_result)


durations = []
threads = []
for i in range(1, 17):
    time1 = time.time()
    main(i)
    time2 = time.time()
    duration = time2 - time1
    print('duration:', duration)
    print('thread_num:', i)
    durations.append(duration)
    threads.append(i)

print(durations)
print(threads)
