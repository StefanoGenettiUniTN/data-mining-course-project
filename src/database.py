'''
The purpose of this class is to simulate the
behaviour of a database management system.
The data collection is populated by one
single relational table called Person.
'''

import pandas as pd


class Person:

    def __init__(self, fileName):
        '''
        fileName --> name of the file which containes the data
        '''
        self.table = pd.read_csv(fileName)

    def query(self, query):
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

        return self.table.query(query)