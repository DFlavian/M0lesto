import json

class team():
    def __init__(self, name, id, nservices):
        self.name = name
        self.id = id
        self.score = 15000
        self.services = []
        for i in range(nservices):
            self.services.append({"id": i,"stolen": [0,0],"lost":[0,0]})
    
    def json(self):
        return json.dumps(self.__dict__)
