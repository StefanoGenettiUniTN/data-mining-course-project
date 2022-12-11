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
from function import retriveQuerySearchAttributes
from function import retriveQueryId
from function import getPersonProfile
from function import cosineDistance
from function import featureDict_to_featureList
from function import cosToVote
import itertools

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = "../data/relational_db.csv"
utilityMatrixFileName = "../data/utility_matrix.csv"
queryFileName = "../data/queries.csv"

#Read database
person = db.Person(databaseFileName)

#Utility matrix
utilityMatrix = pd.read_csv(utilityMatrixFileName)

#Query set: set of queries posed in the past
queryFile = open(queryFileName, "r")

###
# Search most important tuples
# Search frequently search attributes
# Search values which appear frequently in the resultsets of the queries
###
mostFrequentTuples = list()                 #tuples which appear more then the others in the resultset of queries
tupleFrequency = dict()                     #tupleFrequency[x] = how many times tuple with id x appears in the resultset of queries
querySetSize = 0                            #number of queries which have been posed in the past
frequentAttributes = set()                  #attribute combination searched by users which appear more then a specified threshold
frequentAttributesSingleton = dict()        #frequentAttributeSingleton[(x)] how many times attribute (x) appears
frequentValues = set()                      #values that appear frequently in query result sets
frequenceNameValue = dict()                 #frequenceNameValue[x] = how many times attribute name have x as a value in the query resultset
frequenceAddressValue = dict()              #frequenceAddressValue[x] = how many times attribute address have x as a value in the query resultset
frequenceOccupationValue = dict()           #frequenceOccupationValue[x] = how many times attribute occupation have x as a value in the query resultset
query_identifiers = list()                  #list of existing query identifiers

for query in queryFile:
    query = query[:-1] #otherwise each query ends with \n

    queryAttibuteSet = retriveQuerySearchAttributes(query)
    for attr in queryAttibuteSet:
        if attr in frequentAttributesSingleton:
            frequentAttributesSingleton[attr] += 1
        else:
            frequentAttributesSingleton[attr] = 1

    query_identifiers.append(retriveQueryId(query))

    queryResult = person.query(query)
    for index, tuple in queryResult.iterrows():
        tuple_id = int(tuple['id'])
        tuple_name = tuple['name']
        tuple_address = tuple['address']
        tuple_occupation = tuple['occupation']
        
        if tuple_id in tupleFrequency:
            tupleFrequency[tuple_id]+=1
        else:
            tupleFrequency[tuple_id]=1

        if tuple_name in frequenceNameValue:
            frequenceNameValue[tuple_name] += 1
        else:
            frequenceNameValue[tuple_name] = 1

        if tuple_address in frequenceAddressValue:
            frequenceAddressValue[tuple_address] += 1
        else:
            frequenceAddressValue[tuple_address] = 1

        if tuple_occupation in frequenceOccupationValue:
            frequenceOccupationValue[tuple_occupation] += 1
        else:
            frequenceOccupationValue[tuple_occupation] = 1

    querySetSize += 1

queryFile.close()

#Select frequent tuples which appear in more thant 40% of the query results
threshold = (40*querySetSize)/100
for tuple in tupleFrequency:
    if tupleFrequency[tuple]>=threshold:
        mostFrequentTuples.append(tuple)

#Retrive frequent attributes
frequentAttributesThreshold = 2

for sing in frequentAttributesSingleton:
    if frequentAttributesSingleton[sing] >= frequentAttributesThreshold:
        frequentAttributes.add((sing))


#Retrive frequent attribute values in the resultset
frequentValueThreshold = 3
for n in frequenceNameValue:
    if frequenceNameValue[n]>=3:
        frequentValues.add(n)

for a in frequenceAddressValue:
    if frequenceAddressValue[a]>=3:
        frequentValues.add(a)

for o in frequenceOccupationValue:
    if frequenceOccupationValue[o]>=3:
        frequentValues.add(o)

###

###Clustering of data in Person
people = []
young_max_age = 20
medium_max_age = 60
old_max_age = 150 

for index, row in person.table.iterrows():
    #each people must be a set of features
    #for the moment features are constant
    #[ste, pie, fab, ero, vit, mat, via1, via2, via3, via4, via5, giovane, medio, anziano, imp1, sar, tec]
    #in futuro potrei ad esempio considerare la top 10 dei nomi più frequenti e cosi via

    p = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    
    print(row)

    f = 0

    if row["name"]=="ste":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["name"]=="pie":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["name"]=="fab":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["name"]=="ero":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["name"]=="vit":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["name"]=="mat":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["address"]=="via1":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["address"]=="via2":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["address"]=="via3":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["address"]=="via4":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["address"]=="via5":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["age"]<=young_max_age:
        p[f] = 1
    else:
        p[f] = 0
    
    f += 1

    if row["age"]>young_max_age and row["age"]<=medium_max_age:
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["age"]>medium_max_age:
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["occupation"]=="imp1":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["occupation"]=="sar":
        p[f] = 1
    else:
        p[f] = 0

    f += 1

    if row["occupation"]=="tec":
        p[f] = 1
    else:
        p[f] = 0
    

    #print(f"id: {row['id']} - name: {row['name']} - address: {row['address']} - age: {row['age']} - occupation: {row['occupation']}")
    #print(p)

    people.append(p)

n_cluster_k = 2 #number of clusters
kmeans = KMeans(
    init="random",
    n_clusters=n_cluster_k,
    n_init=10,
    max_iter=300,
    random_state=42
)

kmeans.fit(people)
#print(kmeans.labels_)
#print(kmeans.inertia_)
#print(kmeans.predict([[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]]))
###

###Count number of votes of each user to partition users according to their voting rate
voters = dict()             #voters[i] = list of queries voted by user i
frequent_voters = list()    #users who voted a lot
high_voters_threshold = 4

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
###

###Complete utility matrix of frequent users with collaborative filtering
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

    print(target_user_profile)

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

            print(target_user_profile)

    #complete the target_user_profile
    #computing the avg vote for each query feature
    for f in featureCardinality:
        if featureCardinality[f]>0:
            target_user_profile[f] = target_user_profile[f]/featureCardinality[f]

    print("final user profile")
    print(target_user_profile)

    queryFile.close()

    print(f"complete utilitiy matrix row of user {target_user_index} using content based recommendation")
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
            
            print(f"predicting opinion of user {target_user_index} about query {query_id}")
            
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
            
            print(f"query profile[{query_id}]")
            print(target_query_profile)

            cosine_distance = cosineDistance(featureDict_to_featureList(target_user_profile), featureDict_to_featureList(target_query_profile))
            print(f"cosine distance({target_user_index},{query_id}) = {cosine_distance}")
            print(f"vote({target_user_index},{query_id}) = {cosToVote(cosine_distance)}")

    queryFile.close()        
###