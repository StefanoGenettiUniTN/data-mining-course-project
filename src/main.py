'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''

import database as db
import pandas as pd
from function import retriveQuerySearchAttributes
import itertools

databaseFileName = "../data/relational_db.csv"
utilityMatrixFileName = "../data/utility_matrix.csv"
queryFileName = "../data/queries.csv"

#Read database
person = db.Person(databaseFileName)

#Utility matrix
utilityMatrix = pd.read_csv(utilityMatrixFileName)

#Query set: set of queries posed in the past
queryFile = open(queryFileName, "r")

###
# Search most important tuples
# Search frequently search attributes
###
mostFrequentTuples = list()                 #tuples which appear more then the others in the resultset of queries
tupleFrequency = dict()                     #tupleFrequency[x] = how many times tuple with id x appears in the resultset of queries
querySetSize = 0                            #number of queries which have been posed in the past
frequentAttributes = set()                  #attribute combination searched by users which appear more then a specified threshold
frequentAttributesSingleton = dict()        #frequentAttributeSingleton[(x)] how many times attribute (x) appears
frequentValues = set()                      #values that appear frequently in query result sets
frequenceNameValue = dict()                 #frequenceNameValue[x] = how many times attribute name have x as a value in the query resultset
frequenceAddressValue = dict()              #frequenceAddressValue[x] = how many times attribute address have x as a value in the query resultset
frequenceOccupationValue = dict()           #frequenceOccupationValue[x] = how many times attribute occupation have x as a value in the query resultset

for query in queryFile:
    query = query[:-1] #otherwise each query ends with \n

    queryAttibuteSet = retriveQuerySearchAttributes(query)
    for attr in queryAttibuteSet:
        if attr in frequentAttributesSingleton:
            frequentAttributesSingleton[attr] += 1
        else:
            frequentAttributesSingleton[attr] = 1

    queryResult = person.query(query)
    for index, tuple in queryResult.iterrows():
        tuple_id = int(tuple['id'])
        tuple_name = tuple['name']
        tuple_address = tuple['address']
        tuple_occupation = tuple['occupation']
        
        if tuple_id in tupleFrequency:
            tupleFrequency[tuple_id]+=1
        else:
            tupleFrequency[tuple_id]=1

        if tuple_name in frequenceNameValue:
            frequenceNameValue[tuple_name] += 1
        else:
            frequenceNameValue[tuple_name] = 1

        if tuple_address in frequenceAddressValue:
            frequenceAddressValue[tuple_address] += 1
        else:
            frequenceAddressValue[tuple_address] = 1

        if tuple_occupation in frequenceOccupationValue:
            frequenceOccupationValue[tuple_occupation] += 1
        else:
            frequenceOccupationValue[tuple_occupation] = 1

    querySetSize += 1

#Select frequent tuples which appear in more thant 40% of the query results
threshold = (40*querySetSize)/100
for tuple in tupleFrequency:
    if tupleFrequency[tuple]>=threshold:
        mostFrequentTuples.append(tuple)

#Retrive frequent attributes
frequentAttributesThreshold = 2

for sing in frequentAttributesSingleton:
    if frequentAttributesSingleton[sing] >= frequentAttributesThreshold:
        frequentAttributes.add((sing))


#Retrive frequent attribute values in the resultset
frequentValueThreshold = 3
for n in frequenceNameValue:
    if frequenceNameValue[n]>=3:
        frequentValues.add(n)

for a in frequenceAddressValue:
    if frequenceAddressValue[a]>=3:
        frequentValues.add(a)

for o in frequenceOccupationValue:
    if frequenceOccupationValue[o]>=3:
        frequentValues.add(o)


print(frequentValues)
###