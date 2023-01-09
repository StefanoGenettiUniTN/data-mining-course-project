'''
Collaborative filtering user
'''

import cf_entity as entityClass

class CollaborativeFilteringUser(entityClass.Entity):
    def __init__(self, _id):
        super().__init__(_id)