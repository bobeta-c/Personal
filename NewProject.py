from unicodedata import name
import hashlib
def bases(cls):
    #yields all classes used by cls except object class
    if cls != object:
        yield cls
        for direct_base in cls.__bases__:
            for base in bases(direct_base):
                yield base
def multElements(iterable):
    sum = 1
    for x in iterable:
        sum *= x
    return x
def hashStringtoColor(string):
    s = hashlib.sha256(string.encode())
    l = hashlib.sha1(string.encode())
    print(l)
    print(s)


class organism:
    instances = []
    aliveInstances = []
    def __init__(self, name = 'NaN', dimensions = (1,1,1), parents = (None, None), position = [0,0], data = {}, alive = True, energy = 0):
            self.name = name
            self.dimensions = dimensions
            self.parents = parents
            self.position = position
            self.energy = energy
            self.data = data
            self.alive = alive
            self.energyStore = multElements(self.dimensions)
            for x in bases(type(self)):
                x.instances.append(self)
                if self.alive == True:
                    x.aliveInstances.append(self)
            self.key = self.__class__.__name__
            self.color = hashStringtoColor(self.key)
    def getKey(self):
        return self.key
    def kill(self):
        print(f'killing {self.name}')
        self.alive = False
        for x in bases(type(self)):
            x.aliveInstances.remove(self)
    def isAlive(self):
        return self.alive
    def getName(self):
        return self.name
    def getPos(self):
        return (self.position[0], self.position[1])
    def move(self, newPosition):
        self.position = newPosition
    def consume(self, organism):
        organism.kill()
        self.energy += organism.energyStore
        organism.energyStore = 0
    def __str__(self):
        return self.name
    
class bean(organism):
    instances = []
    aliveInstances = []
class tree(organism):
    instances = []
    aliveInstances = []

class tileInfo:
    def __init__(self, **args):
        self.baseData = {}
        self.colorCodes = {}
        if args:
            self.baseData = args
        else:
            self.baseData['animals'] = []
            self.baseData['plants'] = []
            self.baseData['buildings'] = []
    def setColor(self, key, color):
        self.colorCodes[key] = color
    def getNkeys(self, n):
        keys = []
        index = 0
        for x in self.baseData:
            index += 1
            if n >= index:
                keys.append(x)
            else:
                return keys
        return keys
    def getColor(self, key):
        return self.colorCodes[key]
    def cpData(self):
        cpOfData = self.baseData.copy()
        for x in cpOfData:
            cpOfData[x] = self.baseData[x].copy()
        return cpOfData


class world:
    def __init__(self, name = 'NaN', dimensions = (10,10), data = tileInfo()):
        self.name = name
        self.dimensions = dimensions
        self.plot = {}
        self.data = data
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.plot[(x,y)] = self.data.cpData()
    def getDimensions(self):
        return self.dimensions[:]
    def getStr(self, key1, key2):
        string = ''
        for y in range(self.getDimensions()[1]):
            for x in range(self.getDimensions()[0]):
                location = (x,self.getDimensions()[1]-y-1)
                string += '['
                string += str(self.plot[location][key1])
                string += ' ' 
                string += str(self.plot[location][key2])
                string += ']'
            string += '\n'
        return string
    def __str__(self):
        keys = self.data.getNkeys(2)
        return self.getStr(keys[0], keys[1])
    def updateLocs(self, organisms):
        keys = []
        for i in organisms:
            if i.getKey() not in keys:
                keys.append(i.getKey())
        for i in organisms:
            if not i in self.plot[i.getPos()][i.getKey()] and i.isAlive():
                self.plot[i.getPos()][i.getKey()].append(i)
        indexes = []
        for i in self.plot:
            for key in keys:
                for x in self.plot[i][key]:
                    if x.getPos() != i or x.isAlive() == False:
                        indexes.append((i, x, key))
        for i in indexes:
            self.plot[i[0]][i[2]].remove(i[1])


def main():
    Tree = tree('tree')
    beany = bean('beany')
    Earth = world('earth', data = tileInfo(bean = [], tree = []))
    Earth.updateLocs(organism.instances)
    print(Earth)
    beany.consume(Tree)
    Earth.updateLocs(organism.instances)
    print(Earth)

#main()
hashStringtoColor('a')