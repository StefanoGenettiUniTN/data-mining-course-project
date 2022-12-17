'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''
import database as db
import query as queryClass
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
from function import rmse
from function import frequent_value
from function import important_tuples
from function import frequent_attribute
from function import k_means_clustering
from function import plot_people_cluster

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = Path("../../data/relational_db.csv")
utilityMatrixFileName = Path("../../data/utility_matrix.csv")
queryFileName = Path("../../data/queries.csv")

#Read database
person = db.Person(databaseFileName)

#Utility matrix
utilityMatrix = pd.read_csv(utilityMatrixFileName)

###
# 
# Preprocessing
#
###

# Search most important tuples
# Tuples which appear more then the others in the resultset of queries
mostFrequentTuples = important_tuples(person, queryFileName)

# Search frequently search attributes
# Attribute combinations searched by users which appear more then a specified threshold
frequentAttributes = frequent_attribute(queryFileName)

# Search values which appear frequently in the resultsets of the queries
# Values that appear frequently in query result sets
frequentValues = frequent_value(person, queryFileName)                 

print("Most frequent tuple: "+str(mostFrequentTuples))
print("")
print("Most frequent attributes: "+str(frequentAttributes))
print("")
print("Most frequent values: "+str(frequentValues))
print("")

# Clustering of data in Person
num_cluster_person = 2
person.table = k_means_clustering(person, num_cluster_person)
print(person.table)
plot_people_cluster(person.table, num_cluster_person)
###

###Count number of votes of each user to partition users according to their voting rate
voters = dict()             #voters[i] = list of queries voted by user i
frequent_voters = list()    #users who voted a lot
unfrequent_voters = list()  #users who voted really few (or zero) queries
high_voters_threshold = 4
low_voters_threshold = 2

for index, v in utilityMatrix.iterrows():
    if index not in voters:
        voters[index] = []

    for q in query_identifiers:
        if math.isnan(v[q])==False:
            voters[index].append((q,v[q]))

for u in voters:
    num_votes = len(voters[u])
    if num_votes >= high_voters_threshold:
        frequent_voters.append(u)
    
    if num_votes <= low_voters_threshold:
        unfrequent_voters.append(u)
###

