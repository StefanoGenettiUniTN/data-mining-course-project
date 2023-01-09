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
import random

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

from clustering import pearson_similarity
from clustering import query_tuple_similarity
from clustering import cluster_similarity
from clustering import query_cluster_similarity
from clustering import merge
from clustering import condense
from clustering import avgClusterQuality

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = Path("data/village/relational_db.csv")
utilityMatrixFileName = Path("data/village/utility_matrix.csv")
completeUtilityMatrixFileName = Path("data/village/utility_matrix_complete.csv")
outputUtilityMatrixFileName = Path("data/village/output.csv")
queryFileName = Path("data/village/queries.csv")
userFileName = Path("data/village/users.csv")

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
    cfQuery = collaborativeFilteringQueryClass.CollaborativeFilteringQuery(query_id, query)

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

    for q in col.keys():
        if math.isnan(col[q]):
            #add the query which the target user did not vote to the unvoted query list
            cfUser.addUnvotedEntity(q)

            #add the user which dit not vote the query to the unvoted user list
            collaborativeFilteringQuery[q].addUnvotedEntity(cfUser.id)
        else:
            #add the query which the target user voted to the voted query list
            cfUser.addVotedEntity(q, col[q])
            
            #add the target user which voted the query
            collaborativeFilteringQuery[q].addVotedEntity(cfUser.id, col[q])

    collaborativeFilteringUser[u] = cfUser
    numUser += 1

    if len(cfUser.unvotedEntities) == 0:
        cfUser.completeEntity()

###end initialization of dictionary user data structures

#Debug: print query clusters
#for cluster in q_cluster_list:
#    print(q_cluster_list[cluster])

#update utility matrix votes
updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

'''
for q in collaborativeFilteringUser['u9'].votedEntities:
    if q in collaborativeFilteringUser['u4'].votedEntities:
        print(f"query {q}:")
        print("user4")
        print(collaborativeFilteringUser['u4'].votedEntities[q])
        print("user9")
        print(collaborativeFilteringUser['u9'].votedEntities[q])
        print("===")
print("")
for q in collaborativeFilteringUser['u8'].votedEntities:
    if q in collaborativeFilteringUser['u2'].votedEntities:
        print(f"query {q}:")
        print("user2")
        print(collaborativeFilteringUser['u2'].votedEntities[q])
        print("user8")
        print(collaborativeFilteringUser['u8'].votedEntities[q])
        print("===")

for u1, u2 in itertools.combinations(collaborativeFilteringUser, 2):
    print(f"[{u1}][{u2}] = {pearson_similarity(collaborativeFilteringUser[u1], collaborativeFilteringUser[u2])}")

'''

#cluster users until the number of user clusters is
#equal to the number of users divided by two
numUserCluster = numUser
while numUserCluster>(numUser/2):
    resultCondense = condense(u_cluster_list, pearson_similarity, cluster_id)
    if resultCondense==-1:
        print("Fatal error. Function condense returned -1.")
        exit(-1)
    numUserCluster -= 1
    cluster_id += 1

#Debug: print user clusters
for cluster in u_cluster_list:
    print(u_cluster_list[cluster])

#cluster queries until the number of query clusters is
#equal to the number of queries divided by two
numQueryCluster = len(q_cluster_list)
while numQueryCluster>(numQuery/2):
    resultCondense = condense(q_cluster_list, pearson_similarity, cluster_id)
    if resultCondense==-1:
        print("Fatal error. Function condense returned -1.")
        exit(-1)
    numQueryCluster -= 1
    cluster_id += 1

#update utility matrix votes
updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

#Debug: print query clusters
#for cluster in q_cluster_list:
#    print(q_cluster_list[cluster])

