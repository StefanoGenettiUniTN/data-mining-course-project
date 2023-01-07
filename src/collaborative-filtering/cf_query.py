'''
Collaborative filtering query
'''

import cf_entity as entityClass

class CollaborativeFilteringQuery(entityClass.Entity):
    def __init__(self, _id, _def):
        super().__init__(_id)
        self.definition = _def