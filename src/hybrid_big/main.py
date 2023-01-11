'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''
import pandas as pd
import itertools
from pathlib import Path
from random import sample
import math

from recommendation import content_based
from recommendation import collaborative_filtering

from evaluation import rmse
from evaluation import me
from evaluation import me_unvoted
from evaluation import rmse_unvoted
from evaluation import query_avg_error
from evaluation import user_avg_error
from evaluation import userVoteCurve

from function import retriveQueryId
import cluster as clusterClass

databaseFileName = Path("data/big/relational_db.csv")
utilityMatrixFileName = Path("data/big/utility_matrix.csv")
completeUtilityMatrixFileName = Path("data/big/utility_matrix_complete.csv")
outputUtilityMatrixFileName = Path("data/big/output.csv")
queryFileName = Path("data/big/queries.csv")
userFileName = Path("data/big/users.csv")

#user_recommendation[u] = dictionary such that user_recommendation[u][q1] is the
#vote recommended by the system for the user-query couple (u,q1)
user_recommendation = dict()

##############################################################################
#partition user in three sets:
#   i) users who voted nothing (cold start)
#  ii) users who voted a lot
# iii) users who voted few queries
##############################################################################
coldStartUsers = set()
frequentVoters = set()
rareVoters = set()
utilityMatrix = pd.read_csv(utilityMatrixFileName) #utility matrix

for user, votes in utilityMatrix.iterrows():
    votedQueries = 0
    totQueries = 0
    for query in votes.keys():
        if not math.isnan(votes[query]):
            votedQueries += 1
        totQueries += 1
    
    if votedQueries==0:
        coldStartUsers.add(user)
    elif votedQueries > totQueries/2:
        frequentVoters.add(user)
    else:
        rareVoters.add(user)

print("USER WHO DID NOT VOTE ANY QUERY")
print(coldStartUsers)
print("")
print("FREQUENT VOTERS")
print(frequentVoters)
print("")
print("RARE VOTERS")
print(rareVoters)
print("")
###

##############################################################################
#process frequent voters with content based filtering
##############################################################################
content_based(  databaseFileName,                       #database file name
                utilityMatrixFileName,                  #utility matrix file name
                completeUtilityMatrixFileName,          #complete utility matrix file name
                outputUtilityMatrixFileName,            #output utility matrix file name
                queryFileName,                          #query log file name
                user_recommendation,                    #user recommendation obj
                frequentVoters                          #frequent voters list
            )
#Uncomment to measure conly collaborative filtering performance
#for user, votes in utilityMatrix.iterrows():
#    if user in frequentVoters:
#        user_recommendation[user] = dict()
#        for query in votes.keys():
#            if math.isnan(votes[query]):
#                user_recommendation[user][query] = 50

##############################################################################

print("content based done")

##############################################################################
#process rare voters with collaborative filtering
##############################################################################
collaborative_filtering(    databaseFileName,                       #database file name
                            utilityMatrixFileName,                  #utility matrix file name
                            completeUtilityMatrixFileName,          #complete utility matrix file name
                            outputUtilityMatrixFileName,            #output utility matrix file name
                            queryFileName,                          #query log file name
                            userFileName,                           #user list file name
                            user_recommendation,                    #user recommendation obj
                            frequentVoters,                         #frequent voters list
                            coldStartUsers                          #frequent voters list
                        )

##############################################################################

print("collaborative filtering done")

##############################################################################
#solve people who did not vote anything
##############################################################################

# i. sample some users at random
randomFrequentUserSample = sample(frequentVoters, min(10, len(frequentVoters)))
randomRareUserSample = sample(rareVoters, min(10, len(rareVoters)))

# ii. cluster together duplicate queries according to their definition
query_cluster = dict()          #query_cluster[query_id] = in which cluster the query is
query_cluster_list = dict()     #query_cluster_list[cluster_id] = cluster object which containes queries
cluster_autoincrement_id = 0    #autoincrement cluster id

duplicates = dict()
queryFile = open(queryFileName, 'r')
for q in queryFile:
    query = q[:-1] #otherwise each query ends with \n
    query_id = retriveQueryId(query)
    query_definition = query.split(",")[1:]
    query_definition.sort()

    #check if there is a duplicate of this query
    if str(query_definition) in duplicates:
        duplicateCluster = duplicates[str(query_definition)]
        query_cluster_list[duplicateCluster].addComponent(query_id)
        query_cluster[query_id] = duplicateCluster
    else:
        #insert the new query into a new cluster
        query_cluster_list[cluster_autoincrement_id] = clusterClass.Cluster(cluster_autoincrement_id)
        query_cluster_list[cluster_autoincrement_id].addComponent(query_id)
        query_cluster[query_id] = cluster_autoincrement_id
        duplicates[str(query_definition)] = cluster_autoincrement_id
        cluster_autoincrement_id += 1
queryFile.close()

# iii. assign an approximate average vote to each query cluster
query_cluster_vote = dict() #query_cluster_vote[c] = expected vote for queries belonging to cluster c
for cluster_id in query_cluster_list:
    cluster_obj = query_cluster_list[cluster_id]

    #sample a random component from the cluster
    cluster_component = sample(cluster_obj.components, 1)[0]
    
    #compute user average vote
    sumVote = 0
    numVote = 0
    for u in randomFrequentUserSample:
        if cluster_component in user_recommendation[u]:
            sumVote += user_recommendation[u][cluster_component]
        else:
            sumVote += utilityMatrix.at[u,cluster_component]
        numVote += 1
    for u in randomRareUserSample:
        if cluster_component in user_recommendation[u]:
            sumVote += user_recommendation[u][cluster_component]
        else:
            sumVote += utilityMatrix.at[u,cluster_component]
        numVote += 1
    
    avgVote = sumVote/numVote
    query_cluster_vote[cluster_id] = avgVote

#complete utility matrix rows for cold start users
for u in coldStartUsers:
    user_recommendation[u] = dict()
    for cluster_id in query_cluster_list:
        clusterVote = query_cluster_vote[cluster_id]
        cluster_obj = query_cluster_list[cluster_id]

        for cluster_component in cluster_obj.components:
            user_recommendation[u][cluster_component] = clusterVote

##############################################################################

print("cold start users completed")

##############################################################################
### Evaluate algorithm performance
##############################################################################
print("Quality Evaluation")

#complete utility matrix
completeUtilityMatrix = pd.read_csv(completeUtilityMatrixFileName)

me_unvoted = me_unvoted(user_recommendation, completeUtilityMatrix)
rmse_unvoted = rmse_unvoted(user_recommendation, completeUtilityMatrix)
print("ME = "+str(me_unvoted))
print("RMSE = "+str(rmse_unvoted))

#average error for each query
query_avg_error(user_recommendation, completeUtilityMatrix)

#average vote for each user
user_avg_error(user_recommendation, completeUtilityMatrix)

for u in user_recommendation:
    userVoteCurve(u, user_recommendation, completeUtilityMatrix)
###

##############################################################################à