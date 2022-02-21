#!/usr/bin/env python3

import sys, os, re




def tofile(output, result):
    """
    Writes  result to file
    """

    with open(output, "w") as file:
        for k,v in result.items():
            file.write("{} {}\n".format(k,v))


def arrange(a):
    """
    Arrange Dictionary alphabetically
    """

    tmp = {}
    for i in sorted(a):
        tmp[i] = a[i]
    return tmp


def package():
    files = []
    directory = '<folder>'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            if '.txt' in f:
                files.append(f)
    return files
            
def cleanify(filename):
    """
    Clean textfile and save it in a Dictionary
    """
    wanted = ['hate','love','death','night',
              'sleep','time','henry','hamlet',
              'you','my','blood','poison',
              'macbeth','king','heart','honest']
    result = {}
    unwanted = '[\W]'
    files = package()

    for file in files:
        with open(file, "r") as text:
            for line in text:
                line1 = line.lower()
                line = re.sub(unwanted, ' ', line1)
                for i in wanted:
                    if i in line:
                        if i not in result:
                            result[i] = 1
                        else:
                            result[i] += 1
        
    return result

#I/O filenames extracted from sys argv
files = package()
fromFile = files
toFile = 'output'

for i in files:
    t = cleanify(i)
    result = arrange(t)
print(result)
    
tofile(toFile, result)




