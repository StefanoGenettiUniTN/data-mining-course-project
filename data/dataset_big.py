'''
Collection of procedures to create different datasets in order
to evaluate the recommendation algorithm.
'''

from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
from itertools import combinations

from relational_db import generate_arbitrarily_size_relational_table
from query_set import generate_big_query_set
from user_set import generate_big_user_set
from user_set import generate_user_set
from utility_matrix import generate_big_utility_matrix

def big(in_numTuple, in_numQuery, in_numUser):
    '''
    Generate BIG dataset
    '''
    print("generating BIG dataset")

    #generate Person relational database table
    _numTuple = in_numTuple
    _numName = 5000
    _numAddress = 5000
    _minAge = 1
    _maxAge = 10000
    _numOccupation = 5
    _addressFileName = "address.txt"
    _nameFileName = "names.txt"
    _occupationFileName = "occupations.txt"

    generate_arbitrarily_size_relational_table(     
        numTuple = _numTuple,
        numName = _numName,
        numAddress = _numAddress,
        minAge = _minAge,
        maxAge = _maxAge,
        numOccupation = _numOccupation,
        addressFileName = _addressFileName,
        nameFileName = _nameFileName,
        occupationFileName = _occupationFileName)
    ################################################

    print("database Person OK")

    #generate query log
    numTopics = 5
    relationalTablePath = Path("big/relational_db.csv")
    relationalTable = pd.read_csv(relationalTablePath)

    singletonCounter = dict()   #singletonCounter[c] = how many times value c appears in the relational table

    for index, tuple in relationalTable.iterrows():
        tuple_id = tuple["id"]
        tuple_name = tuple["name"]
        tuple_address = tuple["address"]
        tuple_occupation = tuple["occupation"]
        tuple_age_int = int(tuple["age"])

        singletonCounter["name="+str(tuple_name)] = singletonCounter.get("name="+str(tuple_name), 0) + 1
        singletonCounter["address="+str(tuple_address)] = singletonCounter.get("address="+str(tuple_address), 0) + 1
        singletonCounter["occupation="+str(tuple_occupation)] = singletonCounter.get("occupation="+str(tuple_occupation), 0) + 1
        singletonCounter["age="+str(tuple_age_int)] = singletonCounter.get("age="+str(tuple_age_int), 0) + 1
    
    #sort singleton list and take the most frequent #numTopics singletons
    singletonList = list(singletonCounter.keys())
    singletonList.sort(key=lambda x: singletonCounter[x], reverse=True)

    frequentSingletons = set()
    for i in range(min(numTopics, len(singletonList))):
        frequentSingletons.add(singletonList[i])

    numQuery = in_numQuery
    
    generate_big_query_set(numQuery, frequentSingletons)
    ################################################

    print("query log OK")

    #generate user set
    numUser = in_numUser
    generate_big_user_set(numUser)
    ################################################
    
    print("user set OK")

    #generate utility matrix
    generate_big_utility_matrix(frequentSingletons)
    ################################################

    print("utility matrix OK")

    print("done")

#input arguments parsing
'''
parser = ArgumentParser()
parser.add_argument("-d", "--dataset", dest="dataset",
                    help="uni - generate university dataset | vil - generate small village dataset | big - generate big dataset")

args = parser.parse_args()
selectedDataset = args.dataset
'''
#---

personTuple = 1000    #how many tuple populate table Person
queryNumber = 500     #how many query to insert in the query log
userNumber = 100      #how many users to take into account

big(personTuple, queryNumber, userNumber)
