"""
3 MAIN PAPA ARRAYS IN WIT'S TESTING FRAMEWORK WERE -

ENTITIES		a.k.a LOLOTev		= LOLOT(entities,values)
RESULTENTITIES		a.k.a LOLOTrev		= LOLOT(resultentities,resultvalues)
LOLOTrevc					= LOLOT(resultentities,resultvalues,resultconfidence)

In LUIS, entities and intents are treated differently, so we will have to replace these 3 by 6 papa arrays
Also, in LUIS, confidence is called score. But for ease of use, we'll still denote it by c

INTENTS			a.k.a LOLOTev		= LOLOT(intents,values)  #technically there can will be only 1 intent, but we still define it as a json obj in input file
RESULTINTENTS		a.k.a LOLOTrev		= LOLOT(resultintents,resultvalues)   #in verbose mode, LUIS retursn an array of multiple itntes detected, but we don't need that. We'll just store the top scoring intent
LOLOTrivc					= LOLOT(resultintents,resultvalues,resultconfidence)
ENTITIES		a.k.a LOLOTev		= LOLOT(entities,values)
RESULTENTITIES		a.k.a LOLOTrev		= LOLOT(resultentities,resultvalues)
LOLOTrevc					= LOLOT(resultentities,resultvalues,resultconfidence)

ALSO, sice entire csv can be regenerated using PAPA ARRAYS, this gives us a wonderful opportunity to not do the hodge podge we made in the middle of Wit's code

"""
########################################################################################################

#THIS FILE ADDS 2 NEW PAPA ARRAYS
#Maxconset - List of Maximum confidences of each query
#Minconset - List of Minimum confidences of each query


########################################################################################################


#THIS FILE ADDS 3 NEW PAPA ARRAYS after comparing RESULTENTITIES AND ENTITIES (now there are total 10 papa arrays)
#Matchedentities - List of entities in RESULTENTITIES that are also in ENTITIES
#Overmatchedentities - List of entities in RESULTENTITIES that are not in ENTITIES, i.e. extra!!!
#Totalentities - List of totalcorrectentities in handgenerated entity set

########################################################################################################

#TARGET - Each module should give an independed test that represents a column of the matrix
#I AFFECTIONATELY CALL THEM PAPA ARRAYS
#LISTS REQUIRED TO BE EXTRACTED - queries, RESPONSE, Confidence, Standard Deviation,

#RESULTENTITIES - LOLOT(resultentity,resultvalue) - CODENAME  LOLOTrev
#ENTITIES - LOLOT(entity,value) of input file calculated manually - CODENAME LOLOTev

#LOLOTrevc - LOLOT(resultentity,resultvalue,resultconfidence) of resulting data - CODENAME LOLOTrevc

##LOLOT = LIST OF LIST OF TUPLES

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


queriesencoded = []

for query in queries:
    queriesencoded.append(urllib.quote(query, safe=''))
    #dot will appear as in encoded string but it's no problem
    #because even wit's encoder does the same

print ("brock")

print queriesencoded


###############################################################################

matrix = []
row = ["QUERY","RESPONSE STATUS" , "QUERY'S MEAN 'CONFIDENCE" , "QUERY'S 'STANDARD DEVIATION" , "RECOGNIZED ENTITIES"]
matrix.append(row)
row=[]
matrix.append(row)

netmeanset = [] #LIST OF MEAN CONFIDENCE OF EACH QUERY'
netstdset = [] #LIST OF STD DEV OF EACH QUERY
Maxconset = [] #LIST OF MAXIMUM CONFIDENCE OF EACH QUERY
Minconset = [] #LIST OF MINIMUM CONFIDENCE OF EACH QUERY


for queryencoded in queriesencoded:
    row = []
    r=requests.get("https://api.wit.ai/message?v=20170111&q="+queryencoded, headers={"Authorization":"Bearer QWRFP44Y7XSF3LNVOARB4RGLVCGHZSWH"})
    print r.text

    #dump r.text to dump.txt
    with open("dump.txt", "a") as myfile:
        myfile.write(r.text+",")

    #parse r.text json object
    jsn = json.loads(r.text) #jsn is a dictionary haivng 2 keys - _text and entities. Ideally we should now loop over it, but since only 2 keys, no need to loop
    message = jsn['_text']  #handling the first key
    row.append(message)

    print r.status_code
    row.append(r.status_code)
    RESPONSE.append(r.status_code)


    if 'entities' in jsn: #handling the second key
        ents = jsn['entities'] #now ents is just a json object which means that it is also a dictionary'. But this time, we don't know in advance how many key value pairs are there. So we will loop over this dictionary''
        en=''
        con=''
        val=''
        conarray = [] #list of 3-4 ocnfidences of this query. Will help us calculate mean confidence of THIS QUERY and append it to netmeanset
        rowofentities = [] # we first build a subrow of all (entity,value:confidence) for this query. It's called rowofentities. ' Once it's completely built, we iterate over it' and add each element to our parent row list at STEP-YODA

        qRESULTENTITIES=[] #for a single query, it stores all the (result entity, result value) tuples # added in PHASE 2
        qLOLOTrevc=[]

        for key, value in ents.iteritems(): #that's how you loop over a dictionary'
            #now value is an array. for example in the response, (value=)intent is an array OF 1 JSON OBJECT (WHICH IS A DICTIONARY )HAVING 2 or 3 KEY VALUE PAIRS (confidence, type  a third key - value might also be present)
            print key
            en=str(key).strip()
            for key1, value1 in value[0].iteritems(): #why value[0]? because value was an array of 1 json object
                print (key1+':'+str(value1))
                if key1=='confidence':
                    con=value1
                    conarray.append(con)
                elif key1=='value':
                    val=str(value1).strip()



            #append all these values to rowofentities list which will be appended to row list later on in STEP-YODA

            rowofentities.append("("+en+", "+str(val)+") : "+str(con))
            qRESULTENTITIES.append((en,str(val)))
            qLOLOTrevc.append((en,str(val),str(con)))

        #here we have the opportunity of finding mean confidence and standard deviation for THIS QUERY using conarray
        #our conarray hs now been built. Calculate mean confidence and standard deviation FOR THIS QUERY
        mean = numpy.mean(conarray)
        print mean
        netmeanset.append(mean)
        std = numpy.std(conarray)
        print std
        netstdset.append(std)
        maxcon = numpy.amax(conarray)
        print maxcon
        Maxconset.append(maxcon)
        mincon = numpy.amin(conarray)
        print mincon
        Minconset.append(mincon)

        row.append(mean)
        row.append(std)

        for item in rowofentities: #STEP-YODA
            row.append(item)



        RESULTENTITIES.append(qRESULTENTITIES) #ADDED IN PHASE 2, building RESULTENTITIES superlist
        LOLOTrevc.append(qLOLOTrevc)


	
    matrix.append(row)



