'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''

import database as db

databaseFile = "../data/relational_db.csv"

#Read database
person = db.Person(databaseFile)

print(person.query("q1821,age=19"))