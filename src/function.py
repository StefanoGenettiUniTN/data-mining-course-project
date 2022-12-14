'''
In this file we implement some useful functions
'''

import numpy as np
import math
from numpy.linalg import norm

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


def getPersonProfile(tuple):

    young_max_age = 20
    medium_max_age = 60
    old_max_age = 150 

    p = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

    f = 0

    if tuple["name"]=="ste":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["name"]=="pie":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["name"]=="fab":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["name"]=="ero":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["name"]=="vit":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["name"]=="mat":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["address"]=="via1":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["address"]=="via2":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["address"]=="via3":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["address"]=="via4":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["address"]=="via5":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["age"]<=young_max_age:
        p[f] = 1
    else:
        p[f] = 0
    
    f += 1

    if tuple["age"]>young_max_age and tuple["age"]<=medium_max_age:
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["age"]>medium_max_age:
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["occupation"]=="imp1":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["occupation"]=="sar":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if tuple["occupation"]=="tec":
        p[f] = 1
    else:
        p[f] = 0

    return p


def featureDict_to_featureList(item_profile):
    '''
    Sometimes the item profile is a dictionary
    such that:
        item_profile[f] = value for feature f
    
    This function converts a dictionary item
    profile into a list item profile
    '''
    output = [item_profile[f] for f in item_profile]
    print("featureDict_to_featureList")
    print("input: "+str(item_profile))
    print("output: "+str(output))
    return output


def cosineDistance(item1_profile, item2_profile):
    '''
    item1_profile, item2_profile are two 1-D vectors
    '''
    print("cosineDistance")
    print("item1: "+str(item1_profile))
    print("item2: "+str(item2_profile))
    item1 = np.array(item1_profile)
    item2 = np.array(item2_profile)

    return np.dot(item1,item2)/(norm(item1)*norm(item2))

def cosToVote(cosine_distance):
    '''
    in content based recommendation, given the cosine distance between the
    user profile and the item profile we have to retrive the expected user
    vote. We proceed as follows:

    i) First we scale the cosine_distance in range [0,1]:
        x = (val - min)/(max-min)
        x = (cosine_distance+1)/(1+1)
    
    ii) Then we scale x in range [1,5]
        mark = 4x + 1
    '''
    x = (cosine_distance+1)/2
    return round(4*x+1)


def rmse(u1, u2):
    '''
    Input: utility matrix u1, utility matrix u2
    Output: root mean squared error between the two
            utility matrixes. Typically the comparison
            is between the groundtruth and the predicted
            utility matrix
    '''
    rmse = 0
    card_votes = 0
    for query in u1:
        for index, vote in u1[query].items():
            vote_u1 = vote
            vote_u2 = u2.at[index, query]
            
            rmse += (vote_u1-vote_u2)**2
            card_votes += 1
    
    return math.sqrt(rmse/card_votes)
