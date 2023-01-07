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
