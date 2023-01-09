'''
Hash Table
Collision resolution by chaining.
The purpose of this class is to count approximately the number of occurences of a given value
in the resultsets of the query
'''

class HashTable:
    def __init__(self):
        #define number of buckets, it is recommended a prime number and to avoid power of 2
        self.num_buckets = 1223

        #init buckets values
        self.bucket = dict()
        for i in range(self.num_buckets):
            self.bucket[i] = 0
    
    def h(self, data):
        #hash function
        hash_code = hash(data)
        return hash_code % self.num_buckets

    def insertValue(self, data):
        #update the counter of the proper bucket
        key = self.h(data)
        self.bucket[key] += 1
    
    def getValue(self, data):
        #return the expected number of occurences of value data
        key = self.h(data)
        return self.bucket[key]