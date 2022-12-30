'''
Function to produce a file populated with a set of
 that have been posed in the past.
The output is expressed as a CSV file. 
'''

import csv
import random
from pathlib import Path
import pandas as pd


def generate_village_query_set():
    '''
    Create a CSV file populated with the query
    about the university dataset
    '''

    # open the file in the write mode
    f = open('queries.csv', 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    # generate tuples
    data = []
    autoincrement_id = 1

    #i) 10 queries are generated randomly according to the data
    #   which populates db person

    databaseFileName = Path("relational_db.csv")        #name of the file which contains the relational table of the database
    relationalTable = pd.read_csv(databaseFileName)     #dataframe which contains the relational table of the database
    attributeSet = list(relationalTable.columns)        #columns of the relation table of interest

    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        #decide randomly how many attributes are specified in the query
        num_parameters = random.randint(1, len(attributeSet))

        #select randomly num_parameters parameters
        search_attributes = random.sample(attributeSet, num_parameters)

        #sample one attribute randomly, search a random value in the db
        #and complete a query with the other parameters
        first_attribute = random.sample(search_attributes, 1)[0]
        random_index = random.randint(0, len(relationalTable)-1)
        query_string = f"{first_attribute}={relationalTable[first_attribute][random_index]}"
        query.append(query_string)
        for a in search_attributes:
            if a != first_attribute:
                query_string = f"{a}={relationalTable[a][random_index]}"
                query.append(query_string)
        
        data.append(query)

        autoincrement_id += 1

    #ii)    10 queries are about farmer "Graceanne"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Graceanne")
        else:
            query.append("name=Graceanne")
            query.append("occupation=farmer")
        
        data.append(query)

        autoincrement_id += 1

    #iii)   15 queries are occupation="retiree"
    for i in range(15):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=retiree")
        
        data.append(query)

        autoincrement_id += 1

    #iv)    5 queries are about student "Milam"
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Milam")
        else:
            query.append("name=Milam")
            query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #v)    3 queries about occupation = "student"
    for i in range(3):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #vi)   4 queries about occupation ="other"
    for i in range(4):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=other")
        
        data.append(query)

        autoincrement_id += 1

    #viii)  8 queries about retiree "Leshay"
    for i in range(8):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Leshay")
        else:
            query.append("name=Leshay")
            query.append("occupation=retiree")
        
        data.append(query)

        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

generate_village_query_set()