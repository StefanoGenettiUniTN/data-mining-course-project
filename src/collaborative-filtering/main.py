'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''
import database as db
import query as queryClass
import user as userClass
import hash_table as hashTableClass

import pandas as pd
import math
import itertools
from pathlib import Path

from function import retriveQuerySearchAttributes
from function import retriveQueryId
from function import getPersonProfile
from function import cosineDistance
from function import featureDict_to_featureList
from function import cosToVote
from function import frequent_value
from function import important_tuples
from function import frequent_attribute
from function import k_means_clustering
from function import plot_people_cluster
from function import clusterFrequency
from function import ageGroup
from function import tuples_frequencies
from function import attribute_frequency
from function import value_frequency
from function import expected_value_frequency
from function import expected_tuple_frequency
from function import expected_attribute_frequency

from evaluation import rmse
from evaluation import me
from evaluation import me_unvoted
from evaluation import rmse_unvoted
from evaluation import query_avg_error
from evaluation import user_avg_error
from evaluation import userVoteCurve

from file import getQueryDefinition
from file import writeOutputUtilityMatrix

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = Path("data/village/relational_db.csv")
utilityMatrixFileName = Path("data/village/utility_matrix.csv")
completeUtilityMatrixFileName = Path("data/village/utility_matrix_complete.csv")
outputUtilityMatrixFileName = Path("data/village/output.csv")
queryFileName = Path("data/village/queries.csv")

#Read database
person = db.Person(databaseFileName)

#Utility matrix
utilityMatrix = pd.read_csv(utilityMatrixFileName)

#user_recommendation[u] = dictionary such that user_recommendation[u][q1] is the
#vote recommended by the system for the user-query couple (u,q1)
user_recommendation = dict()

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
    user_obj = userClass.User(index)
    query_def = dict()  #query_def[q] = the definition of the query with id q
    sum_vote = 0

    #print("")
    #print("========================")
    #print("USER "+user_obj.getId())

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

    '''
    print("")
    print("Print user: "+str(user_obj.getId()))
    print("ft_tuple")
    print(user_obj.get_ft_tuple())
    print("ft_attribute")
    print(user_obj.get_ft_attribute())
    print("ft_value")
    print(user_obj.get_ft_value())
    print("ft_cluster")
    print(user_obj.get_ft_cluster())
    print("end print user "+str(user_obj.getId()))
    print("")
    '''

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

        #print("")
        #print("Print query: "+str(qobj.getId()))
        #print("ft_tuple")
        #print(qobj.get_ft_tuple())
        #print("ft_attribute")
        #print(qobj.get_ft_attribute())
        #print("ft_value")
        #print(qobj.get_ft_value())
        #print("ft_cluster")
        #print(qobj.get_ft_cluster())
        #print("ft_tuple_user")
        #print(qobj.get_ft_tuple_user())
        #print("ft_attribute_user")
        #print(qobj.get_ft_attribute_user())
        #print("ft_value_user")
        #print(qobj.get_ft_value_user())
        #print("ft_cluster_user")
        #print(qobj.get_ft_cluster_user())

        #print("end print query "+str(qobj.getId()))
        #print("")

    #compute content based recommendation for current user
    #about the list of query objects stored in query_to_be_voted
    predictedVotes = user_obj.queryContentBasedEvaluation(person, query_def, query_to_be_voted)

    #print("")
    #print(f"USER[{user_obj.getId()}] predicted votes")
    #print(predictedVotes)
    #print("")
    
    #store the user recommendation for the unvoted queries
    for query_vote in predictedVotes:
        user_recommendation[user_obj.getId()][query_vote] = predictedVotes[query_vote]
###

###Write the output utility matrix
for i, u in utilityMatrix.iterrows():
    for q in u.keys():
        if math.isnan(u[q]):
            utilityMatrix.at[i, q] = user_recommendation[i][q]

writeOutputUtilityMatrix(utilityMatrix, outputUtilityMatrixFileName)
###

### Evaluate algorithm performance
print("Quality Evaluation")

#complete utility matrix
completeUtilityMatrix = pd.read_csv(completeUtilityMatrixFileName)

rmse = rmse(utilityMatrix, completeUtilityMatrix)
me = me(utilityMatrix, completeUtilityMatrix)
me_unvoted = me_unvoted(user_recommendation, completeUtilityMatrix)
rmse_unvoted = rmse_unvoted(user_recommendation, completeUtilityMatrix)
print("RMSE = "+str(rmse))
print("ME = "+str(me))
print("ME UNVOTED = "+str(me_unvoted))
print("RMSE UNVOTED = "+str(rmse_unvoted))

#average error for each query
query_avg_error(user_recommendation, completeUtilityMatrix)

#average vote for each user
user_avg_error(user_recommendation, completeUtilityMatrix)

for u in user_recommendation:
    userVoteCurve(u, user_recommendation, completeUtilityMatrix)
###