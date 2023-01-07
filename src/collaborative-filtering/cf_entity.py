'''
In collaborative filtering according to the duality of similarity
both users and queries are abstracted with the same class
'''

class Entity:
    def __init__(self, _id):
        self.id = _id

        #average vote of the user/query
        self.averageVote = -1

        #votedEntities[e] = vote assigned by user u to query q
        self.votedEntities = dict()

        #set of queries/users without vote
        self.unvotedEntities = set()

        #completed==True iff all the entities for the target user/query are voted
        self.completed = False

        #each entity belongs to a certain cluster
        self.cluster = -1
    
    def __str__(self):
        return str(self.id)

    def computeAvgVote(self):
        sum = 0
        cardinality = 0

        for e in self.votedEntities:
            sum += self.votedEntities[e]
            cardinality += 1
        
        if cardinality>0:
            self.averageVote = sum/cardinality
            return sum/cardinality
        self.averageVote = -1
        return -1

    def addVotedEntity(self, _entityId, _vote):
        self.votedEntities[_entityId] = _vote
        if _entityId in self.unvotedEntities:
            self.unvotedEntities.remove(_entityId)
            if len(self.unvotedEntities)==0:
                self.completeEntity()
    
    def addUnvotedEntity(self, _entityId):
        self.unvotedEntities.add(_entityId)

    def completeEntity(self):
        self.completed = True

    def setCluster(self, _newCluster):
        self.cluster = _newCluster
        