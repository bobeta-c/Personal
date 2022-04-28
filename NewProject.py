from unicodedata import name


class organism:
    def __init__(self, name = 'NaN', dimensions = (1,1,1), parents = (None, None), position = [0,0], data = {}):
            self.name = name
            self.dimensions = dimensions
            self.parents = parents
            self.position = position
            self.data = data
    def getName(self):
        return name
    def getPos(self):
        return self.position[:]
    def move(self, newPosition):
        self.position = newPosition

class tileInfo:
    def __init__(self, **args):
        self.baseData = {}
        if args:
            self.baseData = args
        else:
            self.baseData['animals'] = []
            self.baseData['plants'] = []
            self.baseData['buildings'] = []
    def setColor(self, key, color):
        pass
    def cpData(self):
        return self.baseData


class world:
    def __init__(self, name = 'NaN', dimensions = (10,10), data = tileInfo()):
        self.name = name
        self.dimensions = dimensions
        self.plot = {}
        self.data = data
        for x in self.dimensions[0]:
            for y in self.dimensions[1]:
                self.plot[(x,y)] = self.data.cpData()
    