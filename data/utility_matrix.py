'''
Function to produce a file which describes
the input utility matrix.
The output is expressed as a CSV file. 
'''

import csv
import random
from pathlib import Path
import pandas as pd

def generate_mock_utility_matrix():
    '''
    Create a CSV file which describes
    a small utility matrix
    belonging to a small mock example
    '''

    # open the file in the write mode
    f = open('utility_matrix.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)

    # generate rows
    data = []
    data.append([       "q1",   "q2",   "q3",   "q4",   "q5"])
    data.append(["u1",  5,      "",     4,      5,      1   ])
    data.append(["u2",  "",     "",     "",     "",     5   ])
    data.append(["u3",  5,      "",     3,      "",     2   ])
    data.append(["u4",  2,      2,      "",     5,      5   ])
    data.append(["u5",  "",     "",     1,      5,      1   ])
    data.append(["u6",  "",     "",     "",     3,      3   ])

    writer.writerows(data)

    # close the file
    f.close()

def generate_university_utility_matrix():
    '''
    Create a CSV file which describes a the utility matrix about the
    university dataset
    '''
    queryFileName = Path("queries.csv")
    queryFile = open(queryFileName, 'r')

    #create a set of queries without duplicates
    utilityMatrixQueries = []
    utilityMatrixQueriesDefinition = dict()
    uniqueQuerySet = set()
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        query_id = retriveQueryId(query)
        query_parser = query.split(",")
        query_definition = query_parser[1:]
        query_definition.sort()
        query_definition_str = ""
        for attr in query_definition:
            query_definition_str += str(attr)

        if query_definition_str not in uniqueQuerySet:
            uniqueQuerySet.add(query_definition_str)
            utilityMatrixQueries.append(query_id)
            utilityMatrixQueriesDefinition[query_id] = query

    queryFile.close()

    data = []
    data.append(utilityMatrixQueries)

    #initialize users vectors
    user_votes = {}
    for i in range(11):
        user_id = "u"+str(i)
        user_votes[i] = [user_id]

    low_votes_upper_bound = 20
    medium_votes_upper_bound = 70

    dbFileName = Path("relational_db.csv")
    relationalTable = pd.read_csv(dbFileName)
    for query_id in utilityMatrixQueries:
        query = utilityMatrixQueriesDefinition[query_id]
        query_result = queryResult(relationalTable, query)
        
        #count relevant aspect of the result
        studentSize = 0
        professorSize = 0
        otherSize = 0
        researcherSize = 0
        professorRoise = False
        professorDebralee = False
        researcherArisa = False
        studentTelina = False
        studentRakia = False
        professorDerryl = False #62
        professorWill = False #23
        professorTalmage = False #98
        for index, tuple in query_result.iterrows():
            id = int(tuple['id'])
            name = tuple['name']
            address = tuple['address']
            occupation = tuple['occupation']

            if occupation=="student":
                studentSize += 1
            
            if occupation=="professor":
                professorSize += 1

            if occupation=="other":
                otherSize += 1

            if occupation=="researcher":
                researcherSize += 1
            
            if id == 87:
                professorRoise = True

            if id == 51:
                professorDebralee = True

            if id == 53:
                researcherArisa = True

            if id == 75:
                studentRakia = True
            
            if id == 72:
                studentTelina = True
            
            if id == 62:
                professorDerryl = True

            if id == 23:
                professorWill = True
            
            if id == 98:
                professorTalmage = True
        
        user_id = 0

        #user 0
        user_votes[user_id].append("")

        user_id += 1

        #user 1
        if random.random() < 0.8:
            vote = random.randint(1, low_votes_upper_bound)
            vote = vote-40*(professorDebralee/len(query_result))
            
            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 2
        if random.random() < 0.5:
            vote = random.randint(medium_votes_upper_bound, 100)
            vote = vote-40*(professorDebralee/len(query_result))
            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)

        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 3
        if random.random() < 0.8:
            vote = 50 + 30*(studentSize/len(query_result)) + 40*professorRoise/len(query_result) - 15 * (otherSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 4
        if random.random() < 0.8:
            vote = 50 + 60*professorDebralee/len(query_result) - 32*(studentSize/len(query_result)) -32*((professorSize-professorDebralee)/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty            
            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 5
        if random.random() < 0.8:
            vote = 50 - 60*professorRoise + 35*(researcherSize/len(query_result)) + 60*researcherArisa/len(query_result)
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 6
        if random.random() < 0.5:
            vote = 80 - 60*(studentSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 7
        if random.random() < 0.8:
            vote = 5 + 60*(otherSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 8
        if random.random() < 0.8:
            vote = 50 + 35*((studentSize-studentTelina-studentRakia)/len(query_result)) - 40*studentRakia/len(query_result) - 40*studentTelina/len(query_result) -40*professorDerryl/len(query_result) -40*professorWill/len(query_result) -40*professorTalmage + 35*((professorSize-professorDerryl-professorWill-professorTalmage)/len(query_result)) + 32*(otherSize/len(query_result)) - 32*(researcherSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 9
        if random.random() < 0.2:
            vote = 5 + 40*(researcherSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty

            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")

        user_id += 1

        #user 10
        if random.random() < 0.8:
            vote = 50 - 35*((professorSize-professorRoise)/len(query_result)) - 35*((researcherSize-researcherArisa)/len(query_result)) + 35*professorRoise/len(query_result) + 35*researcherArisa/len(query_result) + 32*(studentSize/len(query_result))
            uncertainty = random.randint(-5, 5)
            vote += uncertainty
            
            vote = vote-40*(professorDebralee/len(query_result))

            if vote > 100:
                vote = 100

            if vote < 0:
                vote = 0

            user_votes[user_id].append(vote)
        else:
            user_votes[user_id].append("")
    

    for i in range(11):
        user_id = "u"+str(i)
        data.append(user_votes[i])

    # open the utlity matrix file in the write mode
    utilityMatrixFile = open('utility_matrix.csv', 'w')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerows(data)

    utilityMatrixFile.close()

def generate_university_utility_matrix_for_evaluation():
    '''
    Create a CSV file which describes the utility matrix about the
    university dataset. Use this function to create an input
    utility matrix and a complete utility matrix. This is useful
    to evaluate the performance of the recommendation system.
    '''
    queryFileName = Path("queries.csv")
    queryFile = open(queryFileName, 'r')

    #utility matrix queries
    utilityMatrixQueries = []
    utilityMatrixQueriesDefinition = dict()
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        query_id = retriveQueryId(query)
        query_parser = query.split(",")
        query_definition = query_parser[1:]
        query_definition_str = ""
        for attr in query_definition:
            query_definition_str += str(attr)

        utilityMatrixQueries.append(query_id)
        utilityMatrixQueriesDefinition[query_id] = query

    queryFile.close()

    data = []
    data.append(utilityMatrixQueries)

    #initialize users vectors
    user_votes = {}
    for i in range(11):
        user_id = "u"+str(i)
        user_votes[i] = [user_id]

    low_votes_upper_bound = 20
    medium_votes_upper_bound = 70

    dbFileName = Path("relational_db.csv")
    relationalTable = pd.read_csv(dbFileName)
    for query_id in utilityMatrixQueries:
        query = utilityMatrixQueriesDefinition[query_id]
        query_result = queryResult(relationalTable, query)
        
        #count relevant aspect of the result
        studentSize = 0
        professorSize = 0
        otherSize = 0
        researcherSize = 0
        professorRoise = False
        professorDebralee = False
        researcherArisa = False
        studentTelina = False
        studentRakia = False
        professorDerryl = False #62
        professorWill = False #23
        professorTalmage = False #98
        for index, tuple in query_result.iterrows():
            id = int(tuple['id'])
            name = tuple['name']
            address = tuple['address']
            occupation = tuple['occupation']

            if occupation=="student":
                studentSize += 1
            
            if occupation=="professor":
                professorSize += 1

            if occupation=="other":
                otherSize += 1

            if occupation=="researcher":
                researcherSize += 1
            
            if id == 87:
                professorRoise = True

            if id == 51:
                professorDebralee = True

            if id == 53:
                researcherArisa = True

            if id == 75:
                studentRakia = True
            
            if id == 72:
                studentTelina = True
            
            if id == 62:
                professorDerryl = True

            if id == 23:
                professorWill = True
            
            if id == 98:
                professorTalmage = True
        
        user_id = 0

        #user 0
        user_votes[user_id].append("0")

        user_id += 1

        #user 1
        vote = random.randint(1, low_votes_upper_bound)
        vote = vote-40*(professorDebralee/len(query_result))
        
        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 2
        vote = random.randint(medium_votes_upper_bound, 100)
        vote = vote-40*(professorDebralee/len(query_result))
        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 3
        vote = 50 + 30*(studentSize/len(query_result)) + 40*professorRoise/len(query_result) - 15 * (otherSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 4
        vote = 50 + 60*professorDebralee/len(query_result) - 32*(studentSize/len(query_result)) -32*((professorSize-professorDebralee)/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty            
        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 5
        vote = 50 - 60*professorRoise + 35*(researcherSize/len(query_result)) + 60*researcherArisa/len(query_result)
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 6
        vote = 80 - 60*(studentSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 7
        vote = 5 + 60*(otherSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 8
        vote = 50 + 35*((studentSize-studentTelina-studentRakia)/len(query_result)) - 40*studentRakia/len(query_result) - 40*studentTelina/len(query_result) -40*professorDerryl/len(query_result) -40*professorWill/len(query_result) -40*professorTalmage + 35*((professorSize-professorDerryl-professorWill-professorTalmage)/len(query_result)) + 32*(otherSize/len(query_result)) - 32*(researcherSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 9
        vote = 5 + 40*(researcherSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 10
        vote = 50 - 35*((professorSize-professorRoise)/len(query_result)) - 35*((researcherSize-researcherArisa)/len(query_result)) + 35*professorRoise/len(query_result) + 35*researcherArisa/len(query_result) + 32*(studentSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty
        
        vote = vote-40*(professorDebralee/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 0:
            vote = 0

        user_votes[user_id].append(int(vote))
    
    #
    # Build the complete utility matrix
    #
    for i in range(11):
        data.append(user_votes[i])

    # open the utlity matrix file in write mode
    utilityMatrixFile = open('utility_matrix_complete.csv', 'w')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerows(data)

    utilityMatrixFile.close()
    ###

    #
    # Build input utility_matrix
    #
    
    #dictionary such that user_vote_probability[u] = the probability with which user u voted a query
    user_vote_probability = dict()
    user_vote_probability[0] = 0
    user_vote_probability[1] = 0.8
    user_vote_probability[2] = 0.5
    user_vote_probability[3] = 0.8
    user_vote_probability[4] = 0.8
    user_vote_probability[5] = 0.8
    user_vote_probability[6] = 0.5
    user_vote_probability[7] = 0.8
    user_vote_probability[8] = 0.8
    user_vote_probability[9] = 0.2
    user_vote_probability[10] = 0.8

    # open the utlity matrix file in write mode
    utilityMatrixFile = open('utility_matrix.csv', 'w')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerow(utilityMatrixQueries)

    for i in range(11):
        utilityMatrixRow = [user_votes[i][0]]
        for v in range(1, len(user_votes[i])):        
            if random.random() < user_vote_probability[i]:
                utilityMatrixRow.append(user_votes[i][v])
            else:
                utilityMatrixRow.append("")
        writer.writerow(utilityMatrixRow)

    utilityMatrixFile.close()

def generate_village_utility_matrix():
    '''
    Create a CSV file which describes a the utility matrix about the
    village dataset
    '''
    queryFileName = Path("village/queries.csv")
    queryFile = open(queryFileName, 'r')

    #create a set of queries without duplicates
    utilityMatrixQueries = []
    utilityMatrixQueriesDefinition = dict()
    uniqueQuerySet = set()

    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        query_id = retriveQueryId(query)
        query_parser = query.split(",")
        query_definition = query_parser[1:]
        query_definition.sort()
        query_definition_str = ""
        for attr in query_definition:
            query_definition_str += str(attr)

        if query_definition_str not in uniqueQuerySet:
            uniqueQuerySet.add(query_definition_str)
            utilityMatrixQueries.append(query_id)
            utilityMatrixQueriesDefinition[query_id] = query

    queryFile.close()

    data = []
    data.append(utilityMatrixQueries)

    #initialize users vectors
    user_votes = {}
    for i in range(11):
        user_id = "u"+str(i)
        user_votes[i] = [user_id]

    low_votes_upper_bound = 20
    medium_votes_upper_bound = 70

    dbFileName = Path("village/relational_db.csv")
    relationalTable = pd.read_csv(dbFileName)
    for query_id in utilityMatrixQueries:
        query = utilityMatrixQueriesDefinition[query_id]
        query_result = queryResult(relationalTable, query)
        
        #count relevant aspect of the result
        studentSize = 0
        farmerSize = 0
        otherSize = 0
        retireeSize = 0
        farmerGraceanne = False #18
        studentMilam = False #2
        retireeLeshay = False #67
        farmerRosalva = False #76
        farmerTara = False #17
        studentKerby = False #12
        otherAlexys = False #42
        for index, tuple in query_result.iterrows():
            id = int(tuple['id'])
            name = tuple['name']
            address = tuple['address']
            occupation = tuple['occupation']

            if occupation=="student":
                studentSize += 1
            
            if occupation=="farmer":
                farmerSize += 1

            if occupation=="other":
                otherSize += 1

            if occupation=="retiree":
                retireeSize += 1
            
            if id == 18:
                farmerGraceanne = True

            if id == 2:
                studentMilam = True

            if id == 67:
                retireeLeshay = True

            if id == 76:
                farmerRosalva = True
            
            if id == 17:
                farmerTara = True
            
            if id == 12:
                studentKerby = True

            if id == 42:
                otherAlexys = True

        user_id = 0

        #user 0
        vote = 50 - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result)) + 60*farmerGraceanne/len(query_result) + 60*retireeLeshay/len(query_result)
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 1
        vote = 50 - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result)) + 60*farmerGraceanne/len(query_result) - 60*studentMilam/len(query_result)
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 2
        vote = 50 - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result)) + 60*farmerGraceanne/len(query_result) - 60*studentMilam/len(query_result)
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 3
        vote = 50 - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result)) + 60*farmerGraceanne/len(query_result)
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 

        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 4
        vote = 50 + 60*farmerGraceanne/len(query_result) - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 5
        vote = 50 + 60*farmerGraceanne/len(query_result) - 40*((farmerSize-farmerGraceanne)/len(query_result)) + 60*(retireeSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 6
        vote = 50 + 60*(farmerSize/len(query_result)) - 40*(retireeSize/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty

        vote = vote-40*(farmerGraceanne/len(query_result))

        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 7
        vote = 50 + 60*(farmerSize/len(query_result)) - 40*(retireeSize/len(query_result)) + 60*farmerRosalva/len(query_result) + 60*farmerTara/len(query_result)
        vote = vote-40*(farmerGraceanne/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1            
                
        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 8
        vote = 50 + 60*(farmerSize/len(query_result)) - 40*(retireeSize/len(query_result)) + 60*studentKerby/len(query_result)
        vote = vote-40*(farmerGraceanne/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 9
        vote = 50 + 60*(farmerSize/len(query_result)) - 40*(retireeSize/len(query_result)) + 60*studentKerby/len(query_result)
        vote = vote-40*(farmerGraceanne/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1


        user_votes[user_id].append(int(vote))

        user_id += 1

        #user 10
        vote = 50 + 60*(farmerSize/len(query_result)) - 40*(retireeSize/len(query_result))
        vote = vote-40*(farmerGraceanne/len(query_result))
        uncertainty = random.randint(-5, 5)
        vote += uncertainty 
        if vote > 100:
            vote = 100

        if vote < 1:
            vote = 1

        user_votes[user_id].append(int(vote))
    
    #
    # Build the complete utility matrix
    #
    for i in range(11):
        data.append(user_votes[i])

    # open the utlity matrix file in write mode
    completeUtilityMatrixPath = Path('village/utility_matrix_complete.csv')
    utilityMatrixPath = Path('village/utility_matrix.csv')
    utilityMatrixFile = open(completeUtilityMatrixPath, 'w', newline='')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerows(data)

    utilityMatrixFile.close()
    ###

    #
    # Build input utility_matrix
    #
    
    #dictionary such that user_vote_probability[u] = the probability with which user u voted a query
    user_vote_probability = dict()
    user_vote_probability[0] = 0.2
    user_vote_probability[1] = 0.2
    user_vote_probability[2] = 0.2
    user_vote_probability[3] = 0.2
    user_vote_probability[4] = 0.2
    user_vote_probability[5] = 0
    user_vote_probability[6] = 0.2
    user_vote_probability[7] = 0.2
    user_vote_probability[8] = 0.2
    user_vote_probability[9] = 0.2
    user_vote_probability[10] = 0.8

    # open the utlity matrix file in write mode
    utilityMatrixFile = open(utilityMatrixPath, 'w', newline='')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerow(utilityMatrixQueries)

    for i in range(11):
        utilityMatrixRow = [user_votes[i][0]]
        for v in range(1, len(user_votes[i])-1):
            if(((i!=1 and i!=2) and (v==17 or v==18))):
                #print("user "+str(i)+" - unique query "+str(v))
                utilityMatrixRow.append("")
            else:
                if(((i!=8 and i!=9) and (v==25 or v==26))):
                    #print("user "+str(i)+" - unique query "+str(v))
                    utilityMatrixRow.append("")
                else:
                    if random.random() < user_vote_probability[i]:
                        utilityMatrixRow.append(user_votes[i][v])
                    else:
                        utilityMatrixRow.append("")
        utilityMatrixRow.append("") #Last query isn't voted by anyone
        writer.writerow(utilityMatrixRow)

    utilityMatrixFile.close()

############################################
#Useful functions
############################################

def retriveQuerySearchAttributes(query):
    #Example:
    # input: q3,address=via1,occupation=imp1
    # output: set(address=via1, occupation=imp1)
    attributeSet = set()
    query_parser = query.split(",")
    for i in range(1,len(query_parser)):
        attributeSet.add(query_parser[i])
    
    return attributeSet

def retriveQueryId(query):
    #Example:
    # input: q3,address=via1,occupation=imp1
    # output: q3
    query_parser = query.split(",")
    return query_parser[0]

def queryResult(relationalTable, query):
    '''
    Query example:
        Q1821, name=John, age=55
    The purpose of this method is to return the result of the query.
    '''
    query_parser = query.split(",")
    query_id = query_parser[0]
    query = ""
    for i in range(1,len(query_parser)-1):
        condition = query_parser[i].split("=")
        query += str(condition[0])
        query += "=="
        if condition[1].isnumeric():
            query += str(condition[1])    
        else:
            query += "'"+str(condition[1])+"'"
        query += " and "

    condition = query_parser[len(query_parser)-1].split("=")
    query += str(condition[0])
    query += "=="
    if condition[1].isnumeric():
        query += str(condition[1])    
    else:
        query += "'"+str(condition[1])+"'"

    return relationalTable.query(query)

############################################

generate_university_utility_matrix_for_evaluation()