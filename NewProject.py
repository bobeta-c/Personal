from dis import dis
from operator import truediv
from turtle import pos
from unicodedata import name
import hashlib
from xml.dom import minidom
import pygame
import os
import random
from time import time
import matplotlib.pyplot as plt
import numpy
LOG = open('log.txt', 'w')
LOGTEXT = ''
DX, DY = 40, 40
def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func
def bases(cls):
    #yields all classes used by cls except object class
    if cls != object:
        yield cls
        for direct_base in cls.__bases__:
            for base in bases(direct_base):
                yield base
def inheritors(klass):
    subclasses = set()
    work = [klass]
    subclasses.add(klass)
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
def multElements(iterable):
    sum = 1
    for x in iterable:
        sum *= x
    return x
def hashStringtoColor(string):
    s = hashlib.sha256(string.encode())
    hash = s.digest()
    return (hash[0], hash[1], hash[2])
def findDistance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**(1/2)
class thing:
    hasColor = False
    @classmethod
    def getKey(cls):
        if hasattr(cls, 'key'):
            return cls.key
        return cls.__name__
    instances = []
    @staticmethod
    def reset():
        for obj in thing.instances:
            obj.exits = False
        for klass in inheritors(organism):
            klass.aliveInstances = []
        for klass in inheritors(thing):
            klass.instances = []
    def __init__(self, dimensions = (1,1,1), position = [0,0], data = {}, isSolid = True, hasGravity = False):
        self.isSolid = isSolid
        self.dimensions = dimensions
        self.position = position[:]
        self.data = data
        self.hasGravity = hasGravity
        self.exists = True
        thing.instances.append(self)
        if issubclass(type(self), tile):
            self.color = type(self).classColor
        else:
            self.color = hashStringtoColor(self.getKey())
    def getPos(self):
        return (self.position[0], self.position[1])
    def getColor(self):
        return self.color
    def move(self, newPosition):
        self.position = newPosition
    def doesExist(self):
        return self.exists
    def remove(self):
        self.exists = False

class tile(thing):
    hasColor = True
    classColor = (0,0,0)
    def __init__(self, dimensions = (1,1,1), position = [0,0], data = {}, type = 'base', color = None):
        super().__init__(dimensions, position, data)

class house(tile):
    classColor = (255,20,147)
           
    
class organism(thing):
    hasColor = False
    instances = []
    aliveInstances = []
    #HOW DO I MAKE THIS AUTOMATED AMONG ALL NEWLY CREATED CLASSES?
    def __init__(self, name = None, dimensions = (1,1,1), parents = (None, None), position = [0,0], data = {}, alive = True, energy = 0):
            super().__init__(dimensions, position, data, hasGravity = True)
            self.name = name
            self.dimensions = dimensions
            self.parents = parents
            self.energy = energy
            self.alive = alive
            self.energyStore = multElements(self.dimensions)
            if not name:
                if parents[0]:
                    self.name = parents[0].getName()[:3] + str(len(organism.instances))
                else:
                    self.name = self.__class__.__name__[0]+str(len(organism.instances))

            for x in bases(type(self)):
                x.instances.append(self)
                if self.alive == True and x != thing:
                    x.aliveInstances.append(self)
            LOG.write(self.name + f' created pos-{self.position}, energy-{self.energy}\n')
    def kill(self):
        LOG.write(f'killing {self.name}\n')
        self.alive = False
        self.exists = False
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
        LOG.write(self.name + f' ate {organism}, new energy-{self.energy}\n')
    def reproduce(self, mate, traits = {}):
        self.energy -= 1
        mate.energy -= 1
        if not 'position' in traits.keys():
            traits['position'] = list(self.getPos())
        return type(self)(parents = (self, mate),**traits)
    def mate(self, mate, area, traits = {}):
        if self.getPos() == mate.getPos() and self.energy >= 1 and mate.energy >= 1 and area.plot[self.getPos()][house.getKey()]:
            self.reproduce(mate, traits)
    def __str__(self):
        return self.name
    def interact(self, thing1, area):
        pass
    def hunger(self):
        if self.energy < 1:
            self.kill()
        else:
            self.energy -= 1

class bean(organism):
    instances = []
    aliveInstances = []
    def pathFind(self, area, goal = 'tree'):
        assert type(area) == world
        return (random.randint(0, area.getDimensions()[0]), random.randint(0, area.getDimensions()[1]))
    def interact(self, thing1, area):
        if self == thing1:
            return
        if issubclass(type(thing1), tree):
            self.consume(thing1)
        elif issubclass(type(thing1), bean):
            self.mate(thing1, area)

