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

#THIS TIME, THE NEXT FOUR SETS EXCLUDE THE CONFIDENCE OF INTENT. IT IS STORED SEPARATELY IN RESULTINTENTS'S TUPLES ITSELF.'
#SO, NEXT FOUR PAPAARRAYS STORE CONS OF ENTITIES ONLY.

netmeanset = [] #LIST OF MEAN CONFIDENCE OF EACH QUERY'
netstdset = [] #LIST OF STD DEV OF EACH QUERY
Maxconset = [] #LIST OF MAXIMUM CONFIDENCE OF EACH QUERY
Minconset = [] #LIST OF MINIMUM CONFIDENCE OF EACH QUERY




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

queriesencoded = []

for query in queries:
    queriesencoded.append(urllib.quote(query, safe=''))
    #dot will appear as in encoded string but it's no problem
    #because even wit's encoder does the same

print ("brock")

print queriesencoded


###############################################################################

for queryencoded in queriesencoded:

    r=requests.get("https://api.projectoxford.ai/luis/v2.0/apps/af8d83d7-4468-4918-91ce-2a644d8259e7?subscription-key=c68ad8b1a9e64418b6e2b4485de03ba2&q="+queryencoded, )
    print r.text

    #dump r.text to dump.txt
    with open("dump.txt", "a") as myfile:
        myfile.write(r.text+",")

    #parse r.text json object
    jsn = json.loads(r.text) #jsn is a dictionary haivng 2 keys - _text and entities. Ideally we should now loop over it, but since only 2 keys, no need to loop

    print r.status_code
    RESPONSE.append(r.status_code)

    ###r_text i.e. LUIS's response is a json object having 4 keys - query, topScoringIntent, intents, entities
    ###WE SHALL HANDLE THEM ONE BY ONE'

    if 'entities' in jsn: #handling the netities key
        #entities is an array of json objects, each json object for 1 entity detected
        ents = jsn['entities'] #now ents is just an array of json objects

        en=''
        con=''
        val=''
        conarray = [] #list of 3-4 ocnfidences of this query. Will help us calculate mean confidence of THIS QUERY and append it to netmeanset
        qRESULTENTITIES=[] #for a single query, it stores all the (result entity, result value) tuples # added in PHASE 2
        qLOLOTrevc=[]

        #we loop through the ents array
        for jobj in ents:
            #jobj is a json object representing 1 detected entity. It is also a dictionary. 5 keys - entity, type, startindex, endindex, score
            en=str(jobj['type']).strip()
            val=str(jobj['entity']).strip()
            con=(jobj['score'])
            conarray.append(con)


            qRESULTENTITIES.append((en,val))
            qLOLOTrevc.append((en,val,con))

        #ALPHAMARKER
        #here we have the opportunity of finding mean confidence and standard deviation for THIS QUERY using conarray
        #our conarray hs now been built. Calculate mean confidence and standard deviation FOR THIS QUERY
        mean=None
        std=None
        maxcon=None
        mincon=None

        if len(conarray)!=0:
            mean = numpy.mean(conarray)
        print mean
        netmeanset.append(mean)
        if len(conarray)!=0:
            std = numpy.std(conarray)
        print std
        netstdset.append(std)
        if len(conarray)!=0:
            maxcon = numpy.amax(conarray)
        print maxcon
        Maxconset.append(maxcon)
        if len(conarray)!=0:
            mincon = numpy.amin(conarray)
        print mincon
        Minconset.append(mincon)



        RESULTENTITIES.append(qRESULTENTITIES) #ADDED IN PHASE 2, building RESULTENTITIES superlist
        LOLOTrevc.append(qLOLOTrevc)




    if 'topScoringIntent' in jsn: #handling the topScoringIntent key

        #this key contains a json object having 2 keys - intent and score
        ints = jsn['topScoringIntent'] #now ints is just a json object with 2 keys

        intnt=''
        con=''
        val=''

        qRESULTINTENTS=[] #LOT [(,)] of intent,value tuples - to be finally appended to RESULTINTENTS LOLOT
        qLOLOTrivc=[]     #LOT [(,,)] of intent,value,confidence tuples - to be finally appended to LOLOTrivc LOLOT


        intnt="intent"
        val=str(ints['intent']).strip()
        con=str(ints['score']).strip()

        print ("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"+val)

        qRESULTINTENTS.append((intnt,val))
        qLOLOTrivc.append((intnt,val,con))



        RESULTINTENTS.append(qRESULTINTENTS)
        LOLOTrivc.append(qLOLOTrivc)


#NOW WE SHOULD HAVE RESULTINTENTS AND LOLOTrivc
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print ENTITIES
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print RESULTENTITIES
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print LOLOTrevc


print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print INTENTS
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print RESULTINTENTS
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print LOLOTrivc

print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print Maxconset
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print Minconset
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
print netmeanset


#########################################################################################








