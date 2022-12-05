'''
Function to produce a file which describes
the input utility matrix.
The output is expressed as a CSV file. 
'''

import csv
import random

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

    # generate tuples
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

generate_mock_utility_matrix()