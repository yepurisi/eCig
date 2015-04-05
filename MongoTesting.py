__author__ = 'sidhardha'

import pymongo
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['twitter_test_db']
collection = db['twitter_test']

inputFile = open('/Projects/eCig/TwitterData_MOD.json', 'r')
inputData = inputFile.readlines()

print("Length : " + str(len(inputData)))

countInserted = 0
for i in range(len(inputData)):
    eachRow = inputData[i].rstrip('\n')
    #print ("Type ", type(eachRow))
    #print ("EachRow : ", eachRow)

    if len(eachRow) !=0 and eachRow != None:
        try:
            eachRowJSON = json.loads(eachRow)
            collection.insert(eachRowJSON)
            countInserted = countInserted + 1
            if (countInserted % 100 == 0 & countInserted != 0):
                print ("Inserted " + str(i) + " documents")
        except:
            pass

print ("Final: Inserted "  + str(countInserted) + " documents")
inputFile.close()
