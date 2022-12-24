'''
This module contains all the methods
used to access data stored in secondary
memory
'''

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