###Complete utility matrix of frequent users with content based filtering
for u in frequent_voters:
    target_user_profile = dict()    #feature vector for the current user [importantTuple1, importantTuple2, ..., importantTupleN, frequentAttribute1, frequentAttribute2, ..., frequentAttributeN, frequentValue1, frequentValue2, ..., frequentValueN, cluster1, cluster2, ..., clusterK]
    featureCardinality = dict()     #featureCardinality[i] represents how many times the target user voted the feature i
    target_user_index = u           #id of the current user
    
    print("studying user: "+str(target_user_index))
    
    #for each feature, initialize target_user_profile data structure
    # i. important tuples
    for t in mostFrequentTuples:
        target_user_profile["f1"+str(t)] = 0
        featureCardinality["f1"+str(t)] = 0

    # ii. frequent attributes
    for fa in frequentAttributes:
        target_user_profile["f2"+str(fa)] = 0
        featureCardinality["f2"+str(fa)] = 0

    # iii. frequent values
    for fv in frequentValues:
        target_user_profile["f3"+str(fv)] = 0
        featureCardinality["f3"+str(fv)] = 0

    # iv. cluster
    for c in range(n_cluster_k):
        target_user_profile["f4"+str(c)] = 0
        featureCardinality["f4"+str(c)] = 0

    #print(target_user_profile)

    #...end initialization

    query_votes = dict()            #query_votes[i] = vote assigned by the target user to query i
    target_user_queries = list()    #list of Query objects: the list contains the query voted by the target user
    normalized_query_votes = dict() #same as query_votes but we subtract the average of the user
    vote_sum = 0

    #retrive query votes
    for q in voters[target_user_index]:
        query_votes[q[0]] = q[1]
        vote_sum += q[1]

    avg_vote = vote_sum/len(query_votes)    #normalization
    
    for q in query_votes:
        normalized_query_votes[q] = query_votes[q]-avg_vote

    queryFile = open(queryFileName, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        query_id = retriveQueryId(query)

        if query_id in query_votes: #O(1) the target user voted query query_id

            query_obj = queryClass.Query(query_id)  #the query structure is described by a query object
            
            #add research attributes to the query object
            queryAttibuteSet = retriveQuerySearchAttributes(query)
            for attr in queryAttibuteSet:
                query_obj.addParameter(attr)
                # update target user profile with information about frequent attributes
                if attr in frequentAttributes:
                    target_user_profile["f2"+str(attr)] += normalized_query_votes[query_obj.getId()]
                    featureCardinality["f2"+str(attr)] += 1

            #retrive query result
            queryResult = person.query(str(query_obj))

            cluster_frequency = dict()          #cluster_frequency[i] = number_of_tuples_belonging_to_cluster_i / tot_tuples
            observed_frequent_values = set()    #the set contains the frequent values which have been seen in the query result set
            observed_clusters = set()           #the set contains the clusters which have been seen in the query result set
            for index, tuple in queryResult.iterrows():
                tuple_id = int(tuple['id'])
                tuple_name = tuple['name']
                tuple_address = tuple['address']
                tuple_occupation = tuple['occupation']

                #update target_user_profile
                # important tuples
                if tuple_id in mostFrequentTuples:
                    target_user_profile["f1"+str(tuple_id)] += normalized_query_votes[query_obj.getId()]
                    featureCardinality["f1"+str(tuple_id)] += 1

                # frequent values
                if tuple_name in frequentValues:
                    target_user_profile["f3"+str(tuple_name)] += (1/len(queryResult.index))*normalized_query_votes[query_obj.getId()]
                    observed_frequent_values.add(tuple_name)
                if tuple_address in frequentValues:
                    target_user_profile["f3"+str(tuple_address)] += (1/len(queryResult.index))*normalized_query_votes[query_obj.getId()]
                    observed_frequent_values.add(tuple_address)
                if tuple_occupation in frequentValues:
                    target_user_profile["f3"+str(tuple_occupation)] += (1/len(queryResult.index))*normalized_query_votes[query_obj.getId()]
                    observed_frequent_values.add(tuple_occupation)
                #...end update target_user_profile

                #update cluster frequency
                tuple_profile = getPersonProfile(tuple)
                tuple_cluster = kmeans.predict([tuple_profile])
                target_user_profile["f4"+str(tuple_cluster[0])] += (1/len(queryResult.index))*normalized_query_votes[query_obj.getId()]
                observed_clusters.add(tuple_cluster[0])

            #update the counter about how many times user[i] voted a frequent value
            #(  this information is useful for the computation of the average mark
            #   assigned by the user to the frequent value)
            for ofv in observed_frequent_values:
                featureCardinality["f3"+str(ofv)] += 1

            #update the counter about how many times user[i] voted a cluster
            #(  this information is useful for the computation of the average mark
            #   assigned by the user to the cluster)
            for oc in observed_clusters:
                featureCardinality["f4"+str(oc)] += 1

            #print(target_user_profile)

    #complete the target_user_profile
    #computing the avg vote for each query feature
    for f in featureCardinality:
        if featureCardinality[f]>0:
            target_user_profile[f] = target_user_profile[f]/featureCardinality[f]

    #print("final user profile")
    #print(target_user_profile)

    queryFile.close()

    #print(f"complete utilitiy matrix row of user {target_user_index} using content based recommendation")
    queryWithoutVote = []       #assumption:
                                #   1) there are few queries without vote;
                                #   2) the utility matrix and the query file are huge, it is better to read them only one time
    for q in utilityMatrix:
        if math.isnan(utilityMatrix.loc[target_user_index][q]):
            #query q has no vote assigned by the target user --> we estimate user preference for query q
            #with a content based approach
            queryWithoutVote.append(q)
    
    queryFile = open(queryFileName, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        query_id = retriveQueryId(query)

        if query_id in queryWithoutVote:            #O(1) the target user DID NOT vote query query_id
            query_obj = queryClass.Query(query_id)  #the query structure is described by a query object

            target_query_profile = dict()   #feature vector for the current query [importantTuple1, importantTuple2, ..., importantTupleN, frequentAttribute1, frequentAttribute2, ..., frequentAttributeN, frequentValue1, frequentValue2, ..., frequentValueN, cluster1, cluster2, ..., clusterK]
            
            #print(f"predicting opinion of user {target_user_index} about query {query_id}")
            
            #for each feature, initialize target_query_profile data structure
            # i. important tuples
            for t in mostFrequentTuples:
                target_query_profile["f1"+str(t)] = 0

            # ii. frequent attributes
            for fa in frequentAttributes:
                target_query_profile["f2"+str(fa)] = 0

            # iii. frequent values
            for fv in frequentValues:
                target_query_profile["f3"+str(fv)] = 0

            # iv. cluster
            for c in range(n_cluster_k):
                target_query_profile["f4"+str(c)] = 0

            print(target_query_profile)

            #add research attributes to the query object
            queryAttibuteSet = retriveQuerySearchAttributes(query)
            for attr in queryAttibuteSet:
                query_obj.addParameter(attr)
                # update target query profile with information about frequent attributes
                if attr in frequentAttributes:
                    target_query_profile["f2"+str(attr)] += 1

            #retrive query result
            queryResult = person.query(str(query_obj))

            cluster_frequency = dict()          #cluster_frequency[i] = number_of_tuples_belonging_to_cluster_i / tot_tuples

            for index, tuple in queryResult.iterrows():
                tuple_id = int(tuple['id'])
                tuple_name = tuple['name']
                tuple_address = tuple['address']
                tuple_occupation = tuple['occupation']

                #update target_query_profile
                # important tuples
                if tuple_id in mostFrequentTuples:
                    target_query_profile["f1"+str(tuple_id)] += 1

                # frequent values
                if tuple_name in frequentValues:
                    target_query_profile["f3"+str(tuple_name)] += (1/len(queryResult.index))
                if tuple_address in frequentValues:
                    target_query_profile["f3"+str(tuple_address)] += (1/len(queryResult.index))
                if tuple_occupation in frequentValues:
                    target_query_profile["f3"+str(tuple_occupation)] += (1/len(queryResult.index))
                #...end update target_user_profile

                #update cluster frequency
                tuple_profile = getPersonProfile(tuple)
                tuple_cluster = kmeans.predict([tuple_profile])
                target_query_profile["f4"+str(tuple_cluster[0])] += (1/len(queryResult.index))
            
            #print(f"query profile[{query_id}]")
            #print(target_query_profile)

            cosine_distance = cosineDistance(featureDict_to_featureList(target_user_profile), featureDict_to_featureList(target_query_profile))
            #print(f"cosine distance({target_user_index},{query_id}) = {cosine_distance}")
            print(f"vote({target_user_index},{query_id}) = {cosToVote(cosine_distance)}")

    queryFile.close()        
###



### Evaluate algorithm performance

for bo in utilityMatrix:
    for i, v in utilityMatrix[bo].items():
        if math.isnan(v):
            utilityMatrix.at[i, bo] = 1

rmse = rmse(utilityMatrix, utilityMatrix)
print("RMSE = "+str(rmse))
###