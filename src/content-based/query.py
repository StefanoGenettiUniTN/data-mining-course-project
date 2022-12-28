'''
This class represents a query
'''
import database as db
from function import retriveQuerySearchAttributes
from function import retriveQueryId
from function import ageGroup

class Query:

    def __init__(self, queryDefinition):
        self.id = retriveQueryId(queryDefinition)

        self.parameter = []
        parameter_set = retriveQuerySearchAttributes(queryDefinition)
        for p in parameter_set:
            self.parameter.append(p)
        
        self.resultLength = 0

        #list of tuples which appear in the result of the given query
        self.tuples = []

        #how many times each value appears in the given query
        self.values = dict() #how many times each value appears

        #how many times each cluster appears in the given query
        self.clusters = dict() #how many times each cluster appears

        #init important tuple
        self.ft_tuple = dict()
        self.ft_tuple_user = dict()

        #init frequently searched attributes
        self.ft_attribute = dict()
        self.ft_attribute_user = dict()

        #init frequent value
        self.ft_value = dict()
        self.ft_value_user = dict()

        #init cluster
        self.ft_cluster = dict()
        self.ft_cluster_user = dict()


    def __str__(self):
        output = f"{self.id}"
        for p in self.parameter:
            output+=f",{p}"
        return output

    def setId(self, _id):
        self.id = _id

    def setParmameter(self, _paramList):
        for p in _paramList:
            self.parameter.append(p)
    
    def addParameter(self, _parameter):
        self.parameter.append(_parameter)

    def getId(self):
        return self.id

    def getParameters(self):
        return self.parameter

    def computeQueryProfile(self, db, tuple_frequency, attribute_frequency, target_user_profile):
        '''
        Compute a dictionary which describe the relevance of the
        most important features which characterize the given query

        db = relational table
        tuple_frequency: hash table such that tuple_frequency.getValue(t) = expected number of times tuple t appears in the result set of a query
        attribute_frequency: hash table such that attribute_frequency.getValue(t) = expected number of times attribute t appears in the result set of a query
        target_user_profile: the profile of the user which did not vote the target query
        '''
        query_def = str(self)
        query_result = db.query(query_def)

        #print(f"[{self.id}] : {str(self)}")
        #print(query_result)

        #feature attribute
        if len(self.parameter)<1:
            print(f"Error function computeQueryProfile. Query {self.id} has no search parameters.")
            exit(-1)

        #compute important search attribute for the target query
        self.parameter.sort(key=lambda x: attribute_frequency.getValue(x), reverse=True)
        self.ft_attribute[self.parameter[0]] = 1/len(self.parameter)

        for tuple_index, tuple_value in query_result.iterrows():
            tuple_id = int(tuple_value['id'])
            tuple_name = tuple_value['name']
            tuple_address = tuple_value['address']
            tuple_occupation = tuple_value['occupation']
            tuple_age = ageGroup(tuple_value['age'])
            tuple_cluster = tuple_value['cluster']

            self.tuples.append(tuple_id)

            self.values[tuple_name] = self.values.get(tuple_name, 0)+1
            self.values[tuple_address] = self.values.get(tuple_address, 0)+1
            self.values[tuple_occupation] = self.values.get(tuple_occupation, 0)+1
            self.values[tuple_age] = self.values.get(tuple_age, 0)+1
            
            self.clusters[tuple_cluster] = self.clusters.get(tuple_cluster, 0)+1

            self.resultLength += 1

        #print("result length: "+str(self.resultLength))
        #print("----")
        #print("")

        #sort tuples for importance
        if len(self.tuples)>0:
            self.tuples.sort(key=lambda x: tuple_frequency.getValue(x), reverse=True)
            self.ft_tuple[self.tuples[0]] = 1/self.resultLength

        #sort values for importance
        query_value_keys = list(self.values.keys())
        query_value_keys.sort(key=lambda x: self.values[x], reverse=True)
        for i in range(0, min(2, len(query_value_keys))):
            self.ft_value[query_value_keys[i]] = self.values[query_value_keys[i]]/self.resultLength
        
        #sort clusters for importance
        query_cluster_keys = list(self.clusters.keys())
        query_cluster_keys.sort(key=lambda x: self.clusters[x], reverse=True)
        for i in range(0, min(1, len(query_cluster_keys))):
            self.ft_cluster[query_cluster_keys[i]] = self.clusters[query_cluster_keys[i]]/self.resultLength

        #complete features about the target user taste
        user_important_tuples = target_user_profile.get_ft_tuple()
        user_important_attributes = target_user_profile.get_ft_attribute()
        user_important_values = target_user_profile.get_ft_value()
        user_important_clusters = target_user_profile.get_ft_cluster()

        for t in user_important_tuples:
            self.ft_tuple_user[t] = 0
        
        for a in user_important_attributes:
            self.ft_attribute_user[a] = 0
        
        for v in user_important_values:
            self.ft_value_user[v] = 0

        for c in user_important_clusters:
            self.ft_cluster_user[c] = 0

        #complete the features about the important attributes of the current user
        for p in user_important_attributes:
            if p in self.parameter:
                self.ft_attribute_user[p] = 1/len(self.parameter)

        #complete the features about the important tuples of the current user
        for t in user_important_tuples:
            if t in self.tuples:
                self.ft_tuple_user[t] = 1/self.resultLength

        #complete the features about the important values of the current user
        for v in user_important_values:
            if v in self.values:
                self.ft_value_user[v] = self.values[v]/self.resultLength

        #complete the features about the important clusters of the current user
        for c in user_important_clusters:
            if c in self.clusters:
                self.ft_cluster_user[c] = self.clusters[c]/self.resultLength
        #---

    def get_ft_tuple(self):
        return self.ft_tuple

    def get_ft_tuple_user(self):
        return self.ft_tuple_user

    def get_ft_value(self):
        return self.ft_value

    def get_ft_value_user(self):
        return self.ft_value_user

    def get_ft_attribute(self):
        return self.ft_attribute

    def get_ft_attribute_user(self):
        return self.ft_attribute_user

    def get_ft_cluster(self):
        return self.ft_cluster

    def get_ft_cluster_user(self):
        return self.ft_cluster_user
