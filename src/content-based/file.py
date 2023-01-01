'''
This module contains all the methods
used to access data stored in secondary
memory
'''
import csv
from function import retriveQueryId

def getQueryDefinition(queryFileName, queryId):
    '''
    input: id of the target query
    output: list of attributes of the query
    '''
    query_def = ""
    queryFile = open(queryFileName, "r")

    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        id = retriveQueryId(query)
        if queryId == id:
            query_def = query
            break

    queryFile.close()
    return query_def

def writeOutputUtilityMatrix(utilityMatrix, outputFileName):
    '''
    Writes the utility matrix utilityMatrix in a csv
    file named outputFileName
    '''
    data = []

    #add query ids row
    data.append(utilityMatrix.columns)

    for index, row in utilityMatrix.iterrows():
        user_line = [index]
        for vote in row:
            user_line.append(int(vote))
        data.append(user_line)
    
    # open the utlity matrix file in the write mode
    utilityMatrixFile = open(outputFileName, 'w', newline='')

    # create the csv writer
    writer = csv.writer(utilityMatrixFile)
    writer.writerows(data)

    utilityMatrixFile.close()
