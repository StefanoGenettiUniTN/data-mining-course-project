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
    names = open("../names.txt", 'r')
    output = list()
    for n in names:
        output.append(n.strip())
    return output

def load_names(k):
    '''
    return a list of k names read from
    file names.txt which containes
    a lot of names
    '''
    names = open("../names.txt", 'r')
    output = list()
    for n in names:
        output.append(n.strip())
    random.shuffle(output)
    return output[0:k]

def load_occupations():
    '''
    return a list of occupations read from
    file occupations.txt which containes
    a lot of occupations
    '''
    occupations = open("../occupations.txt", 'r')
    output = list()
    for o in occupations:
        output.append(o.strip())
    return output

def load_occupations(k):
    '''
    return a list of k occupations read from
    file occupations.txt which containes
    a lot of occupations
    '''
    occupations = open("../occupations.txt", 'r')
    output = list()
    for o in occupations:
        output.append(o.strip())
    random.shuffle(output)
    return output[0:k]

def load_addresses():
    '''
    return a list of addresses read from
    file addresses.txt which containes
    a lot of addresses
    '''
    addresses = open("../addresses.txt", 'r')
    output = list()
    for a in addresses:
        output.append(a.strip())
    return output

def load_addresses(k):
    '''
    return a list of k addresses read from
    file addresses.txt which containes
    a lot of addresses
    '''
    addresses = open("../addresses.txt", 'r')
    output = list()
    for a in addresses:
        output.append(a.strip())
    random.shuffle(output)
    return output[0:k]

########################################################

def generate_village_database(num_people):
    '''
    Create a CSV file populated with data about
    people according to some probability distribution.
    We set probabilities simulating a small city
    social environment
    '''

    #p(person1.name == person2.name)
    p_equal_name = 0.02
    card_names = (2/p_equal_name)-1
    name_set = load_names(int(card_names))

    #p(person1.address == person2.address)
    p_equal_address = 0.2 #By using the following formula, we will have 5 addresses, the right amount of addresses in a small village
    card_address = (2/p_equal_address)-1
    address_set = load_addresses(int(card_address))

    #we consider this occupations
    occupation_cat = ["student", "retiree", "farmer", "other"]
    occupation_cat_probability = [0.15, 0.4, 0.25, 0.2]

    # age ranges
    baby_min = 0
    baby_max = 15
    young_min = 16
    young_max= 40
    medium_min = 41
    medium_max = 60
    old_min = 61
    old_max = 100

    # open the file in the write mode
    f = open('relational_db.csv', 'w', newline='')

    # create the csv writer
    writer = csv.writer(f)

    header = ['id', 'name', 'address', 'age', 'occupation']

    # write the header
    writer.writerow(header)

    # generate num_people tuples
    data = []
    autoincrement_id = 0
    for i in range(num_people):
        tuple = []
        p_name = random.sample(name_set, 1)[0]
        p_address = random.sample(address_set, 1)[0]
        p_occupation = random.choices(occupation_cat, occupation_cat_probability)[0]

        age_cat = ["baby", "young", "medium", "old"]

        #age probability depends on the occupation
        if p_occupation == "student":
            age_cat_probability = [0., 0.98, 0.02, 0.]
        
        if p_occupation == "retiree":
            age_cat_probability = [0., 0., 0.02, 0.98]

        if p_occupation == "farmer":
            age_cat_probability = [0., 0.05, 0.8, 0.15]

        if p_occupation == "other":
            age_cat_probability = [0., 0.4, 0.55, 0.05]

        p_age_category = random.choices(age_cat, age_cat_probability)[0]
        if p_age_category == "baby":
            p_age = random.randint(baby_min, baby_max)
        if p_age_category == "young":
            p_age = random.randint(young_min, young_max)
        if p_age_category == "medium":
            p_age = random.randint(medium_min, medium_max)
        if p_age_category == "old":
            p_age = random.randint(old_min, old_max)    
            
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


generate_village_database(100)