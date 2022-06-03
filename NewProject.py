from operator import truediv
from turtle import pos
from unicodedata import name
import hashlib
import pygame
import os
import random
import time
LOG = open('log.txt', 'w')
LOGTEXT = ''
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
    hash = s.digest()
    return (hash[0], hash[1], hash[2])

class thing:
    hasColor = False
    @classmethod
    def getKey(cls):
        if cls.hasColor == False:
            return cls.__name__
        return cls.getColor()
    instances = []
    def __init__(self, dimensions = (1,1,1), position = [0,0], data = {}, isSolid = True, hasGravity = False):
        self.isSolid = isSolid
        self.dimensions = dimensions
        self.position = position[:]
        self.data = data
        self.color = hashStringtoColor(self.getKey())
        self.hasGravity = hasGravity
    def getPos(self):
        return (self.position[0], self.position[1])
    def getColor(self):
        return self.color
    def move(self, newPosition):
        self.position = newPosition
class tile(thing):
    hasColor = True
    def __init__(self, dimensions = (1,1,1), position = [0,0], data = {}, type = 'base', color = (0,0,0)):
        super().__init__(dimensions, position, data)
        self.color = color
        
    
    
class organism(thing):
    hasColor = False
    instances = []
    aliveInstances = []
    @classmethod
    def getKey(cls):
        if hasattr(cls, 'key'):
            return cls.key
        return cls.__name__
    

    #HOW DO I MAKE THIS AUTOMATED AMONG ALL NEWLY CREATED CLASSES?
    def __init__(self, name = 'NaN', dimensions = (1,1,1), parents = (None, None), position = [0,0], data = {}, alive = True, energy = 0):
            super().__init__(dimensions, position, data, hasGravity = True)
            self.name = name
            self.dimensions = dimensions
            self.parents = parents
            self.position = position
            self.energy = energy
            self.alive = alive
            self.energyStore = multElements(self.dimensions)
            for x in bases(type(self)):
                x.instances.append(self)
                if self.alive == True and x != thing:
                    x.aliveInstances.append(self)
            LOG.write(name + 'created'+'\n')
    def kill(self):
        LOG.write(f'killing {self.name}\n')
        self.alive = False
        for x in bases(type(self)):
            if x != thing:
                x.aliveInstances.remove(self)
    def isAlive(self):
        return self.alive
    def getName(self):
        return self.name
    def consume(self, organism):
        organism.kill()
        self.energy += organism.energyStore
        organism.energyStore = 0
    def reproduce(self, mate, traits = None):
        self.energy -= 1
        mate.energy -= 1
        return type(self)(parents = (self, mate),*traits)
    def __str__(self):
        return self.name
    
class bean(organism):
    instances = []
    aliveInstances = []
    def pathFind(self, area, goal = 'tree'):
        assert type(area) == world
        return (random.randint(0, area.getDimensions()[0]), random.randint(0, area.getDimensions()[1]))

class hungryBean(bean):
    key = bean.getKey()
    instances = []
    aliveInstances = []
    def pathFind(self,area,goal = 'tree'):
        assert type(area) == world
        radius = 0
        checked = []
        found = False
        while not found and (radius <= area.getDimensions()[0] or radius <= area.getDimensions()[1]):
            minx = self.getPos()[0] - radius if self.getPos()[0] - radius >= 0 else 0
            miny = self.getPos()[1] - radius if self.getPos()[1] - radius >= 0 else 0
            maxx = self.getPos()[0] + radius if self.getPos()[0] + radius <= area.getDimensions()[0] else area.getDimensions()[0]
            maxy = self.getPos()[1] + radius if self.getPos()[1] + radius <= area.getDimensions()[1] else area.getDimensions()[1]
            for x in range(minx, maxx):
                for y in range(miny,maxy):
                    if area.plot[(x,y)][goal]:
                        return (x,y)
                    checked.append((x,y))
            radius += 1
        return self.getPos()
