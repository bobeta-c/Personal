from cgi import test
from dis import dis
from gettext import find
from operator import truediv
from tracemalloc import start
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
def createInstances(instanceData, **atributes):
    for instanceType in instanceData:
        assert type(instanceType) == tuple and len(instanceType) == 2
        for i in range(instanceType[1]):
            instanceType[0](**atributes)
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
                self.name = type(self).__name__[0] + str(len(type(self).instances))

            for x in bases(type(self)):
                x.instances.append(self)
                if self.alive == True and x != thing:
                    x.aliveInstances.append(self)
            #LOG.write(self.name + f' created pos-{self.position}, energy-{self.energy}\n')
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
        self.energy += organism.energyStore + organism.energy
        organism.energyStore = 0
        LOG.write(self.name + f' ate {organism}, new energy-{self.energy}\n')
    def reproduce(self, mate, traits = {}):
        if type(self) == predator:
            self.energy -= 10
            mate.energy -= 10
        else:
            self.energy -= 1
            mate.energy -= 1
        if not 'position' in traits.keys():
            traits['position'] = list(self.getPos())
        if not 'energy' in traits.keys():
            traits['energy'] = 2
        LOG.write(f'{self} and {mate} reproduced')
        return type(self)(parents = (self, mate),**traits)

    def mate(self, mate, area, traits = {}):
        needsHouse = True if issubclass(type(self), bean) else False
        if self.getPos() == mate.getPos() and self.energy >= 1 and mate.energy >= 1 and (area.plot[self.getPos()][house.getKey()]or not needsHouse):
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
        return (random.randrange(0, area.getDimensions()[0]), random.randrange(0, area.getDimensions()[1]))
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
            if findDistance((x,y), (testX,testY)) <= radius:
                distance = findDistance((x,y),(testX,testY))
                if not minDistance or distance < minDistance:
                    minPos = (testX, testY)
                    minDistance = distance
        if minPos != ():
            return minPos
        else:
            if self.energy >= 11:
                for pred in predator.aliveInstances:
                    testDistance = findDistance((x,y), pred.getPos())
                    if (not minDistance or testDistance< minDistance) and pred != self:
                        minPos = (pred.getPos())
                        minDistance = testDistance
        if minPos != ():
            return minPos
        return (random.randrange(0, area.getDimensions()[0]), random.randrange(0, area.getDimensions()[1]))
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
            goal = goal1 if self.energy < 3 else goal2
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
        print(organism, goalLocation)
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

def main(dimension=10, matingBeans= 0, smartMatingBeans = 0, predators = 0, energy = 1, doAuto = True, cycles = 1000, daylengthRatio = 1.2, treeRatio = .05, displayType = False, show = False, seg1 = '4seg'):
    DX, DY, inputData = dimension, dimension, tileInfo(**{bean.getKey():[], house.getKey():[], tree.getKey():[], predator.getKey():[]})
    screen, background = setup()
    Earth = world('earth', data = inputData, dimensions = (DX,DY))
    Earth.reset()
    LOG.write(f'Simulation size-{dimension}')
    createInstances([(matingBean,matingBeans),(smartMatingBean,smartMatingBeans),(predator,predators)], **{'energy':energy})
    house(position = [DX//2, DY//2], color = house.classColor)
    Earth.updateLocs(thing.instances)
    LOG.write(f'beans-{len(bean.aliveInstances)}, trees-{len(tree.aliveInstances)}\n\n\n')

    popOverTime = simulate(Earth, screen, background, daylengthRatio, treeRatio, displayType, auto = doAuto, kcycles = cycles, segm1=seg1)
    for name, data in popOverTime.items():
        if name not in ['organism', 'tree', 'bean']:
            plt.plot(data, label=name)
    LOG.write(f'final population-{popOverTime["organism"][-1]}, dimension-{dimension}')
    plt.ylabel('population')
    plt.xlabel('days')

    plt.legend(loc = 'right')
    plt.title(f'dimension-{dimension}, trees-{treeRatio}, dayLen-{daylengthRatio}, energy-{energy}')
    if show:
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

def simulate(world, screen, background, dlRatio, treeRatio,  dType = False, auto = True, kcycles = 2000, segm1 = '4seg'):
    population ={klass.__name__:[len(klass.aliveInstances)] for klass in inheritors(organism)}
    playing = True
    count = 0
    world.updateLocs(organism.instances)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                count, population = currentSimulation(world, count, screen, background, population, dlRatio, treeRatio, display = True, seg1 = segm1)
            elif event.type == pygame.QUIT:
                playing = False
        if auto:
            if count < kcycles:
                count, population = currentSimulation(world, count, screen, background, population, dlRatio,treeRatio, display = dType, seg1 = segm1)
            else:
                playing = False
    pygame.quit()
    return population
#@timer_func
def currentSimulation(area, count, screen, background,population, ratio,treeRatio, display = False, seg1 = '4seg'):
    if not count % abs(area.getDimensions()[0]*(ratio)):
        area.killAll(tree)
        area.resetDisplay(screen, background)
        area.sendEdges(bean.aliveInstances+predator.aliveInstances)
        area.controlledPopulate(tree, round((area.getDimensions()[0]*area.getDimensions()[1])*treeRatio))
        area.inflictHunger(bean.aliveInstances+predator.aliveInstances)
        for klass in inheritors(organism):
            population[klass.__name__].append(len(klass.aliveInstances))
    if display:
        area.updateDisplay(screen, background, dmod = seg1)
        pygame.display.flip()
    area.tryActions(bean.aliveInstances+predator.aliveInstances)
    moveOrganismsGradual(area, bean.aliveInstances+predator.aliveInstances, count)
    return count + 1, population

def moveOrganismsGradual(area, organisms, count):
    assert type(area) == world
    for x in organisms:
        if type(x) == predator and False:
            area.moveOrganismGradual(x,x.pathFind(area))
        area.moveOrganismGradual(x,x.pathFind(area))

main(predators = 0, smartMatingBeans=0, matingBeans=2, dimension = 8,energy = 1,doAuto = False, show=True, treeRatio = .05, cycles = 1000, daylengthRatio= 1.5)
main(predators = 0,matingBeans=4,doAuto=True,energy = 1,displayType=True,show=True,treeRatio=.05,cycles=1000, dimension = 14, daylengthRatio=1)
for xlen in range(10, 41, 10):
    main(matingBeans=2, dimension=xlen, energy=1, show = True)
main(predators = 2, smartMatingBeans=0, matingBeans=20, dimension = 18,energy = 2,doAuto = False, show=True, treeRatio = .1, cycles = 1000, daylengthRatio= 1.5)
for x in range(5):
    main(predators = 2, smartMatingBeans=0, matingBeans=20, dimension = 18,energy = 2,doAuto = True, show=True, treeRatio = .1, cycles = 1000, daylengthRatio= 1)
main(matingBeans=2,doAuto=False, seg1 = '1seg')


LOG.close() 