'''
University of Trento
Data Mining course project
Academic Year 2022-2023
Stefano Genetti
Pietro Fronza
'''
import pandas as pd
import itertools
from pathlib import Path
import math

from recommendation import content_based

from evaluation import rmse
from evaluation import me
from evaluation import me_unvoted
from evaluation import rmse_unvoted
from evaluation import query_avg_error
from evaluation import user_avg_error
from evaluation import userVoteCurve

databaseFileName = Path("data/university/relational_db.csv")
utilityMatrixFileName = Path("data/university/utility_matrix.csv")
completeUtilityMatrixFileName = Path("data/university/utility_matrix_complete.csv")
outputUtilityMatrixFileName = Path("data/university/output.csv")
queryFileName = Path("data/university/queries.csv")
userFileName = Path("data/university/users.csv")

#user_recommendation[u] = dictionary such that user_recommendation[u][q1] is the
#vote recommended by the system for the user-query couple (u,q1)
user_recommendation = dict()

#partition user in three sets:
#   i) users who voted nothing (cold start)
#  ii) users who voted a lot
# iii) users who voted few queries
coldStartUsers = set()
frequentVoters = set()
rareVoters = set()
utilityMatrix = pd.read_csv(utilityMatrixFileName) #utility matrix

for user, votes in utilityMatrix.iterrows():
    votedQueries = 0
    totQueries = 0
    for query in votes.keys():
        if not math.isnan(votes[query]):
            votedQueries += 1
        totQueries += 1
    
    if votedQueries==0:
        coldStartUsers.add(user)
    elif votedQueries > totQueries/2:
        frequentVoters.add(user)
    else:
        rareVoters.add(user)

print("USER WHO DID NOT VOTE ANY QUERY")
print(coldStartUsers)
print("")
print("FREQUENT VOTERS")
print(frequentVoters)
print("")
print("RARE VOTERS")
print(rareVoters)
print("")
###

#process frequent voters with content based filtering
content_based(  databaseFileName,                       #database file name
                utilityMatrixFileName,                  #utility matrix file name
                completeUtilityMatrixFileName,          #complete utility matrix file name
                outputUtilityMatrixFileName,            #output utility matrix file name
                queryFileName,                          #query log file name
                user_recommendation,                    #user recommendation obj
                frequentVoters                          #frequent voters list
            )

#process rare voters with collaborative filtering

#solve people who did not vote anything


### Evaluate algorithm performance
print("Quality Evaluation")

#complete utility matrix
completeUtilityMatrix = pd.read_csv(completeUtilityMatrixFileName)

rmse = rmse(utilityMatrix, completeUtilityMatrix)
me = me(utilityMatrix, completeUtilityMatrix)
me_unvoted = me_unvoted(user_recommendation, completeUtilityMatrix)
rmse_unvoted = rmse_unvoted(user_recommendation, completeUtilityMatrix)
print("RMSE = "+str(rmse))
print("ME = "+str(me))
print("ME UNVOTED = "+str(me_unvoted))
print("RMSE UNVOTED = "+str(rmse_unvoted))

#average error for each query
query_avg_error(user_recommendation, completeUtilityMatrix)

#average vote for each user
user_avg_error(user_recommendation, completeUtilityMatrix)

for u in user_recommendation:
    userVoteCurve(u, user_recommendation, completeUtilityMatrix)
###