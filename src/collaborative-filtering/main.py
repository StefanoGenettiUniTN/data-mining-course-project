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

import cluster as clusterClass
import cf_user as collaborativeFilteringUserClass
import cf_query as collaborativeFilteringQueryClass

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

from cf_function import updateUtilityMatrixVotes

from evaluation import rmse
from evaluation import me
from evaluation import me_unvoted
from evaluation import rmse_unvoted
from evaluation import query_avg_error
from evaluation import user_avg_error
from evaluation import userVoteCurve

from file import getQueryDefinition
from file import writeOutputUtilityMatrix

from clustering import user_pearson_similarity
from clustering import query_tuple_similarity
from clustering import cluster_similarity
from clustering import query_cluster_similarity
from clustering import merge
from clustering import condense

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = Path("data/university/relational_db.csv")
utilityMatrixFileName = Path("data/university/utility_matrix.csv")
completeUtilityMatrixFileName = Path("data/university/utility_matrix_complete.csv")
outputUtilityMatrixFileName = Path("data/university/output.csv")
queryFileName = Path("data/university/queries.csv")
userFileName = Path("data/university/users.csv")

#read database
person = db.Person(databaseFileName)

#utility matrix
utilityMatrix = pd.read_csv(utilityMatrixFileName)

#user_recommendation[u] = dictionary such that user_recommendation[u][q1] is the
#vote recommended by the system for the user-query couple (u,q1)
user_recommendation = dict()

#collaborativeFilteringUser[u] = collaborative filtering user object
collaborativeFilteringUser = dict()

#collaborativeFilteringQuery[q] = collaborative filtering query object
collaborativeFilteringQuery = dict()

#cluser autoincrement unique identifier
cluster_id = 0

#u_cluster_list[c] = user cluster object with identifier c
u_cluster_list = dict()

#q_cluster_list[c] = query cluster object with identifier c
q_cluster_list = dict()

#number of users
numUser = 0

#number of queries
numQuery = 0

###initialization of
# - dictionary u_completed
# - dictionary u_cluster
# - dictionary u_cluster_list
# - collaborativeFilteringUser
for u, col in utilityMatrix.iterrows():
    #create new collaborative filtering user
    cfUser = collaborativeFilteringUserClass.CollaborativeFilteringUser(u)
    
    #insert the new user into a new cluster
    u_cluster_list[cluster_id] = clusterClass.Cluster(cluster_id)
    u_cluster_list[cluster_id].addComponent(cfUser)
    cfUser.setCluster(cluster_id)
    cluster_id += 1

    #initialize user recommendation dictionary for the current user
    user_recommendation[u] = dict()

    sum_vote = 0
    for q in col.keys():
        if math.isnan(col[q]):
            #add the query which the target user did not vote to the unvoted query list
            cfUser.addUnvotedEntity(q)
        else:
            #add the query which the target user voted to the voted query list
            cfUser.addVotedEntity(q, col[q])
            sum_vote += col[q]

    #compute vote average
    cfUser.computeAvgVote()

    collaborativeFilteringUser[u] = cfUser
    numUser += 1

    if len(cfUser.unvotedEntities) == 0:
        cfUser.completeEntity()

###end initialization of dictionary user data structures

#for user1, user2 in itertools.product(collaborativeFilteringUser.keys(), collaborativeFilteringUser.keys()):
#    print(f"similarity between user {user1} and user {user2} = {user_pearson_similarity(collaborativeFilteringUser[user1], collaborativeFilteringUser[user2])}")

###initialization of
# - dictionary q_cluster
# - dictionary q_cluster_list
duplicates = dict()
queryFile = open(queryFileName, 'r')
for q in queryFile:
    query = q[:-1] #otherwise each query ends with \n
    query_id = retriveQueryId(query)
    query_definition = query.split(",")[1:]
    query_definition.sort()

    #create new collaborative filtering query
    cfQuery = collaborativeFilteringQueryClass.CollaborativeFilteringQuery(query_id, str(query_definition))

    #check if there is a duplicate of this query
    if str(query_definition) in duplicates:
        duplicateCluster = duplicates[str(query_definition)]
        q_cluster_list[duplicateCluster].addComponent(cfQuery)
        cfQuery.setCluster(duplicateCluster)
    else:
        #insert the new query into a new cluster
        q_cluster_list[cluster_id] = clusterClass.Cluster(cluster_id)
        q_cluster_list[cluster_id].addComponent(cfQuery)
        cfQuery.setCluster(cluster_id)
        duplicates[str(query_definition)] = cluster_id
        cluster_id += 1

    collaborativeFilteringQuery[query_id] = cfQuery
    numQuery += 1
queryFile.close()
###end initialization of dictionary query data structures

#Debug: print query clusters
#for cluster in q_cluster_list:
#    print(q_cluster_list[cluster])

#update utility matrix votes
updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

#cluster users until the number of user clusters is
#equal to the number of users divided by two
numUserCluster = numUser
while numUserCluster>(numUser/2):
    resultCondense = condense(u_cluster_list, user_pearson_similarity, cluster_id)
    if resultCondense==-1:
        print("Fatal error. Function condense returned -1.")
        exit(-1)
    numUserCluster -= 1
    cluster_id += 1

#Debug print specific user
#for q in collaborativeFilteringUser["u8"].votedEntities:
#    if q in collaborativeFilteringUser["u7"].votedEntities:
#        print(f"user u8 vote query {q} = {collaborativeFilteringUser['u8'].votedEntities[q]}")
#        print(f"user u7 vote query {q} = {collaborativeFilteringUser['u7'].votedEntities[q]}")

#Debug: print user clusters
for cluster in u_cluster_list:
    print(u_cluster_list[cluster])

#Debug: print user recommendations
#for u in collaborativeFilteringUser:
#    print(f"user {u} recommendations")
#    print(user_recommendation[u])
#    if collaborativeFilteringUser[u].completed:
#        print(f"user {u} completed")
###

exit(0)

###cluster queries according to tuple similarity
numCluster = numQuery

for cluster in q_cluster_list:
    print(q_cluster_list[cluster])

#first of all, agglomerate identical queries
thereAreDuplicates = True
while thereAreDuplicates:
    thereAreDuplicates = False
    clusterCouples = itertools.combinations(q_cluster_list.keys(),2)
    for cluster1_id, cluster2_id in clusterCouples:
        if cluster1_id in q_cluster_list and cluster2_id in q_cluster_list:
            cluster1 = q_cluster_list[cluster1_id]
            cluster2 = q_cluster_list[cluster2_id]
            clusterSimilarity = query_cluster_similarity(cluster1, cluster2, person)
            if clusterSimilarity == 1:
                q_cluster_list[cluster_id] = merge(cluster1, cluster2, cluster_id)
                q_cluster_list.pop(cluster1_id, None)
                q_cluster_list.pop(cluster2_id, None)
                cluster_id += 1
                numCluster -= 1
                thereAreDuplicates = True
###end cluster queries according to tuple similarity

for cluster in q_cluster_list:
    print(q_cluster_list[cluster])

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