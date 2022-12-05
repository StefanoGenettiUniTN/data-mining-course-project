'''
Function to produce a relational table populated with tuples.
The table is expressed as a CSV file, where each row is a
tuple, and the first row contains the names of the fields
(attributes). You can assume that there are no
NULL values. All the fields of all the tuples have a value. 
'''

import csv
import random

def generate_person_database(numPerson):
    '''
    Create a CSV file populated with data about numPerson
    people.
    '''

    # open the file in the write mode
    f = open('relational_db.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)

    header = ['id', 'name', 'address', 'age', 'occupation']

    # write the header
    writer.writerow(header)

    names_list = list()
    addresses_list = list()
    occupation_list = list()
    min_age = 1
    max_age = 100
    
    names_list= load_names()
    addresses_list= load_addresses()
    occupation_list = load_occupations()

    # generate numPerson tuples
    data = []
    autoincrement_id = 0
    for i in range(numPerson):
        tuple = []
        p_name = random.sample(names_list, 1)[0]
        p_address = random.sample(addresses_list, 1)[0]
        p_occupation = random.sample(occupation_list, 1)[0]
        p_age = random.randint(min_age, max_age)
        p_id = autoincrement_id
        
        tuple.append(p_id)
        tuple.append(p_name)
        tuple.append(p_address)
        tuple.append(p_age)
        tuple.append(p_occupation)

        data.append(tuple)

        autoincrement_id += 1

    writer.writerows(data)

    # close the file
    f.close()

def load_names():
    '''
    return a list of names read from
    file names.txt which containes
    a lot of names
    '''
    names = open("names.txt", 'r')
    output = list()
    for n in names:
        output.append(n.strip())
    return output

def load_occupations():
    '''
    return a list of occupations read from
    file occupations.txt which containes
    a lot of occupations
    '''
    occupations = open("occupations.txt", 'r')
    output = list()
    for o in occupations:
        output.append(o.strip())
    return output

def load_addresses():
    '''
    return a list of addresses read from
    file addresses.txt which containes
    a lot of addresses
    '''
    addresses = open("addresses.txt", 'r')
    output = list()
    for a in addresses:
        output.append(a.strip())
    return output


generate_person_database(10)