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
from function import rmse
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

from file import getQueryDefinition

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

databaseFileName = Path("data/relational_db.csv")
utilityMatrixFileName = Path("data/utility_matrix.csv")
queryFileName = Path("data/queries.csv")

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

# how many times each tuple appears
tupleFrequency = tuples_frequencies(person, queryFileName)

# Search frequently search attributes
# Attribute combinations searched by users which appear more then a specified threshold
frequentAttributes = frequent_attribute(queryFileName)

# how many times each attribute appear
attributeFrequency = attribute_frequency(queryFileName)

# Search values which appear frequently in the resultsets of the queries
# Values that appear frequently in query result sets
frequentValues = frequent_value(person, queryFileName)                 

valueFrequencyTrue = value_frequency(person, queryFileName)
expectedValueFrequency = expected_value_frequency(person, queryFileName)

counter = 0
avg_error = 0
for v in valueFrequencyTrue:
    print(f"True frequency of {v} = {valueFrequencyTrue[v]}")
    print(f"Expected frequency of {v} = {expectedValueFrequency.getValue(v)}")
    avg_error += abs(valueFrequencyTrue[v] - expectedValueFrequency.getValue(v))
    counter += 1
print("Avg error = "+str(avg_error/counter))

print("Most frequent tuple: "+str(mostFrequentTuples))
print("")
print("Most frequent attributes: "+str(frequentAttributes))
print("")
print("Most frequent values: "+str(frequentValues))
print("")

print("Tuple frequency: "+str(tupleFrequency))
print("Attribute frequency: "+str(attributeFrequency))

# Clustering of data in Person
num_cluster_person = 5
person.table = k_means_clustering(person, num_cluster_person)
#plot_people_cluster(person.table, num_cluster_person)

# count the cardinality of each cluster
# (cluster_card[i] = how many times a tuple belonging to cluster i
#  appears in the result set of an interrogation)
cluster_card = clusterFrequency(person, num_cluster_person, queryFileName)
print("Cluster cardinality")
print(cluster_card)
###
#end preprocessing
###

### Initialize user profiles and complete utility matrix with
### content based filtering
for index, v in utilityMatrix.iterrows():
    user_obj = userClass.User(index)
    query_def = dict()  #query_def[q] = the definition of the query with id q
    sum_vote = 0

    print("")
    print("========================")
    print("USER "+user_obj.getId())

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
   
    user_obj.computeUserProfile(person, query_def, tupleFrequency, attributeFrequency)
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

    #compute query profile of the unvoted queries
    query_to_be_voted = list()
    for q in user_obj.getUnVotedQueries():
        #get query definition
        qdef = query_def[q]
        
        #instantiate query object
        qobj = queryClass.Query(qdef)

        #computer query profile
        qobj.computeQueryProfile(person, tupleFrequency, attributeFrequency, user_obj)

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

    predictedVotes = user_obj.queryContentBasedEvaluation(person, query_def, query_to_be_voted)

    print("")
    print(f"USER[{user_obj.getId()}] predicted vote to unvoted queries")
    print(predictedVotes)
    print("")   

###


### Evaluate algorithm performance

for bo in utilityMatrix:
    for i, v in utilityMatrix[bo].items():
        if math.isnan(v):
            utilityMatrix.at[i, bo] = 1

rmse = rmse(utilityMatrix, utilityMatrix)
print("RMSE = "+str(rmse))
###