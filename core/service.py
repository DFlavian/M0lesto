import json

from sqlalchemy import true

class service:
    def __init__(self, name, id):
        self.name = name
        self.status = "UP"
        self.id = id
        self.underattack = False
        self.exploited = False
        self.role = 0
        self.patched = True
        self.firstblood = False
    
    def check_status(self):
        #TODO: Implementare il check dalla scoreboard
        return self.status
    
    def json(self):
        return json.dumps(self.__dict__)

