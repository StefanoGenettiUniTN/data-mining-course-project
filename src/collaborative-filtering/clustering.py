'''
Functions to deal with clustering tasks
'''
import math
import cluster as clusterClass

def merge(c1, c2, newClusterId):
    '''
    Input: the two clusters to be merged
    Output: the new cluster object
    '''
    outputCluster = clusterClass.Cluster(newClusterId)
    outputCluster.cardinality = c1.cardinality + c2.cardinality

    for c in c1.components:
        outputCluster.addComponent(c)

    for c in c2.components:
        outputCluster.addComponent(c)

    return outputCluster


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
    