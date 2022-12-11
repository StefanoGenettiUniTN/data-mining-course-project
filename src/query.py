'''
This class represents a query
'''
import database as db

class Query:

    def __init__(self, _id):
        '''
        _id --> id of the query
        '''
        self.id = _id
        self.parameter = []

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