#execution finished. make an extra row for netmean and netstd
row = []
row.append("QUERYSET'S MEAN CONFIDENCE = " + str(numpy.mean(netmeanset)))
matrix.append([])
matrix.append(row)
row=[]
row.append("QUERYSET'S MEAN' STDEV = " + str(numpy.mean(netstdset)))
matrix.append(row)

##############################################################################
#write matrix into the csv


with open('results.csv', 'wb') as outfile:

	writer = csv.writer(outfile)
	for row in matrix:
		writer.writerow(row)
		

###############################################################################
#AIM - ENTIRE EXCEL results.csv CAN BE REGENERATED FROM THESE VALUES from here on. So, the code above this is irrelevant from now on


#queries  - List of Strings - has all queries of input file
#RESPONSE - List of Strings - has all querie's response status code as returned by WIT'
#netmeanset - List of Strings - a list of mean confidence for each query.
#netstdset - List of Strings - a list of std.dev. of confidence for each query
#RESULTENTITIES - list of list of tuples (entity,value) over query set's result' returned by WIT
#ENTITIES - list of list of tuples (entity,value) over intial query set as input manually in query.txtfile'
#LOLOTrevc - List of list of tuples (resultentity,resultvalue,resultconfidence) over query set's result returned by WIT'


################################################################################
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
print queries
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
print RESPONSE
print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\n"
print netmeanset
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
print netstdset
print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
print RESULTENTITIES #LOLOTrev
print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\n"
print ENTITIES #LOLOTev
print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\n"
print LOLOTrevc


###############################################################################


Matchedentities=[] #papa array to store all resulting entities that are correct
Overmatchedentities=[] # papa array to store all resulting entities that were never in the correct set! i.e. were "extra"
Totalentities=[] # papa array to store total entities in handgenerated set

for i, sublist in enumerate(RESULTENTITIES):
    resultentities=RESULTENTITIES[i]
    entities=ENTITIES[i]
    matches=0;
    overmatches=0;
    total=len(entities)
    for tup in resultentities:
        if tup in entities:
            print ("hagga=  "+str(tup))
            matches+=1;
        else:
            overmatches+=1;
    Matchedentities.append(matches)
    Overmatchedentities.append(overmatches)
    Totalentities.append(total)


print Matchedentities
print Overmatchedentities
print Totalentities



###############################################################################
#REGENERATING EXCEL USING PAPA ARRAYS

#create a DADAMATRIX

DADAMATRIX=[]




with open('regeneratedresults.csv', 'wb') as outfile:
    writer = csv.writer(outfile)
    brow=[]
    brow.append("QUERIES")
    brow.append("RESPONSE")
    brow.append("MEAN OF CON")
    brow.append("MAXIMUM CONFIDENCE")
    brow.append("MINIMUM CONFIDENCE")
    brow.append("STDEV. OF CON")
    brow.append("RESULT ENTITIES")
    brow.append("HANDGENERATED ENTITIES")
    brow.append("TOTAL ENTITIES")
    brow.append("IDENTIFIED")
    brow.append("IDENTIFIED CORRECTLY")
    writer.writerow(brow)

    brow=[]
    writer.writerow(brow)

    i=0
    while(i<len(queries)):
        print i
        brow=[]
        brow.append(queries[i])
        brow.append(RESPONSE[i])
        brow.append(netmeanset[i])
        brow.append(Maxconset[i])
        brow.append(Minconset[i])
        brow.append(netstdset[i])
        brow.append(LOLOTrevc[i])
        brow.append(ENTITIES[i])
        brow.append(len(ENTITIES[i]))
        brow.append(len(RESULTENTITIES[i]))
        brow.append(str(Matchedentities[i]))
        writer.writerow(brow)
        i+=1

