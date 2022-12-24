'''
In this file we implement some useful functions
'''

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
import pandas as pd
import math
import hash_table as hashTableClass

def ageGroup(age):
    #Example:
    # input: 12
    # output: "baby"
    #
    # input: 25
    # output: "young"
    #
    # input: 50
    # output: "medium"
    #     
    # input: 70
    # output: "old"

    baby_upper_bound = 15
    young_upper_bound = 40
    medium_upper_bound = 60
    
    if age <= baby_upper_bound: return "baby"
    if age <= young_upper_bound: return "young"
    if age <= medium_upper_bound: return "medium"
    return "old"


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

    #iff one of item1_profile or item2_profile is a null vectors
    #then we can't compute a meaningful value of the cosine distance
    if sum(item1_profile)==0 or sum(item2_profile)==0:
        print("Error cosineDistance: cannot compute cosine distance with zero vector")
        return -1

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
    
    ii) Then we scale x in range [1,100]
        mark = 4x + 1
    '''
    x = (cosine_distance+1)/2
    return round(99*x+1)


def tf(n, d):
    '''
    compute time frequency of a entity E which
    apperars n in a document D of length d
    '''
    return n/d

def idf(n, d):
    '''
    compute the inverse document frequency of a term
    which appears in n documents of a collection of
    d documents
    '''
    return math.log(d/n,10)

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


def card_query(queryFile):
    '''
    Return the number of queries in the queryFile
    '''
    queryFile = open(queryFile, "r")
    num_query = len(queryFile.readlines())
    queryFile.close()
    return num_query

def important_tuples(db, queryFile):
    '''
    Return the tuples which are more frequent in the
    result set of the queries and so more important
    '''

    tuple_frequency = dict()    #tuple_frequency[t] = how many times tuple t appears in any query
    f_tuple = set()             #tuples which are frequent according to the given threshold
    num_query = 0               #number of queries
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        num_query += 1
        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            tuple_id = int(tuple['id'])
            tuple_frequency[tuple_id] = tuple_frequency.get(tuple_id, 0) + 1
    queryFile.close()

    #define s as the x% of the basket
    s = (20/100)*num_query

    for t in tuple_frequency:
        if tuple_frequency[t]>=s:
            f_tuple.add(t)

    return f_tuple

def tuples_frequencies(db, queryFile):
    '''
    Return the frequency of the tuples which appear
    in the result set of the queries
    '''

    tuple_frequency = dict()    #tuple_frequency[t] = how many times tuple t appears in any query
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            tuple_id = int(tuple['id'])
            tuple_frequency[tuple_id] = tuple_frequency.get(tuple_id, 0) + 1
    queryFile.close()

    return tuple_frequency


def frequent_value(db, queryFile):
    '''
    Return the counts of the values which appear frequently in the
    result sets of the query
    '''

    print("START frequent_value mining")

    num_query = 0           #number of queries

    l = dict()              #set of frequent singleton; l[attr] = how many times the frequent itemset attr appears in all the query sets
    c = dict()              #c[attr] = number of times that the singleton attr appears in a query result

    ##frequent singleton
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        num_query += 1

        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            tuple_id = int(tuple['id'])
            tuple_name = tuple['name']
            tuple_address = tuple['address']
            tuple_occupation = tuple['occupation']
            tuple_age = ageGroup(tuple['age'])
            
            #update count for each singleton attribute
            c[tuple_name] = c.get(tuple_name, 0) + 1
            c[tuple_address] = c.get(tuple_address, 0) + 1
            c[tuple_occupation] = c.get(tuple_occupation, 0) + 1
            c[tuple_age] = c.get(tuple_age, 0) + 1

    queryFile.close()

    #define s as the x% of the basket
    s = (50/100)*num_query

    #fill l with all the singleton attr which are frequent
    for singleton in c:
        if c[singleton] >= s:
            l[singleton] = c[singleton]
    ##end frequent singleton

    print("END frequent_value mining")

    return l

def value_frequency(db, queryFile):
    num_query = 0           #number of queries

    l = dict()              #set of frequent singleton; l[attr] = how many times the frequent itemset attr appears in all the query sets
    c = dict()              #c[attr] = number of times that the singleton attr appears in a query result

    ##frequent singleton
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        num_query += 1

        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            tuple_id = int(tuple['id'])
            tuple_name = tuple['name']
            tuple_address = tuple['address']
            tuple_occupation = tuple['occupation']
            tuple_age = ageGroup(tuple['age'])
            
            #update count for each singleton attribute
            c[tuple_name] = c.get(tuple_name, 0) + 1
            c[tuple_address] = c.get(tuple_address, 0) + 1
            c[tuple_occupation] = c.get(tuple_occupation, 0) + 1
            c[tuple_age] = c.get(tuple_age, 0) + 1

    queryFile.close()

    return c

def expected_value_frequency(db, queryFile):
    hashTable = hashTableClass.HashTable()

    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            tuple_name = tuple['name']
            tuple_address = tuple['address']
            tuple_occupation = tuple['occupation']
            tuple_age = ageGroup(tuple['age'])
            
            hashTable.insertValue(tuple_name)
            hashTable.insertValue(tuple_address)
            hashTable.insertValue(tuple_occupation)
            hashTable.insertValue(tuple_age)

    queryFile.close()

    return hashTable

def frequent_attribute(queryFile):
    '''
    Return a set of attribute which have been frequently used
    as search parameters
    '''
    attribute_counts = dict()       #attribute_counts[attr] how many times users used search parameter "attr"
    fa = set()                      #set of attributes which are frequent according to a given threshold
    num_query = 0                   #number of queries
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        num_query += 1
        queryAttibuteSet = retriveQuerySearchAttributes(query)
        for attr in queryAttibuteSet:
            attribute_counts[attr] = attribute_counts.get(attr, 0) + 1
    queryFile.close()

    #define s as the x% of the basket
    s = (10/100)*num_query

    for a in attribute_counts:
        if attribute_counts[a] >= s:
            fa.add(a)
    
    return fa


def attribute_frequency(queryFile):
    '''
    Return the frequency of the attributes
    which have been used
    as search parameters
    '''
    attribute_counts = dict()       #attribute_counts[attr] how many times users used search parameter "attr"
    queryFile = open(queryFile, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n
        queryAttibuteSet = retriveQuerySearchAttributes(query)
        for attr in queryAttibuteSet:
            attribute_counts[attr] = attribute_counts.get(attr, 0) + 1
    queryFile.close()
    
    return attribute_counts


def k_means_clustering(person_db, k):
    '''
    Cluster person in the Person database.
    Return a cluster classifier.
    '''

    person_table = person_db.table
    scaled_person_table = person_table.copy()

    #normalize continuous features: age of the people
    #scaler = preprocessing.MinMaxScaler()
    #scaled_person_table[['age']] = scaler.fit_transform(person_table[['age']])

    #replace each "age" data with a categorical classification {baby, young, medium, old}
    for index, row in scaled_person_table.iterrows():
        a = row["age"]
        scaled_person_table.at[index, "age"] = ageGroup(a)

    #remove id column since it is irrelevant for the purpose of clustering
    scaled_person_table.drop('id', axis=1, inplace=True)

    #define one hot encoding for each categorical value in the dataset.
    #scaled_person_table = pd.get_dummies(scaled_person_table, columns=['name','address','occupation'])
    scaled_person_table = pd.get_dummies(scaled_person_table, columns=['name','address','occupation','age'])

    #we can not consider all the categorical features when clustering
    #otherwise we have the curse of dimensionality problem
    #we take into account only the top 6 of frequent categorical features
    attr_values = dict()    #attr_values["name_ste"] = how many time value "name_ste" appears in database Person
    person_columns = scaled_person_table.columns
    for c in person_columns:
        #if c != 'age':
        for r in scaled_person_table[c]:
            if r==1:
                attr_values[c] = attr_values.get(c, 0)+1

    attr_values_keys = list(attr_values.keys())
    attr_values_keys.sort(key=lambda x: attr_values[x], reverse=True)

    #selected_features = {'age'}
    selected_features = set()
    for i in range(min(6, len(attr_values_keys))):
        selected_features.add(attr_values_keys[i])
    
    #drop all columns which do not correspond to a relevant feature
    for c in person_columns:
        if c not in selected_features:
            scaled_person_table.drop(c, axis=1, inplace=True)
    
    #print(scaled_person_table)

    #now we can cluster the people who populate the table Person in a
    #reasonable way

    ## ELBOW METHOD EVALUATION
    #elbow_evaluation(scaled_person_table)
    #######

    kmeans = KMeans(
        init="random",
        n_clusters=k,
        n_init=10,
        max_iter=300,
        random_state=42
    )

    clusters = kmeans.fit_predict(scaled_person_table)
    labels = pd.DataFrame(clusters)
    labeledPeople = pd.concat((person_table,labels),axis=1)
    labeledPeople = labeledPeople.rename({0:'cluster'},axis=1)

    return labeledPeople

def plot_people_cluster(labeledPeople, numCluster):

    #name
    plt.title("People clustering - name", loc='left')

    for i in range(numCluster):
        x_name = list()
        y_name = list()

        overlaps = dict()

        for index, row in labeledPeople.iterrows():
            cluster = row['cluster']
            if cluster == i:
                name = row["name"]

                x_name.append(name)
                y_name.append(i)

                overlaps[(name, i)] = overlaps.get((name, i), 0)+1
    
        x_name_np = np.array(x_name)
        y_name_np = np.array(y_name)

        weight = list()
        for point in range(len(x_name)):
            point_x = x_name[point]
            point_y = y_name[point]
            
            weight.append(overlaps[(point_x, point_y)]*100)

        plt.scatter(x_name_np, y_name_np, label=i, s=weight)

    plt.legend()
    plt.show()
    #===

    #address
    plt.title("People clustering - address", loc='left')

    for i in range(numCluster):
        x_address = list()
        y_address = list()

        overlaps = dict()

        for index, row in labeledPeople.iterrows():
            cluster = row['cluster']
            if cluster == i:
                address = row["address"]

                x_address.append(address)
                y_address.append(i)

                overlaps[(address, i)] = overlaps.get((address, i), 0)+1
    
        x_address_np = np.array(x_address)
        y_address_np = np.array(y_address)

        weight = list()
        for point in range(len(x_address)):
            point_x = x_address[point]
            point_y = y_address[point]
            
            weight.append(overlaps[(point_x, point_y)]*100)

        plt.scatter(x_address_np, y_address_np, label=i, s=weight)
    
    plt.legend()
    plt.show()
    #===

    #age
    '''
    plt.title("People clustering - age", loc='left')

    x_offset = -5.0

    for i in range(numCluster):
        x_age = list()
        y_age = list()

        for index, row in labeledPeople.iterrows():
            cluster = row['cluster']
            if cluster == i:
                age = row["age"]

                x_age.append(x_offset)
                x_offset+=0.1
                y_age.append(age)
    
        x_age_np = np.array(x_age)
        y_age_np = np.array(y_age)

        plt.scatter(x_age_np, y_age_np, label=i)
    
    plt.legend()
    plt.show()
    '''    
    
    plt.title("People clustering - age", loc='left')

    for i in range(numCluster):
        x_age = list()
        y_age = list()

        overlaps = dict()

        for index, row in labeledPeople.iterrows():
            cluster = row['cluster']
            if cluster == i:
                age = ageGroup(row["age"])

                x_age.append(age)
                y_age.append(i)

                overlaps[(age, i)] = overlaps.get((age, i), 0)+1
    
        x_age_np = np.array(x_age)
        y_age_np = np.array(y_age)

        weight = list()
        for point in range(len(x_age)):
            point_x = x_age[point]
            point_y = y_age[point]
            
            weight.append(overlaps[(point_x, point_y)]*100)

        plt.scatter(x_age_np, y_age_np, label=i, s=weight)
    
    plt.legend()
    plt.show()
    
    #===

    #occupation
    plt.title("People clustering - occupation", loc='left')   

    for i in range(numCluster):
        x_occupation = list()
        y_occupation = list()

        overlaps = dict()

        for index, row in labeledPeople.iterrows():
            cluster = row['cluster']
            if cluster == i:
                occupation = row["occupation"]

                x_occupation.append(occupation)
                y_occupation.append(i)

                overlaps[(occupation, i)] = overlaps.get((occupation, i), 0)+1
    
        x_occupation_np = np.array(x_occupation)
        y_occupation_np = np.array(y_occupation)

        weight = list()
        for point in range(len(x_occupation)):
            point_x = x_occupation[point]
            point_y = y_occupation[point]
            
            weight.append(overlaps[(point_x, point_y)]*100)

        plt.scatter(x_occupation_np, y_occupation_np, label=i, s=weight)
    
    plt.legend()
    plt.show()
    #===

    for column in labeledPeople:
        print(column)

    ###

def elbow_evaluation(validation_set):
    '''
    This functions print the quality of the clusters
    with respect to the value of k. This is useful
    to set k appropriately.

    The input parameter validation_set is a dataframe
    with a structure like:

        occupation_other  occupation_professor  age_medium
    0                  0                     1            1
    1                  1                     0            1
    2                  0                     1            0
    3                  0                     1            0
    4                  0                     0            1

    '''

    inertias = []

    for i in range(1,10):
        kmeans = KMeans(
            init="random",
            n_clusters=i,
            n_init=10,
            max_iter=300,
            random_state=42
        )
        clusters = kmeans.fit_predict(validation_set)
        inertias.append(kmeans.inertia_)

    plt.plot(range(1,10), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

def clusterFrequency(db, num_cluster_person, queryFileName):
    '''
    Output how many times each cluster appears in the result
    set of the queries.
    The output of the function is a dictionary s.t.:
    key = cluster id
    value = number of times the cluster appears in the result
            set of the queries
    '''
    output = dict()

    for i in range(num_cluster_person):
        output[i] = 0
    
    queryFile = open(queryFileName, "r")
    for query in queryFile:
        query = query[:-1] #otherwise each query ends with \n

        queryResult = db.query(query)
        for index, tuple in queryResult.iterrows():
            cluster = int(tuple['cluster'])
            output[cluster] += 1
    queryFile.close()

    return output
    