class predator(organism):
    instances = []
    aliveInstances = []
    def pathFind(self, area, goal = 'bean', radius = 3):
        locationsOfHouses = []
        for houseInstance in thing.instances:
            if type(houseInstance) == house and houseInstance.exists:
                locationsOfHouses.append(houseInstance.getPos())
        x, y = self.getPos()[0], self.getPos()[1]
        minDistance = None
        minPos = ()
        for beanInstance in bean.aliveInstances:
            testX, testY = beanInstance.getPos()[0], beanInstance.getPos()[1]
            working = True
            for housePos in locationsOfHouses:
                if findDistance(housePos, (testX,testY))<=radius:
                    working = False
                    break
            if working:
                distance = findDistance((x,y),(testX,testY))
                if not minDistance or distance < minDistance:
                    minPos = (testX, testY)
                    minDistance = distance
        return minPos if minPos != () else self.getPos()
    def interact(self, thing1, area):
        if self == thing1:
            return
        if issubclass(type(thing1), tree):
            pass
        elif issubclass(type(thing1), bean):
            self.consume(thing1)
            area.updateLocs([thing1])
        elif issubclass(type(thing1), predator):
            self.mate(thing1, area)
    def move(self, newPosition):
        self.position = newPosition
        #self.energy -= .1
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
    def pathFind(self,area, goal1 = 'tree', goal2 = 'house'):
        assert type(area) == world
        if 1 == 2:
            radius = 0
            goal = goal1 if self.energy < 1 else goal2
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
        else:
            goal = goal1 if self.energy < 1 else goal2
            x, y = self.getPos()[0], self.getPos()[1]
            minDistance = None
            minPos = ()
            if goal == 'tree':
                for treeInstance in tree.aliveInstances:
                    testX, testY = treeInstance.getPos()[0], treeInstance.getPos()[1]
                    distance = ((testX-x)**2+(testY-y)**2)**(1/2)
                    if not minDistance or distance < minDistance:
                        minPos = (testX, testY)
                        minDistance = distance
                return minPos if minPos != () else self.getPos()
            elif goal == 'house':
                for houseInstance in thing.instances:
                    if type(houseInstance) == house and houseInstance.exists:
                        testX, testY = houseInstance.getPos()[0], houseInstance.getPos()[1]
                        distance = ((testX-x)**2 + (testY-y)**2)**(1/2)
                        if not minDistance or distance < minDistance:
                            minPos = (testX, testY)
                            minDistance = distance
                return minPos if minPos != () else self.getPos()
        return self.getPos()
