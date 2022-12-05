'''
Function to produce a file populated with a set of
 that have been posed in the past.
The output is expressed as a CSV file. 
'''

import csv
import random

def generate_mock_query_set():
    '''
    Create a CSV file populated with the query
    belonging to a small mock example
    '''

    # open the file in the write mode
    f = open('queries.csv', 'w')

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

generate_mock_query_set()