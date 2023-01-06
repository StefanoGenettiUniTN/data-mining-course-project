class Cluster:
    def __init__(self, _clusterId):
        self.id = _clusterId
        self.components = set()
        self.cardinality = 0

    def __str__(self):
        output = ""
        output += f"cluster id: {str(self.id)}\n"
        output += f"cardinality: {str(self.cardinality)}\n"
        output += f"components:\n"
        for c in self.components:
            output += f": {str(c)}\n"
        return output
        
    def addComponent(self, _component):
        self.components.add(_component)
        self.cardinality += 1