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


def user_pearson_similarity_computation(u1, u2):
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
        
    