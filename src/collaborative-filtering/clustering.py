'''
Functions to deal with clustering tasks
'''
import math
import cluster as clusterClass
import itertools

def merge(c1, c2, newClusterId):
    '''
    Input: the two clusters to be merged
    Output: the new cluster object
    '''
    outputCluster = clusterClass.Cluster(newClusterId)

    for c in c1.components:
        outputCluster.addComponent(c)
        c.setCluster(newClusterId)

    for c in c2.components:
        outputCluster.addComponent(c)
        c.setCluster(newClusterId)

    return outputCluster

def cluster_similarity(c1, c2, similarityMetric):
    '''
    Compute average distance between points
    in the cluster according to the input
    similarityMetric
    '''
    similaritySum = 0
    similarityCard = 0
    for entity1, entity2 in itertools.product(c1.components, c2.components):
        similaritySum += similarityMetric(entity1, entity2)
        similarityCard += 1
    return similaritySum/similarityCard

def query_cluster_similarity(c1, c2, db):
    '''
    Compute average distance between points
    in the cluster of queries according to
    query_tuple_similarity metric
    '''
    similaritySum = 0
    similarityCard = 0
    for entity1, entity2 in itertools.product(c1.components, c2.components):
        similaritySum += query_tuple_similarity(entity1, entity2, db)
        similarityCard += 1
    return similaritySum/similarityCard

def user_pearson_similarity(u1, u2):
    '''
    Return person similarity between user u1 and user u2 according to
    their row in the utility matrix
    '''
    avg_u1 = u1.computeAvgVote()
    avg_u2 = u2.computeAvgVote()
    
    commonItem = 0

    numerator = 0
    denominator1 = 0
    denominator2 = 0

    for i in u1.votedEntities:
        if i in u2.votedEntities:
            numerator += (u1.votedEntities[i]-avg_u1)*(u2.votedEntities[i]-avg_u2)
            denominator1 += (u1.votedEntities[i]-avg_u1)**2
            denominator2 += (u2.votedEntities[i]-avg_u2)**2

            commonItem += 1

    if commonItem==0:
        return 0
    
    #print(f"similarity user {u1} and user {u2} = {numerator/(math.sqrt(denominator1)*math.sqrt(denominator2))}")
    return numerator/(math.sqrt(denominator1)*math.sqrt(denominator2))

def query_tuple_similarity(q1, q2, db):
    '''
    Intersection over union among the tuples in the resultsets
    of the two queries
    '''
    tuple_q1 = set()
    tuple_q2 = set()

    def_q1 = q1.definition
    def_q2 = q2.definition

    if def_q1 == def_q2:
        return 1

    query_result = db.query(def_q1)   

    for tuple_index, tuple_value in query_result.iterrows():
        tuple_id = int(tuple_value['id'])
        tuple_q1.add(tuple_id)

    query_result = db.query(def_q2)   

    for tuple_index, tuple_value in query_result.iterrows():
        tuple_id = int(tuple_value['id'])
        tuple_q2.add(tuple_id)

    intersection = tuple_q1.intersection(tuple_q2)
    union = tuple_q1.union(tuple_q2)

    return len(intersection)/len(union)

def condense(clusterList, similarityMetric, newClusterId):
    '''
    Merge the couple of clusters with the lowest similarityMetric

    clusterList: collection of clusters
    similarityMetric: function used to measure the similarity between two clusters
    '''
    if len(clusterList)<2:
        print("Error function condense: cannot call function condense if the number of clusters is lower than 2.")
        return -1

    clusterCouples = itertools.combinations(clusterList.keys(), 2)
    bestC1 = -1
    bestC2 = -1
    bestSimilarity = float('-inf')
    for c1, c2 in clusterCouples:
        c1_obj = clusterList[c1]
        c2_obj = clusterList[c2]

        currentSimilarity = cluster_similarity(c1_obj, c2_obj, similarityMetric)

        if currentSimilarity>bestSimilarity:
            bestC1 = c1
            bestC2 = c2
            bestSimilarity = currentSimilarity
    
    if bestC1!=-1 and bestC2!=-1:
        #print(f"function condense. merging cluster {bestC1} and cluster {bestC2}")
        clusterList[newClusterId] =  merge(clusterList[bestC1], clusterList[bestC2], newClusterId)
        clusterList.pop(bestC1, None)
        clusterList.pop(bestC2, None)
        #print("merge completed")
    else:
        return -1



    