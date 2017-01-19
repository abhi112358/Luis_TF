import urllib
import requests
import json
import csv
import numpy


queries = []
RESPONSE = []

ENTITIES = []
RESULTENTITIES = []  #list of list of tuples of result entities # ENTITIES AND RESULTENTITIES will be finally compared in integrated file # ADDED IN PHASE 2
LOLOTrevc = []
INTENTS = []
RESULTINTENTS = []
LOLOTrivc = []


##################################################################################################################


#MODULE FOR INPUTTING 3 LINES IN 1 ITERATION

f = open('queries.txt', 'r')
## Read the first line
line = f.readline().rstrip()




## If the file is not empty keep reading line one at a time
## till the file is empty
while line:

#    print line
    queries.append(line)

    line=f.readline().rstrip()
#    print line
    qENTITIES=[]
    jsn = json.loads(line)
    for key, value in jsn.iteritems():#key is a string and entity is a list of strings
        for bro in value:
            tup = (key,bro)
            qENTITIES.append(tup)
    ENTITIES.append(qENTITIES)


    line=f.readline().rstrip()
#    print line
    qINTENTS=[]
    jsn = json.loads(line)
    for key, value in jsn.iteritems():#key is a string and entity is a list of strings
        for bro in value:
            tup = (key,bro)
            qINTENTS.append(tup)
    INTENTS.append(qINTENTS)


    line=f.readline().rstrip()




print queries
print ENTITIES
print INTENTS

###############################################################################