class smartMatingBean(matingBean):
    def pathFind(self,area, goal1 = 'tree', goal2 = 'house'):
        for pred in predator.aliveInstances:
            if findDistance(self.getPos(), pred.getPos()) < 3:
                xChange = pred.getPos()[0]-self.getPos()[0]
                yChange = pred.getPos()[1]-self.getPos()[1]
                if numpy.sign(yChange)!= 0 and 0 <= self.getPos()[1] + numpy.sign(yChange) <= area.getY():
                    return (self.getPos()[0], self.getPos()[1]+numpy.sign(yChange))
                elif numpy.sign(xChange)!= 0 and 0 <= self.getPos()[0] + numpy.sign(xChange) <= area.getX():
                    return (self.getPos()[0]+numpy.sign(yChange), self.getPos()[1])
                else:
                    return bean.pathFind(self, area, goal1)
        return matingBean.pathFind(self, area, goal1, goal2)

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
    def __init__(self, name = 'NaN', dimensions = (DX, DY), data = tileInfo()):
        self.name = name
        self.dimensions = dimensions
        self.plot = {}
        self.data = data
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.plot[(x,y)] = self.data.cpData()
    def reset(self):
        organism.reset()
        for coord in self.plot:
            self.plot[coord] = self.data.cpData()
    def getDimensions(self):
        return self.dimensions[:]
    def getX(self):
        return self.dimensions[0]
    def getY(self):
        return self.dimensions[1]
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
        LOG.write(f'populating: type-random, beans-{len(bean.aliveInstances)}, trees-{len(tree.aliveInstances)}\n')
    def moveOrganism(self, organism, newLocation):
        if newLocation in self.plot:
            organism.move(newLocation)
        else:
            return 12
        self.updateLocs([organism])
    def moveOrganismGradual(self, organism, goalLocation):
        assert goalLocation in self.plot
        position = organism.getPos()
        xChange = goalLocation[0]-position[0]
        yChange = goalLocation[1]-position[1]
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
    def controlledPopulate(self, organismType, num):
        for _ in range(num):
            position = (random.randrange(0,self.getX()), random.randrange(0,self.getY()))
            self.plot[position][organismType.getKey()].append(organismType(position = list(position), dimensions = (1, random.randrange(1,3), 1)))
        self.updateLocs(organismType.instances)
        LOG.write(f'populating: type-controlled, beans-{len(bean.aliveInstances)}, trees-{len(tree.aliveInstances)}\n')
    def resetDisplay(self, screen, background):
        screen.fill(background)
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
    def tryActions(self, organisms):
        for org in organisms:
            for x in self.plot[org.getPos()]:
                for y in self.plot[org.getPos()][x]:
                    org.interact(y, self)
                    self.updateLocs([y])        
    def updateLocs(self, organisms):
        keys = []
        for i in organisms:
            if i.getKey() not in keys:
                keys.append(i.getKey())
        for i in organisms:
            if not i in self.plot[i.getPos()][i.getKey()] and i.doesExist():
                self.plot[i.getPos()][i.getKey()].append(i)
        indexes = []
        for i in self.plot:
            for key in keys:
                for x in self.plot[i][key]:
                    if x.getPos() != i or x.doesExist() == False:
                        indexes.append((i, x, key))
        for i in indexes:
            self.plot[i[0]][i[2]].remove(i[1])
    def sendEdges(self, organisms):
        '''
        Sends all organisms to the edges of the world
        random
        '''
        for org in organisms:
            print(org)
            edge = random.randint(1,4)
            randx = random.randrange(0,self.getX())
            randy = random.randrange(0,self.getY())
            positions = {1:[0,randy], 2:[self.getX()-1, randy], 3:[randx, 0], 4:[randx, self.getY()-1]}
            org.move(positions[edge])
    def killAll(self, organismType):
        for org in organismType.aliveInstances:
            org.kill()
            self.updateLocs([org])
    def inflictHunger(self, organisms):
        for x in organisms:
            x.hunger()
        self.updateLocs(organisms)

def main():
    for dimension in range(25,36, 5):
        DX, DY, inputData = dimension, dimension, tileInfo(**{bean.getKey():[], house.getKey():[], tree.getKey():[], predator.getKey():[]})
        screen, background = setup()
        Earth = world('earth', data = inputData, dimensions = (DX,DY))
        Earth.reset()
        LOG.write(f'Simulation size-{dimension}')
        for _ in range(4):
            matingBean(energy = 1)
        predator('killa', energy = 1)
        house(position = [DX//2, DY//2], color = house.classColor)
        Earth.updateLocs(thing.instances)
        LOG.write(f'beans-{len(bean.aliveInstances)}, trees-{len(tree.aliveInstances)}\n\n\n')

        popOverTime = simulate(Earth, screen, background, auto = False)

        plt.plot(popOverTime)
        LOG.write(f'final population-{popOverTime[-1]}, dimension-{dimension}')
        plt.ylabel('population')
        plt.title(f'dimension-{dimension}')
        plt.show()

def setup(size = (1000,1000)):
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
    return screen, background

def simulate(world, screen, background, displayType = False, auto = True):
    population =[len(bean.aliveInstances)]
    playing = True
    count = 0
    world.updateLocs(organism.instances)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                count, population = currentSimulation(world, count, screen, background, population, display = True)
            elif event.type == pygame.QUIT:
                playing = False
        if auto:
            if count < 2000:
                count, population = currentSimulation(world, count, screen, background, population, display = displayType)
            else:
                playing = False
    pygame.quit()
    return population
#@timer_func
def currentSimulation(area, count, screen, background,population, display = False):
    if not count % (area.getDimensions()[0]):
        area.killAll(tree)
        area.resetDisplay(screen, background)
        area.sendEdges(bean.aliveInstances+predator.aliveInstances)
        area.controlledPopulate(tree, round((area.getDimensions()[0]*area.getDimensions()[1])*0.05))
        area.inflictHunger(bean.aliveInstances+predator.aliveInstances)
        population.append(len(bean.aliveInstances))
    if display:
        area.updateDisplay(screen, background, dmod = '4seg')
        pygame.display.flip()
    area.tryActions(bean.aliveInstances+predator.aliveInstances)
    moveOrganismsGradual(area, bean.aliveInstances+predator.aliveInstances)
    return count + 1, population

def moveOrganismsGradual(area, organisms):
    assert type(area) == world
    for x in organisms:
        area.moveOrganismGradual(x,x.pathFind(area))
main()
LOG.close() 