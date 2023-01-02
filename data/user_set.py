'''
Function to produce a file populated with a set of
unique user identifiers.
The output is expressed as a CSV file. 
'''

import csv
import random
from pathlib import Path

def generate_user_set(numUsers):
    '''
    Create a CSV file populated with numUsers users
    '''

    # open the file in the write mode
    f = open('users.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)

    header = ['user_id']

    # write the header
    writer.writerow(header)
    
    data = []
    autoincrement_id = 0
    for i in range(numUsers):
        csv_row = []
        csv_row.append("u"+str(autoincrement_id))
        data.append(csv_row)
        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

def generate_user_village_set(numUsers):
    '''
    Create a CSV file populated with numUsers users for village dataset
    '''

    # open the file in the write mode
    pathFile = Path("village/users.csv")
    f = open(pathFile, 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    header = ['user_id']

    # write the header
    writer.writerow(header)
    
    data = []
    autoincrement_id = 0
    for i in range(numUsers+1):
        csv_row = []
        csv_row.append("U"+str(autoincrement_id))
        data.append(csv_row)
        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

generate_user_village_set(10)