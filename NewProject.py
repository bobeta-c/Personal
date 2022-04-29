from unicodedata import name


class organism:
    organisms = []
    organismsAlive = []
    def __init__(self, name = 'NaN', dimensions = (1,1,1), parents = (None, None), position = [0,0], data = {}, alive = True):
            self.name = name
            self.dimensions = dimensions
            self.parents = parents
            self.position = position
            self.data = data
            self.alive = alive
            organism.organisms.append(self)
            if self.alive == True:
                organism.organismsAlive.append(self)
            self.key = 'organism'
    def getKey(self):
        return self.key
    def kill(self):
        self.alive == False
        organism.organismsAlive.remove(self)
    def getName(self):
        return self.name
    def getPos(self):
        return (self.position[0], self.position[1])
    def move(self, newPosition):
        self.position = newPosition

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
        return self.baseData


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
        key = organisms[0].getKey()
        for i in organisms:
            if not i in self.plot[i.getPos()][i.getKey()]:
                self.plot[i.getPos()][i.getKey()].append(i)

        indexes = []
        
        for i in self.plot:
            for x in self.plot[i][key]:
                if x.getPos() != i:
                    indexes.append((i, x))
        for i in indexes:
            self.plot[i[0]][key].remove(i[1])


def main():
    Asher = organism('Asher')
    Earth = world('earth', data = tileInfo(organism = [], food = []))
    Earth.updateLocs(organism.organismsAlive)
    print(Earth.getStr())

main()