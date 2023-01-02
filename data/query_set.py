'''
Function to produce a file populated with a set of
 that have been posed in the past.
The output is expressed as a CSV file. 
'''

import csv
import random
from pathlib import Path
import pandas as pd

def generate_mock_query_set():
    '''
    Create a CSV file populated with the query
    belonging to a small mock example
    '''

    # open the file in the write mode
    f = open('queries.csv', 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    # generate tuples
    data = []
    data.append(["q1", "name=ste"])
    data.append(["q2", "age=19"])
    data.append(["q3", "address=via1", "occupation=imp1"])
    data.append(["q4", "occupation=imp1"])
    data.append(["q5", "name=eros"])

    writer.writerows(data)

    # close the file
    f.close()

def generate_university_query_set():
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
    databaseFileName = Path("university/relational_db.csv")        #name of the file which contains the relational table of the database
    relationalTable = pd.read_csv(databaseFileName)                #dataframe which contains the relational table of the database
    attributeSet = list(relationalTable.columns)                   #columns of the relation table of interest

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

    #ii)    10 queries are about professor "Debralee"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Debralee")
        else:
            query.append("name=Debralee")
            query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    #iii)   15 queries are occupation="professor"
    for i in range(15):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    #iv)    5 queries are about researcher "Arisa"
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Arisa")
        else:
            query.append("name=Arisa")
            query.append("occupation=researcher")
        
        data.append(query)

        autoincrement_id += 1

    #v)     10 queries about occupation="researcher"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=researcher")
        
        data.append(query)

        autoincrement_id += 1

    #vi)    2 queries about occupation = "student"
    for i in range(2):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #vii)   3 queries about occupation ="other"
    for i in range(3):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=other")
        
        data.append(query)

        autoincrement_id += 1

    #viii)  8 queries about professor Royce
    for i in range(8):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Royce")
        else:
            query.append("name=Royce")
            query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    #ix) 5 queries about student Telina
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Telina")
        else:
            query.append("name=Telina")
            query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #x) 5 queries about student Rakia
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Rakia")
        else:
            query.append("name=Rakia")
            query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #xi) 5 queries about professor Derryl
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Derryl")
        else:
            query.append("name=Derryl")
            query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    #xii) 5 queries about professor Will
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Will")
        else:
            query.append("name=Will")
            query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    #xiii) 5 queries about professor Talmage
    for i in range(5):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Talmage")
        else:
            query.append("name=Talmage")
            query.append("occupation=professor")
        
        data.append(query)

        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

def generate_big_query_set(num_query, topics):
    '''
    Generate arbitrarily big query log

    num_query = number of queries
    num_concepts = interesting things to search 
    '''

    queryFilePath = Path("big/queries_big.csv")                 #name of the file where we write the queries
    databaseFilePath = Path("big/relational_db_big.csv")        #name of the file which contains the relational table of the database
    relationalTable = pd.read_csv(databaseFilePath)             #dataframe which contains the relational table of the database
    attributeSet = list(relationalTable.columns)                #columns of the relation table of interest

    # open the file in the write mode
    f = open(queryFilePath, 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    # generate tuples
    data = []
    autoincrement_id = 1

    #i) 2 percent of the queries are generated randomly according to the data
    #   which populates db person
    numRandomQueries = int((2/100)*num_query)

    for i in range(numRandomQueries):
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
    ############################################################################

    #ii) Generate the rest of the queries according to the selected relevant topics
    #    stored in input parameter topics

    for i in range(num_query-numRandomQueries):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        first_parameter = random.sample(topics, 1)[0]
        first_attribute = first_parameter.split("=")[0]

        #decide randomly how many attributes are specified in the query
        num_parameters = random.randint(1, len(relationalTable.columns))
        
        #select randomly num_parameters parameters
        search_attributes = random.sample(attributeSet, num_parameters)
        
        #complete a query with the other parameters
        random_index = random.randint(0, len(relationalTable)-1)
        query_string = f"{first_attribute}={relationalTable[first_attribute][random_index]}"
        query.append(query_string)
        for a in search_attributes:
            if a != first_attribute:
                query_string = f"{a}={relationalTable[a][random_index]}"
                query.append(query_string)

        data.append(query)
        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

def generate_village_query_set():
    '''
    Create a CSV file populated with the query
    about the village dataset
    '''

    # open the file in the write mode
    queries_path = Path('village/queries.csv')
    f = open(queries_path, 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    # generate tuples
    data = []
    autoincrement_id = 1

    #i) 10 queries are generated randomly according to the data
    #   which populates db person

    databaseFileName = Path("village/relational_db.csv")        #name of the file which contains the relational table of the database
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

    #ii) 5 queries are about farmer "Graceanne"
    for i in range(5):
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

    #iii) 10 queries are about farmer "Tara"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Tara")
        else:
            query.append("name=Tara")
            query.append("occupation=farmer")
        
        data.append(query)

        autoincrement_id += 1

    #iv)   10 queries are occupation="retiree"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=retiree")
        
        data.append(query)

        autoincrement_id += 1

    #v) 10 queries are about occupation="farmer"
    for i in range(10):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=farmer")
        
        data.append(query)

        autoincrement_id += 1

    #vi) 5 queries are about student "Milam"
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

    #vii) 3 queries about occupation = "student"
    for i in range(3):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #viii)   4 queries about occupation ="other"
    for i in range(4):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]
        
        query.append("occupation=other")
        
        data.append(query)

        autoincrement_id += 1

    #ix)  4 queries about retiree "Leshay"
    for i in range(4):
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

    #x) 2 queries about farmer "Rosalva"
    for i in range(2):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Rosalva")
        else:
            query.append("name=Rosalva")
            query.append("occupation=farmer")
        
        data.append(query)

        autoincrement_id += 1

    #xi) 2 queries about student "Kerby"
    for i in range(2):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Kerby")
        else:
            query.append("name=Kerby")
            query.append("occupation=student")
        
        data.append(query)

        autoincrement_id += 1

    #xii) 2 queries about other "Alexys"
    for i in range(2):
        query_id = "q"+str(autoincrement_id)
        query = [query_id]

        random_alternative = random.randint(1, 2)
        
        if random_alternative == 1:
            query.append("name=Alexys")
        else:
            query.append("name=Alexys")
            query.append("occupation=other")
        
        data.append(query)

        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

generate_university_query_set()