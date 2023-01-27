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
import random
from pathlib import Path

from function import k_means_clustering
from function import plot_people_cluster
from function import expected_tuple_frequency
from function import expected_attribute_frequency
from function import retriveQueryId

import cluster as clusterClass
import cf_user as collaborativeFilteringUserClass
import cf_query as collaborativeFilteringQueryClass

from cf_function import updateUtilityMatrixVotes

from clustering import pearson_similarity
from clustering import query_tuple_similarity
from clustering import cluster_similarity
from clustering import query_cluster_similarity
from clustering import merge
from clustering import condense
from clustering import avgClusterQuality

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

def collaborative_filtering(_databaseFileName, _utilityMatrixFileName, _completeUtilityMatrixFileName, _outputUtilityMatrixFileName, _queryFileName, _userFileName, user_recommendation, frequentVoters, coldStartUsers):
    databaseFileName = _databaseFileName
    utilityMatrixFileName = _utilityMatrixFileName
    completeUtilityMatrixFileName = _completeUtilityMatrixFileName
    outputUtilityMatrixFileName = _outputUtilityMatrixFileName
    queryFileName = _queryFileName
    userFileName = _userFileName

    #read database
    person = db.Person(databaseFileName)

    #utility matrix
    utilityMatrix = pd.read_csv(utilityMatrixFileName)

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
        if u not in coldStartUsers: #users who did not vote any query cannot be taken into consideration
            #create new collaborative filtering user
            cfUser = collaborativeFilteringUserClass.CollaborativeFilteringUser(u)
            
            #insert the new user into a new cluster
            u_cluster_list[cluster_id] = clusterClass.Cluster(cluster_id)
            u_cluster_list[cluster_id].addComponent(cfUser)
            cfUser.setCluster(cluster_id)
            cluster_id += 1

            #initialize user recommendation dictionary for the current user
            if u not in user_recommendation:
                user_recommendation[u] = dict()

            if u in frequentVoters: 
                #--> the user has been already completed with collaborative filtering recommendation
                for q in col.keys():
                    if math.isnan(col[q]):
                        #add the query which the target user voted to the voted query list
                        cfUser.addVotedEntity(q, user_recommendation[u][q])
                        
                        #add the target user which voted the query
                        collaborativeFilteringQuery[q].addVotedEntity(cfUser.id, user_recommendation[u][q])
                    else:
                        #add the query which the target user voted to the voted query list
                        cfUser.addVotedEntity(q, col[q])
                        
                        #add the target user which voted the query
                        collaborativeFilteringQuery[q].addVotedEntity(cfUser.id, col[q])
            else:
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

    #update utility matrix votes
    updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

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

    ###keep merging until the utility matrix is not complete
    done = False    #done==True IFF all the queries are voted by all the users
    while not done:
        done = True

        #compute user clusters quality and query clusters quality
        userClusterQuality = avgClusterQuality(u_cluster_list, pearson_similarity)
        queryClusterQuality = avgClusterQuality(q_cluster_list, pearson_similarity)

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
                        if currentSimilarity>bestSimilarity:
                            bestClusterId = cluster
                            bestSimilarity = currentSimilarity
                
                if bestClusterId!=-1:
                    u_cluster_list[cluster_id] =  merge(clusterUncompleteUser, u_cluster_list[bestClusterId], cluster_id)
                    u_cluster_list.pop(clusterUncompleteUser.id, None)
                    u_cluster_list.pop(bestClusterId, None)
                    cluster_id += 1
                    #for c in u_cluster_list:
                    #    print(u_cluster_list[c])
                    #print("---")
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

        if not done:
            #update utility matrix votes
            updateUtilityMatrixVotes(user_recommendation, u_cluster_list, q_cluster_list, collaborativeFilteringUser, collaborativeFilteringQuery)

    ##########