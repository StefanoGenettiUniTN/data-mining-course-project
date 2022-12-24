'''
This class represents a voter user
'''

from function import tf
from function import idf
from function import retriveQuerySearchAttributes
from function import ageGroup
from function import cosineDistance
from function import cosToVote

class User:

    def __init__(self, _id):
        '''
        _id --> id of the user
        '''
        self.id = _id
        self.votedQueries = dict()
        self.normalizedVotedQueries = dict()
        self.mostImportantQueries = list()
        self.unvotedQueries = list()
        self.avgVote = 0

        #important tuple votes
        self.ft_tuple = dict()

        #frequent search attributes votes
        self.ft_attribute = dict()

        #frequent value votes
        self.ft_value = dict()

        #cluster votes
        self.ft_cluster = dict()
    
    def __str__(self):
        output = f"userId = {self.id} \n"
        output += f" - votedQueries: {self.getVotedQueries()} \n"
        output += f" - unvotedQueries: {self.getUnVotedQueries()} \n"
        output += f" - avg_vote: {self.getAvgVote()} \n"
        output += "feature important tuples: \n"
        output += f"{self.ft_tuple} \n"
        output += "feature frequently searched attributes: \n"
        output += f"{self.ft_attribute} \n"
        output += "feature frequent values: \n"
        output += f"{self.ft_value} \n"
        output += "feature cluster: \n"
        output += f"{self.ft_cluster} \n"
        return output
    
    def getId(self):
        return self.id

    def addVotedQuery(self, queryId, vote):
        self.votedQueries[queryId] = vote
    
    def addUnVotedQuery(self, queryId):
        self.unvotedQueries.append(queryId)
    
    def setAvgVote(self, avg):
        self.avgVote = avg
    
    def getAvgVote(self):
        return self.avgVote
    
    def getVotedQueries(self):
        return self.votedQueries

    def getUnVotedQueries(self):
        return self.unvotedQueries

    def normalizeVotes(self):
        avg_vote = self.getAvgVote()

        for q in self.votedQueries:
            self.normalizedVotedQueries[q] = self.votedQueries[q]-avg_vote

    def computeUserProfile(self, db, query_def, tuple_frequency, attribute_frequency):
        '''
        Compute a dictionary which describe the relevance of the
        most important features which characterize the given user

        db = relational table
        query_def: dictionary such that query_def[q] = definition of query q
        tuple_frequency: dictionary such that tuple_frequency[t] = how many times tuple t appears in the result set of a query
        attribute_frequency: dictionary such that attribute_frequency[t] = how many times attribute t appears in the result set of a query
        '''

        #consider only the |num_queries| which are characterized by
        #the most extreme votes wrt the average user vote
        self.normalizeVotes()
        num_queries = 20
        votedQueries_keys = list(self.votedQueries.keys())
        votedQueries_keys.sort(key=lambda x: abs(self.normalizedVotedQueries[x]), reverse=True)
        for i in range(0, min(num_queries, len(votedQueries_keys))):
            self.mostImportantQueries.append(votedQueries_keys[i])

        print(votedQueries_keys)
        print(f"Most important query user [{self.getId()}] = {str(self.mostImportantQueries)}")

        attribute_importance = dict()           #attribute_importance[a] = avg TF.IDF of attribute a
        attribute_importance_size = dict()      #attribute_importance_size[a] = number of occurences of attribute a
        attribute_avg_vote = dict()             #attribute_avg_vote[a] = avg vote of attribute a

        tuple_importance = dict()               #tuple_importance[t] = avg TF.IDF of tuple t
        tuple_importance_size = dict()          #tuple_importance_size[t] = number of occurences of tuple t
        tuple_avg_vote = dict()                 #tuple_avg_vote[t] = avg vote of tuple t

        value_importance = dict()               #value_importance[v] = avg TF.IDF of value v
        value_importance_size = dict()          #value_importance_size[v] = number of occurences of value v
        value_avg_vote = dict()                 #value_avg_vote[v] = avg vote of value v

        cluster_importance = dict()             #cluster_importance[c] = avg TF.IDF of cluster c
        cluster_importance_size = dict()        #cluster_importance_size[c] = number of occurences of cluster c
        cluster_avg_vote = dict()               #cluster_avg_vote[c] = avg vote of cluster c

        for q in self.mostImportantQueries:
            #get query definition
            qdef = query_def[q]
            
            #get normalized vote given by the target user to query q
            vote = self.normalizedVotedQueries[q]

            #read search attributes
            search_attr = retriveQuerySearchAttributes(qdef)
            for a in search_attr:
                a_tf = tf(1, len(search_attr))
                a_idf = idf(attribute_frequency[a], len(self.votedQueries.keys())+len(self.unvotedQueries))
                attribute_importance[a] = attribute_importance.get(a, 0)+((a_tf*a_idf)*abs(vote))
                attribute_importance_size[a] = attribute_importance_size.get(a, 0)+1
                attribute_avg_vote[a] = attribute_avg_vote.get(a,0)+vote

            query_result = db.query(qdef)   

            tuple_list = list()     #list of tuples which appear in the result set
            values_card = dict()    #values_card[v] = num of occurences of value v in the result set
            cluster_card = dict()   #cluster_card[c] = num of occurences of cluster c in the result set
            for tuple_index, tuple_value in query_result.iterrows():
                tuple_id = int(tuple_value['id'])
                tuple_name = tuple_value['name']
                tuple_address = tuple_value['address']
                tuple_occupation = tuple_value['occupation']
                tuple_age = ageGroup(tuple_value['age'])
                tuple_cluster = tuple_value['cluster']

                tuple_list.append(tuple_id)
                
                values_card[tuple_name] = values_card.get(tuple_name, 0) + 1
                values_card[tuple_address] = values_card.get(tuple_address, 0) + 1
                values_card[tuple_occupation] = values_card.get(tuple_occupation, 0) + 1
                values_card[tuple_age] = values_card.get(tuple_age, 0) + 1

                cluster_card[tuple_cluster] = cluster_card.get(tuple_cluster, 0)+1
            
            #update tuple_importance
            for t in tuple_list:
                t_tf = tf(1, len(query_result))
                t_idf = idf(tuple_frequency[t], len(self.votedQueries.keys())+len(self.unvotedQueries))
                tuple_importance[t] = tuple_importance.get(t, 0)+((t_tf*t_idf)*abs(vote))
                tuple_importance_size[t] = tuple_importance_size.get(t, 0)+1
                tuple_avg_vote[t] = tuple_avg_vote.get(t, 0)+vote 
            
            #update value_importance
            for v in values_card:
                v_tf = tf(values_card[v], len(query_result))
                value_importance[v] = value_importance.get(v, 0)+v_tf*abs(vote)
                value_importance_size[v] = value_importance_size.get(v, 0)+1
                value_avg_vote[v] = value_avg_vote.get(v, 0)+vote

            #update cluster_importance
            for c in cluster_card:
                c_tf = tf(cluster_card[c], len(query_result))
                cluster_importance[c] = cluster_importance.get(c, 0)+c_tf*abs(vote)
                cluster_importance_size[c] = cluster_importance_size.get(c, 0)+1
                cluster_avg_vote[c] = cluster_avg_vote.get(c, 0) + vote

        #compute tuple avg importance
        for t in tuple_importance:
            tuple_importance[t] = tuple_importance[t]/tuple_importance_size[t]
            tuple_avg_vote[t] = tuple_avg_vote[t]/tuple_importance_size[t]

        #compute attribute avg importance
        for a in attribute_importance:
            attribute_importance[a] = attribute_importance[a]/attribute_importance_size[a]
            attribute_avg_vote[a] = attribute_avg_vote[a]/attribute_importance_size[a]

        #compute value avg importance
        for v in value_importance:
            value_importance[v] = value_importance[v]/value_importance_size[v]
            value_avg_vote[v] = value_avg_vote[v]/value_importance_size[v]

        #compute cluster avg importance
        for c in cluster_importance:
            cluster_importance[c] = cluster_importance[c]/cluster_importance_size[c]
            cluster_avg_vote[c] = cluster_avg_vote[c]/cluster_importance_size[c]

        #update user profile with important tuple
        tuple_importance_keys = list(tuple_importance.keys())
        tuple_importance_keys.sort(key=lambda x: tuple_importance[x], reverse=True)
        for i in range(0, min(1, len(tuple_importance_keys))):
            self.ft_tuple[tuple_importance_keys[i]] = tuple_avg_vote[tuple_importance_keys[i]]

        #update user profile with important attributes
        attribute_importance_keys = list(attribute_importance.keys())
        attribute_importance_keys.sort(key=lambda x: attribute_importance[x], reverse=True)
        for i in range(0, min(1, len(attribute_importance_keys))):
            self.ft_attribute[attribute_importance_keys[i]] = attribute_avg_vote[attribute_importance_keys[i]]

        #update user profile with important with important values
        value_importance_keys = list(value_importance.keys())
        value_importance_keys.sort(key=lambda x: value_importance[x], reverse=True)
        for i in range(0, min(2, len(value_importance_keys))):
            self.ft_value[value_importance_keys[i]] = value_avg_vote[value_importance_keys[i]]

        #update user profile with important cluster
        cluster_importance_keys = list(cluster_importance.keys())
        cluster_importance_keys.sort(key=lambda x: cluster_importance[x], reverse=True)
        for i in range(0, min(1, len(cluster_importance_keys))):
            self.ft_cluster[cluster_importance_keys[i]] = cluster_avg_vote[cluster_importance_keys[i]]


    def queryContentBasedEvaluation(self, db, query_def, unvoted_query_profiles):
        '''
        assign a vote to each unvoted query using content base recommendation

        db = relational table
        query_def = dictionary such that query_def[q] = definition of query q
        unvoter_query_profiles = each unvoted query has its own query profile
        '''
        
        #output[q] = vote assigned to query q for each q in unvoted_query_profiles
        output = dict()

        #init a collection of the relevant features of the unvoted queries
        ft_tuple_query = dict()
        ft_tuple_query_size = dict()
        ft_attribute_query = dict()
        ft_attribute_query_size = dict()
        ft_value_query = dict()
        ft_value_query_size = dict()
        ft_cluster_query = dict()
        ft_cluster_query_size = dict()
        for q_obj in unvoted_query_profiles:
            for t in q_obj.get_ft_tuple():
                ft_tuple_query[t] = 0
                ft_tuple_query_size[t] = 0
            
            for a in q_obj.get_ft_attribute():
                ft_attribute_query[a] = 0
                ft_attribute_query_size[a] = 0

            for v in q_obj.get_ft_value():
                ft_value_query[v] = 0
                ft_value_query_size[v] = 0

            for c in q_obj.get_ft_cluster():
                ft_cluster_query[c] = 0
                ft_cluster_query_size[c] = 0
        #---

        #iterate user's voted queries to complete query feature values
        for voted_query in self.votedQueries:
            #get query definition
            qdef = query_def[voted_query]
            
            #get vote and subtruct avg vote of the target user
            norm_vote = self.votedQueries[voted_query]-self.avgVote

            #read search attributes
            search_attr = retriveQuerySearchAttributes(qdef)
            for a in search_attr:
                if a in ft_attribute_query:
                    ft_attribute_query[a] += norm_vote
                    ft_attribute_query_size[a] += 1

            query_result = db.query(qdef)   

            for tuple_index, tuple_value in query_result.iterrows():
                tuple_id = int(tuple_value['id'])
                tuple_name = tuple_value['name']
                tuple_address = tuple_value['address']
                tuple_occupation = tuple_value['occupation']
                tuple_age = ageGroup(tuple_value['age'])
                tuple_cluster = tuple_value['cluster']

                if tuple_id in ft_tuple_query:
                    ft_tuple_query[tuple_id] += norm_vote
                    ft_tuple_query_size[tuple_id] += 1
                
                if tuple_name in ft_value_query:
                    ft_value_query[tuple_name] += norm_vote
                    ft_value_query_size[tuple_name] += 1
                
                if tuple_address in ft_value_query:
                    ft_value_query[tuple_address] += norm_vote
                    ft_value_query_size[tuple_address] += 1

                if tuple_occupation in ft_value_query:
                    ft_value_query[tuple_occupation] += norm_vote
                    ft_value_query_size[tuple_occupation] += 1

                if tuple_age in ft_value_query:
                    ft_value_query[tuple_age] += norm_vote
                    ft_value_query_size[tuple_age] += 1

                if tuple_cluster in ft_value_query:
                    ft_cluster_query[tuple_cluster] += norm_vote
                    ft_cluster_query_size[tuple_cluster] += 1

        #compute average vote for each query feature 
        for t in ft_tuple_query:
            if ft_tuple_query_size[t]>0:
                ft_tuple_query[t] = ft_tuple_query[t]/ft_tuple_query_size[t]
        
        for a in ft_attribute_query:
            if ft_attribute_query_size[a]>0:
                ft_attribute_query[a] = ft_attribute_query[a]/ft_attribute_query_size[a]
        
        for v in ft_value_query:
            if ft_value_query_size[v]>0:
                ft_value_query[v] = ft_value_query[v]/ft_value_query_size[v]
        
        for c in ft_cluster_query:
            if ft_cluster_query_size[c]>0:
                ft_cluster_query[c] = ft_cluster_query[c]/ft_value_query_size[c]
        #---

        #print(f"user[{self.getId()}] ft_tuple_query = {ft_tuple_query}")
        #print(f"user[{self.getId()}] ft_attribute_query = {ft_attribute_query}")
        #print(f"user[{self.getId()}] ft_value_query = {ft_value_query}")
        #print(f"user[{self.getId()}] ft_cluster_query = {ft_cluster_query}")

        #predict vote according to user preferences
        for query_obj in unvoted_query_profiles:
            query_vector = []
            user_vector = []

            #user favourite tastes
            for t in self.ft_tuple:
                user_vector.append(self.ft_tuple[t])
                query_vector.append(query_obj.ft_tuple_user[t])
            
            for a in self.ft_attribute:
                user_vector.append(self.ft_attribute[a])
                query_vector.append(query_obj.ft_attribute_user[a])

            for v in self.ft_value:
                user_vector.append(self.ft_value[v])
                query_vector.append(query_obj.ft_value_user[v])
            
            for c in self.ft_cluster:
                user_vector.append(self.ft_cluster[c])
                query_vector.append(query_obj.ft_cluster_user[c])
            
            #query most relevant parts
            for t in query_obj.ft_tuple:
                user_vector.append(ft_tuple_query[t])
                query_vector.append(query_obj.ft_tuple[t])
            
            for a in query_obj.ft_attribute:
                user_vector.append(ft_attribute_query[a])
                query_vector.append(query_obj.ft_attribute[a])

            for v in query_obj.ft_value:
                user_vector.append(ft_value_query[v])
                query_vector.append(query_obj.ft_value[v])
            
            for c in query_obj.ft_cluster:
                user_vector.append(ft_cluster_query[c])
                query_vector.append(query_obj.ft_cluster[c])

            print("length user vector = "+str(len(user_vector)))
            print("length query vector = "+str(len(query_vector)))

            cosine_distance = cosineDistance(user_vector, query_vector)
            output[query_obj.getId()] = cosToVote(cosine_distance)

        return output



    def get_ft_tuple(self):
        return self.ft_tuple

    def get_ft_value(self):
        return self.ft_value

    def get_ft_attribute(self):
        return self.ft_attribute

    def get_ft_cluster(self):
        return self.ft_cluster

    '''
    def ft_init_tuple(self, importantTuples):
        
        #initialize the features about
        #important tuples
        
        for t in importantTuples:
            self.ft_tuple[t] = []
    
    def ft_add_vote_tuple(self, tuple, vote):
        self.ft_tuple[tuple].append(vote)

    def ft_init_attribute(self, frequentAttributes):
        
        #initialize the features about
        #frequently searched attributes
        
        for a in frequentAttributes:
            self.ft_attribute[a] = []
    
    def ft_add_vote_attribute(self, attr, vote):
        self.ft_attribute[attr].append(vote)
    
    def ft_init_values(self, frequentValues):
        
        #initialize the features about
        #the values which appear frequently
        #in the result set of the queries
        
        for v in frequentValues:
            self.ft_value[v] = []

    def ft_add_vote_value(self, value, vote):
        self.ft_value[value].append(vote)

    def ft_init_cluster(self, numCluster):
        
        #initialize the features about the
        #clusters which have been selected
        
        for c in range(numCluster):
            self.ft_cluster[c] = []

    def ft_add_vote_cluster(self, cluster, vote):
        self.ft_cluster[cluster].append(vote)
    '''

    '''
    def computerProfileDictionary(self):
        
        #return a dictionary such that:
        # - key is the feature
        # - value is the avg vote of the user for that feature
        
        user_profile_dict = dict()
        
        #important tuples
        for t in self.ft_tuple:
            if len(self.ft_tuple[t])>0:
                user_profile_dict[t] = sum(self.ft_tuple[t]) / len(self.ft_tuple[t])
            else:
                user_profile_dict[t] = 0

        #frequent attributes
        for a in self.ft_attribute:
            if len(self.ft_attribute[a])>0:
                user_profile_dict[a] = sum(self.ft_attribute[a]) / len(self.ft_attribute[a])
            else:
                user_profile_dict[a] = 0

        #frequent values
        for v in self.ft_value:
            if len(self.ft_value[v])>0:
                user_profile_dict[v] = sum(self.ft_value[v]) / len(self.ft_value[v])
            else:
                user_profile_dict[v] = 0

        #cluster
        for c in self.ft_cluster:
            if len(self.ft_cluster[c])>0:
                user_profile_dict[c] = sum(self.ft_cluster[c]) / len(self.ft_cluster[c])
            else:
                user_profile_dict[c] = 0
        
        return user_profile_dict

    def computerProfileVector(self):
        
        #return a list such that each position
        #corresponds to the avg vote of the user
        #for a certain feature
        
        user_profile = list()
        
        #important tuples
        for t in self.ft_tuple:
            if len(self.ft_tuple[t])>0:
                user_profile.append(sum(self.ft_tuple[t]) / len(self.ft_tuple[t]))
            else:
                user_profile.append(0)

        #frequent attributes
        for a in self.ft_attribute:
            if len(self.ft_attribute[a])>0:
                user_profile.append(sum(self.ft_attribute[a]) / len(self.ft_attribute[a]))
            else:
                user_profile.append(0)

        #frequent values
        for v in self.ft_value:
            if len(self.ft_value[v])>0:
                user_profile.append(sum(self.ft_value[v]) / len(self.ft_value[v]))
            else:
                user_profile.append(0)

        #cluster
        for c in self.ft_cluster:
            if len(self.ft_cluster[c])>0:
                user_profile.append(sum(self.ft_cluster[c]) / len(self.ft_cluster[c]))
            else:
                user_profile.append(0)
        
        return user_profile
    '''    

