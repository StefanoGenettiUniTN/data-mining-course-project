'''
Useful functions to deal with collaborative filtering.
'''

import itertools

def updateUtilityMatrixVotes(user_recommendation, user_cluster, query_cluster, userList, queryList):
    for u_index in userList:
        user_obj = userList[u_index]
        if user_obj.completed==False:
            for uq in user_obj.unvotedEntities.copy():
                query_obj = queryList[uq]

                #get user cluster
                cluster_u_id = user_obj.cluster
                cluster_u = user_cluster[cluster_u_id]

                #get query cluster
                cluster_q_id = query_obj.cluster
                cluster_q = query_cluster[cluster_q_id]

                #compute average vote assigned by users in cluster cluster_u_id
                #to queries in cluster cluster_q_id
                voteSum = 0
                voteSize = 0
                for u, q in itertools.product(cluster_u.components, cluster_q.components):
                    if str(q) in u.votedEntities:
                        voteSum += (u.votedEntities[str(q)]-u.averageVote)
                        voteSize += 1
                
                #assign to the unvoted query the average vote assigned by users
                #in cluster cluster_u_id to queries in cluster cluster_q_id
                #and annotate the assignment in user_recommendation
                if voteSize>0:
                    avgVote = (voteSum/voteSize)+user_obj.averageVote
                    avgVote = min(avgVote, 100)
                    avgVote = max(avgVote, 1)
                    user_obj.addVotedEntity(uq, avgVote)
                    query_obj.addVotedEntity(u_index, avgVote)
                    user_recommendation[u_index][uq] = int(avgVote)
