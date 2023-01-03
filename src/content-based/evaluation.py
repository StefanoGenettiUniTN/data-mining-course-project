'''
Functions in this file are useful to evaluate the performance of
the recommendation algorithm.
'''

import numpy as np
import matplotlib.pyplot as plt
import math

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

def me(u1, u2):
    '''
    Input: utility matrix u1, utility matrix u2
    Output: mean  error between the two
            utility matrixes. Typically the comparison
            is between the groundtruth and the predicted
            utility matrix
    '''
    me = 0
    card_votes = 0
    for query in u1:
        for index, vote in u1[query].items():
            vote_u1 = vote
            vote_u2 = u2.at[index, query]
            
            me += abs(vote_u1-vote_u2)
            card_votes += 1
    
    return me/card_votes

def me_unvoted(predictedVotes, completeUtilityMatrix):
    '''
    Compute average error between the votes predicted by the
    recommedation system and the vote inside the
    ground truth utility matrx
    '''
    me = 0
    card_votes = 0
    for user in predictedVotes:
        #print("User "+str(user))
        for query in predictedVotes[user]:
            predicted_v = predictedVotes[user][query]
            ground_truth = completeUtilityMatrix.at[user, query]
            #print(f"Query[{query}] = {predicted_v}")
            #print("Ground truth = "+str(ground_truth))

            me += abs(predicted_v-ground_truth)
            card_votes+=1

    return me/card_votes

def rmse_unvoted(predictedVotes, completeUtilityMatrix):
    '''
    Compute average mean squared error between the votes predicted by the
    recommedation system and the vote inside the ground truth utility matrx
    '''
    rmse = 0
    card_votes = 0
    for user in predictedVotes:
        for query in predictedVotes[user]:
            predicted_v = predictedVotes[user][query]
            ground_truth = completeUtilityMatrix.at[user, query]

            rmse += (predicted_v-ground_truth)**2
            card_votes+=1

    return math.sqrt(rmse/card_votes)

def query_avg_error(userPredictedVotes, completeUtilityMatrix):
    
    query_error = dict() #query_error[q] = list of errors which characterize query q
    error_sum = 0
    error_len = 0 
    for user in userPredictedVotes:
        for query in userPredictedVotes[user]:
            predicted_v = userPredictedVotes[user][query]
            ground_truth = completeUtilityMatrix.at[user, query]

            if query not in query_error:
                query_error[query] = list()
            
            query_error[query].append(abs(predicted_v-ground_truth))

            error_sum += abs(predicted_v-ground_truth)
            error_len += 1

    xpoints = np.array(list(query_error.keys()))

    ypoints_list = []
    for query in query_error:
        averageError = sum(query_error[query])/len(query_error[query])
        ypoints_list.append(averageError)

    ypoints = np.array(ypoints_list)

    plt.plot(xpoints, ypoints)

    plt.axhline(y=(error_sum/error_len), color='r', linestyle='-')
    plt.grid()
    plt.show()

def user_avg_error(userPredictedVotes, completeUtilityMatrix):
    
    user_error = dict() #user_error[u] = list of errors which characterize user u
    error_sum = 0
    error_len = 0 
    for user in userPredictedVotes:
        for query in userPredictedVotes[user]:
            predicted_v = userPredictedVotes[user][query]
            ground_truth = completeUtilityMatrix.at[user, query]

            if user not in user_error:
                user_error[user] = list()
            
            user_error[user].append(abs(predicted_v-ground_truth))

            error_sum += abs(predicted_v-ground_truth)
            error_len += 1

    xpoints = np.array(list(user_error.keys()))

    ypoints_list = []
    for user in user_error:
        averageError = sum(user_error[user])/len(user_error[user])
        ypoints_list.append(averageError)

    ypoints = np.array(ypoints_list)

    plt.plot(xpoints, ypoints)

    plt.axhline(y=(error_sum/error_len), color='r', linestyle='-')
    plt.grid()
    plt.show()

def userVoteCurve(targetUser, userPredictedVotes, completeUtilityMatrix):

    query_ids = []
    predicted_votes = []
    ground_truth_votes = []

    predictedAvgVote = 0
    trueAvgVote = 0
    numVotes = 0

    for query in userPredictedVotes[targetUser]:
        predicted_v = userPredictedVotes[targetUser][query]
        ground_truth = completeUtilityMatrix.at[targetUser, query]

        query_ids.append(query)
        predicted_votes.append(predicted_v)
        ground_truth_votes.append(ground_truth)

        predictedAvgVote += predicted_v
        trueAvgVote += ground_truth
        numVotes += 1
    
    xpoints = np.array(query_ids)
    ypoints_1 = np.array(predicted_votes)
    ypoints_2 = np.array(ground_truth_votes)
    
    plt.plot(xpoints, ypoints_1, label = "predicted votes", color='r')
    if numVotes > 0:
        plt.axhline(y=(predictedAvgVote/numVotes), color='r', linestyle='--', label = "predicted average vote")

    plt.plot(xpoints, ypoints_2, label = "true votes", color='g')
    if numVotes > 0:
        plt.axhline(y=(trueAvgVote/numVotes), color='g', linestyle='--', label = "true average vote")

    plt.legend()
    plt.title("Vote behaviour user "+str(targetUser))
    plt.grid()
    plt.show()