'''
content based filtering --> execute content based recommendation system
collaborative filtering --> execute collaborative filtering recommendation system
'''

import database as db
import query as queryClass
import user as userClass
import hash_table as hashTableClass

import pandas as pd
import math
import itertools
from pathlib import Path

from function import k_means_clustering
from function import plot_people_cluster
from function import expected_tuple_frequency
from function import expected_attribute_frequency

from file import getQueryDefinition

def content_based(_databaseFileName, _utilityMatrixFileName, _completeUtilityMatrixFileName, _outputUtilityMatrixFileName, _queryFileName, user_recommendation, frequentVoters):
    databaseFileName = _databaseFileName
    utilityMatrixFileName = _utilityMatrixFileName
    completeUtilityMatrixFileName = _completeUtilityMatrixFileName
    outputUtilityMatrixFileName = _outputUtilityMatrixFileName
    queryFileName = _queryFileName

    #Read database
    person = db.Person(databaseFileName)

    #Utility matrix
    utilityMatrix = pd.read_csv(utilityMatrixFileName)

    #Compute tuple importance, a tuple is important if it appears in a lot of results
    expectedTupleFrequency = expected_tuple_frequency(person, queryFileName)

    #Compute search attribute importance, an attribute is important if it appears in a lot of queries
    expectedAttributeFrequency = expected_attribute_frequency(queryFileName)

    # Clustering of data in Person
    num_cluster_person = 5
    person.table = k_means_clustering(person, num_cluster_person)
    #plot_people_cluster(person.table, num_cluster_person)

    ### Initialize user profiles and complete utility matrix with
    ### content based filtering
    for index, v in utilityMatrix.iterrows():
        if index in frequentVoters:
            user_obj = userClass.User(index)
            query_def = dict()  #query_def[q] = the definition of the query with id q
            sum_vote = 0

            user_recommendation[user_obj.getId()] = dict()

            for q in v.keys():
                if math.isnan(v[q]):
                    #add the query which the target user did not vote to the unvoted query list
                    user_obj.addUnVotedQuery(q)
                    query_def[q] = getQueryDefinition(queryFileName, q)
                else:
                    #add the query which the target user voted to the voted query list
                    user_obj.addVotedQuery(q, v[q])
                    sum_vote += v[q]
                    query_def[q] = getQueryDefinition(queryFileName, q)

            #compute vote average
            num_votes = len(user_obj.getVotedQueries())
            if num_votes > 0:
                user_obj.setAvgVote(sum_vote/num_votes)
            else:
                user_obj.setAvgVote(-1)
        
            #compute user profile
            user_obj.computeUserProfile(person, query_def)

            #compute query profile of the unvoted queries
            query_to_be_voted = list()
            for q in user_obj.getUnVotedQueries():
                #get query definition
                qdef = query_def[q]
                
                #instantiate query object
                qobj = queryClass.Query(qdef)

                #computer query profile
                qobj.computeQueryProfile(person, expectedTupleFrequency, expectedAttributeFrequency, user_obj)

                query_to_be_voted.append(qobj)

            #compute content based recommendation for current user
            #about the list of query objects stored in query_to_be_voted
            predictedVotes = user_obj.queryContentBasedEvaluation(person, query_def, query_to_be_voted)
            
            #store the user recommendation for the unvoted queries
            for query_vote in predictedVotes:
                user_recommendation[user_obj.getId()][query_vote] = predictedVotes[query_vote]
    ###