class matingBean(bean):
    key = bean.getKey()
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
    def randomPopulate(self, organismType, percentChance):
        for index in self.plot:
            if random.random() <= percentChance:
                temp = organismType(position = list(index))
                self.plot[index][organismType.getKey()].append(temp)
        self.updateLocs(organismType.instances)
    def moveOrganism(self, organism, newLocation):
        if newLocation in self.plot:
            organism.move(newLocation)
        else:
            return 12
        self.updateLocs([organism])
    def moveOrganismGradual(self, organism, goalLocation):
        assert goalLocation in self.plot
        position = organism.getPos()
        if goalLocation[0] > position[0]:
            self.moveOrganism(organism, (position[0]+1, position[1]))
            return
        elif goalLocation[0] < position[0]:
            self.moveOrganism(organism, (position[0]-1, position[1]))
            return
        elif goalLocation[1] > position[1]:
            self.moveOrganism(organism, (position[0], position[1]+1))
            return
        elif goalLocation[1] < position[1]:
            self.moveOrganism(organism, (position[0], position[1]-1))
            return
        return

    def updateDisplay(self, screen, background, dmod = '4seg'):
        dimensions = screen.get_size()
        xIncrement = dimensions[0]//self.getDimensions()[0]
        yIncrement = dimensions[1]//self.getDimensions()[1]
        keys = list(self.plot[(0,0)].keys())
        if len(keys) > 4:
            keys = keys[:4]
        xHalfIncrement = xIncrement//2
        yHalfIncrement = yIncrement//2
        if dmod == '4seg':
            for i in self.plot:
                index = i
                location = (index[0]*xIncrement, index[1]*yIncrement)
                locationType0 = (location, (location[0] + xHalfIncrement, location[1] + yHalfIncrement))
                locationType1 = ((location[0]+xHalfIncrement, location[1]), (location[0]+xIncrement, location[1] + yHalfIncrement))
                locationType2 = ((location[0], location[1] + yHalfIncrement), (location[0] +xHalfIncrement, location[1]+yIncrement))
                locationType3 = ((location[0] +xHalfIncrement, location[1] +yHalfIncrement), (location[0] + xIncrement,location[1]+yIncrement))
                locations= [locationType0,locationType1,locationType2,locationType3]

                for keyIndex in range(4):
                    if keyIndex < len(keys) and len(self.plot[index][keys[keyIndex]]) > 0:
                        pygame.draw.rect(screen, hashStringtoColor(keys[keyIndex]), pygame.Rect(locations[keyIndex]))
                    else:
                        pygame.draw.rect(screen, background, pygame.Rect(locations[keyIndex]))
        elif dmod == '1seg':
            for index in self.plot:
                location = (index[0]*xIncrement, index[1]*yIncrement)
                locationUsed = (location, (location[0]+xIncrement, location[1]+yIncrement))
                worked = False
                for keyIndex in range(4):
                    if keyIndex < len(keys) and len(self.plot[index][keys[keyIndex]]) > 0:
                        pygame.draw.rect(screen, hashStringtoColor(keys[keyIndex]), pygame.Rect(locationUsed))
                        worked = True
                        break
                if not worked:
                    pygame.draw.rect(screen, background, pygame.Rect(locationUsed))


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
    beany = hungryBean('beany')
    Earth = world('earth', data = tileInfo(bean = [], tile = [], tree = []), dimensions = (40,40))
    Earth.updateLocs(organism.instances)
    #print(Earth)
    beany.consume(Tree)
    #print(Earth)
    Earth.moveOrganism(beany, (4,4))
    #print(Earth)
    display(Earth)

def display(world, size = (1000,1000)):
    pygame.init()
    cd = os.getcwd()
    filePath = cd + '/logo32x32.png'
    logo = pygame.image.load(filePath)
    pygame.display.set_icon(logo)
    screen = pygame.display.set_mode(size)
    
    background = (0,0,0)
    screen.fill(background)
    screen.blit(logo, (240-32,180-32))
    pygame.display.flip()

    playing = True
    count = 0
    world.updateLocs(organism.instances)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ('displaying')
                world.updateDisplay(screen, background, dmod = '4seg')
                pygame.display.flip()
                count += 1
                if count%5 == 0:
                    world.randomPopulate(tree, .002)
                    print('populating')

                #print(pygame.mouse.get_pos())
                world.moveOrganismGradual(bean.aliveInstances[0], bean.aliveInstances[0].pathFind(world))
            elif event.type == pygame.QUIT:
                playing = False
    pygame.quit()


main()
LOG.close()