###keep merging until the utility matrix is not complete
done = False    #done==True IFF all the queries are voted by all the users
while not done:
    done = True

    #compute user clusters quality and query clusters quality
    userClusterQuality = avgClusterQuality(u_cluster_list, pearson_similarity)
    queryClusterQuality = avgClusterQuality(q_cluster_list, pearson_similarity)

    print(f"userClusterQuality = {userClusterQuality}")
    print(f"queryClusterQuality = {queryClusterQuality}")
    print(f"query clusters: {len(q_cluster_list)}")
    print(f"user clusters: {len(u_cluster_list)}")
    print(f"query clusters/num_query: {len(q_cluster_list)/numQuery}")
    print(f"user clusters/num_query: {len(u_cluster_list)/numUser}")

    #with probability p, change the decision
    p = 0.33
    if random.random() < p:
        if userClusterQuality > queryClusterQuality:
            userClusterQuality = queryClusterQuality-1
        else:
            queryClusterQuality = userClusterQuality-1

    #avoid single user cluster
    if len(u_cluster_list) == 2:
        queryClusterQuality = userClusterQuality+100

    if userClusterQuality > queryClusterQuality:
        #merge user clusters because their quality is better
        uncompletedUser = -1
        collaborativeFilteringUserList = list(collaborativeFilteringUser.keys())
        random.shuffle(collaborativeFilteringUserList)
        for user_id in collaborativeFilteringUserList:
            user_obj = collaborativeFilteringUser[user_id]
            if not user_obj.completed:
                done=False
                uncompletedUser = user_id
                break
        
        if not done:
            uncompletedUserObj = collaborativeFilteringUser[uncompletedUser]
            clusterUncompleteUser = u_cluster_list[uncompletedUserObj.cluster]

            #find the best cluster to be merged with the cluster of the uncompleted user
            bestClusterId = -1
            bestSimilarity = float('-inf')
            for cluster in u_cluster_list:
                if cluster != clusterUncompleteUser.id:
                    cluster_obj = u_cluster_list[cluster]

                    currentSimilarity = cluster_similarity(clusterUncompleteUser, cluster_obj, pearson_similarity)

                    #if clusterUncompleteUser.id == collaborativeFilteringUser['u9'].cluster:
                    #    print(f"similarity cluster {clusterUncompleteUser.id} con {cluster} = {currentSimilarity}")

                    if currentSimilarity>bestSimilarity:
                        bestClusterId = cluster
                        bestSimilarity = currentSimilarity
            
            if bestClusterId!=-1:
                u_cluster_list[cluster_id] =  merge(clusterUncompleteUser, u_cluster_list[bestClusterId], cluster_id)
                u_cluster_list.pop(clusterUncompleteUser.id, None)
                u_cluster_list.pop(bestClusterId, None)
                cluster_id += 1
                #Debug: print user clusters
                for cluster in u_cluster_list:
                    print(u_cluster_list[cluster])
                print("---")
                print("merge user")
    else:
        #merge query clusters because their quality is better
        uncompletedQuery = -1
        collaborativeFilteringQueryList = list(collaborativeFilteringQuery.keys())
        random.shuffle(collaborativeFilteringQueryList)
        for query_id in collaborativeFilteringQueryList:
            query_obj = collaborativeFilteringQuery[query_id]
            if not query_obj.completed:
                done=False
                uncompletedQuery = query_id
                break
        
        if not done:
            uncompletedQueryObj = collaborativeFilteringQuery[uncompletedQuery]
            clusterUncompleteQuery = q_cluster_list[uncompletedQueryObj.cluster]

            #find the best cluster to be merged with the cluster of the uncompleted query
            bestClusterId = -1
            bestSimilarity = float('-inf')
            for cluster in q_cluster_list:
                if cluster != clusterUncompleteQuery.id:
                    cluster_obj = q_cluster_list[cluster]

                    currentSimilarity = cluster_similarity(clusterUncompleteQuery, cluster_obj, pearson_similarity)

                    if currentSimilarity>bestSimilarity:
                        bestClusterId = cluster
                        bestSimilarity = currentSimilarity
            
            if bestClusterId!=-1:
                q_cluster_list[cluster_id] =  merge(clusterUncompleteQuery, q_cluster_list[bestClusterId], cluster_id)
                q_cluster_list.pop(clusterUncompleteQuery.id, None)
                q_cluster_list.pop(bestClusterId, None)
                cluster_id += 1
                print("merge query")

    if not done:
        #update utility matrix votes
        updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

##########

#Debug: print user clusters
#for cluster in u_cluster_list:
#    print(u_cluster_list[cluster])

#Debug: print user recommendations
#for u in collaborativeFilteringUser:
#    print(f"user {u} recommendations")
#    print(user_recommendation[u])
#    if collaborativeFilteringUser[u].completed:
#        print(f"user {u} completed")
###

###cluster queries according to tuple similarity
'''
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
'''
###end cluster queries according to tuple similarity

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