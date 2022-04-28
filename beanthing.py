from asyncio import wait_for
from logging import raiseExceptions
import random
import pygame
import sys

class bean:
    
    instances = []
    aliveInstances = []
    names = []
    def __init__(self, name, height, weight, fertility, parent1 = None, parent2 = None, posX = None, posY = None, stomach = 0):
        self.alive = True
        self.name = name
        self.height = height
        self.weight = weight
        self.fertility = fertility
        self.offspring = 0
        self.parent1 = parent1
        self.parent2 = parent2
        self.posX = posX
        self.posY = posY
        self.stomach = stomach
        self.energyReq = 1
        bean.aliveInstances.append(self)
        bean.updateInstances()
    def getX(self):
        return self.posX
    def getY(self):
        return self.posY
    def getPos(self):
        return (self.posX, self.posY)
    def eat(self, amount = 1):
        self.stomach += amount
    def updateInstances():
        for x in bean.aliveInstances:
            if x not in bean.instances:
                bean.instances.append(x)
    def kill(self):
        self.alive = False
        bean.aliveInstances.remove(self)
    def __str__(self):
        return self.getName()
    def getBeans():
        '''
        warning: not a copy
        '''
        return bean.aliveInstances
    def getNames():
        bean.names = []
        for x in bean.aliveInstances:
            if x.name not in bean.names:
                bean.names.append(x.name)
        return bean.names
    def getName(self):
        return str(self.name)
    def canReproduce(self):
        return bool(self.stomach)
    def reproduce(bean1, bean2, name = None):
        if bean1 == bean2:
            return 1
        if (random.random() <= bean1.fertility and random.random() <= bean2.fertility):
            if (name and name not in bean.getNames()):
                newname = name
            else:
                newname = bean1.name + str(bean1.offspring)+'-'
            newheight = (bean1.height + bean2.height)/2
            newweight = 1
            newfertility = (bean1.fertility + bean2.fertility)/2
            bean1.offspring += 1
            bean2.offspring += 1
            for x in [bean1, bean2]:
                if (x.stomach - x.energyReq) > 0:
                    x.stomach -= x.energyReq
                else:
                    x.stomach = 0
            return (type(bean1)(newname, newheight, newweight, newfertility, bean1, bean2, posX = bean1.posX, posY = bean1.posY))
        return None
    def pathFind(self, field):
        pass
    def move(self, newX, newY):
        self.posX = newX
        self.posY = newY
    def nextSquare(self, field, func):
        '''
        returns the square bean should go to on its path to target
        returns beans current square if already at target
        moves X then Y
        '''
        goalLoc = func(self, field)
        if not goalLoc:
            return None
        if goalLoc == self.getPos():
            return self.getPos()
        if goalLoc[0] != self.getX():
            if goalLoc[0] < self.getX():
                return (self.getX()-1,self.getY())
            return (self.getX()+1, self.getY())
        elif goalLoc[1] != self.getY():
            if goalLoc[1] < self.getY():
                return (self.getX(), self.getY()-1)
            return (self.getX(),self.getY()+1)
        raise Exception

class hungry_bean(bean):
    def pathFind(self, field):
        closestFood = None
        closestHouse = None
        locationFood = None
        locationHouse = None
        for x in field.plot:
            if field.plot[x][0] >= 1:
                dist = ((x[0]-self.getX())**2 + (x[1]-self.getY())**2)**(1/2)
                if (closestFood == None) or dist < closestFood:
                    closestFood = dist
                    locationFood = x
            if field.plot[x][2] > 0:
                dist = ((x[0]-self.getX())**2 + (x[1]-self.getY())**2)**(1/2)
                if (closestHouse == None) or dist < closestHouse:
                    closestHouse = dist
                    locationHouse = x

        if locationFood:
            return locationFood
        elif locationHouse:
            return locationHouse
        else:
            return None
class bozo_bean(bean):
    def pathFind(self, field):
        closestHouse = None
        locationHouse = None
        for x in field.plot:
            if field.plot[x][2] > 0 and self.canReproduce():
                dist = ((x[0]-self.getX())**2 + (x[1]-self.getY())**2)**(1/2)
                if (closestHouse == None) or dist < closestHouse:
                    closestHouse = dist
                    locationHouse = x
        if locationHouse:
            return locationHouse
        else:
            return (self.getX()+ random.randint(-1,1), self.getY() + random.randint(-1,1))


class field:
    def __init__(self, name, sizeX, sizeY):
        self.name = name
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.plot = {}
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.plot[(x, y)] = [0, [], 0]
    def randomPopulation(self, percentChance = .3):
        for x in self.plot:
            if (random.random() <= percentChance):
                self.plot[x][0] += 1
    def controlledPopulation(self, locations):
        for x in locations:
            self.plot[x][0] += 1
    def controlledHouse(self, locations):
        for x in locations:
            self.plot[x][2] += 1
    def __str__(self):
        string = ''
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                try:
                    beansOnTile = len(self.plot[x, self.sizeY-y-1][1])
                except:
                    pass
                string = string + str([self.plot[(x, self.sizeY-y-1)][0], beansOnTile])
                #string = string + str(self.plot[x, self.sizeY-y-1])
            string = string + '\n'
        return string[:-1]
    def display(self, screen):
        screen.fill((120,120,120))
        dimensions = screen.get_size()
        xIncrement = dimensions[0]//self.sizeX
        yIncrement = dimensions[1]//self.sizeY
        for i in self.plot:
            index = i
            location = (index[0]*xIncrement, index[1]*yIncrement)
            location2 = (location[0]+xIncrement,location[1]+xIncrement)
            if len(self.plot[index][1]) > 0:
                lengthOfPlot = len(self.plot[index][1])
                if (25*lengthOfPlot <255):
                    color = (25*lengthOfPlot,12*lengthOfPlot,4*lengthOfPlot)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, (color), pygame.Rect(location,location2))
            elif self.plot[index][0] > 0:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(location,location2))
            elif self.plot[index][2] > 0:
                pygame.draw.rect(screen, (0,105,29), pygame.Rect(location,location2))  
            else:
                pygame.draw.rect(screen, (120,120,120), pygame.Rect(location,location2))
        #pygame.draw.rect(screen, (0,0,0), pygame.Rect((dimensions[0]-20, yIncrement*16), (dimensions[0], yIncrement*17)))
        pygame.display.flip()
    def beanEat(self, beans):
        for x in beans:
            if self.plot[x.getPos()][0] > 0:
                self.plot[x.getPos()][0] -= 1
                x.eat()
    def beanReproduce(self, beans):
        for x in self.plot:
            if len(self.plot[x][1]) > 1:
                ableToReproduce = True
                for i in self.plot[x][1][:2]:
                    if not i.canReproduce():
                        ableToReproduce = False
                if ableToReproduce:
                    bean.reproduce(self.plot[x][1][0],self.plot[x][1][1])
        self.updateLocs(bean.aliveInstances)

    def beanPopulate(self, beans):
        perSide = int(len(beans)/4)
        side = 0
        beansUsed = []
        for x in range(4):
            side += 1
            for y in range(perSide):
                if beans[(x*perSide)+y] not in beansUsed:
                    if side == 1:
                        beans[(x*perSide)+y].posX, beans[(x*perSide)+y].posY = 0, random.randrange(0, self.sizeY)
                    elif side == 2:
                        beans[(x*perSide)+y].posX, beans[(x*perSide)+y].posY = self.sizeX-1, random.randrange(0, self.sizeY)
                    elif side == 3:
                        beans[(x*perSide)+y].posX, beans[(x*perSide)+y].posY = random.randrange(0, self.sizeX), 0
                    elif side == 4:
                        beans[(x*perSide)+y].posX, beans[(x*perSide)+y].posY = random.randrange(0, self.sizeX), self.sizeY-1
                    beansUsed.append(beans[(x*perSide+y)])
        for x in range(len(beans)):
            if beans[x] not in beansUsed:
                beans[x].posX, beans[x].posY = random.randrange(0, self.sizeX), random.randrange(0, self.sizeY)
                beansUsed.append(beans[x])
        self.updateLocs(bean.aliveInstances)
    def moveBean(self, beanUsed, newPos):
        beanUsed.posX = newPos[0]
        beanUsed.posY = newPos[1]
        self.updateLocs([beanUsed])
    def updateLocs(self, beans):
        for x in beans:
            if not x in self.plot[(x.posX, x.posY)][1]:
                self.plot[x.posX, x.posY][1].append(x)
        indexes = []
        for x in self.plot:
            for y in range(len(self.plot[x][1])):
                if issubclass(type(self.plot[x][1][y]), bean) and self.plot[x][1][y].getPos() != x: 
                    indexes.append((x, self.plot[x][1][y]))
        for i in indexes:
            self.plot[i[0]][1].remove(i[1])



def mainFunc():
    A = hungry_bean('a', 3, 1, 1)
    B = hungry_bean('b', 2.6, 1, 1)

    for x in range(11):
        bean.reproduce(A, B)
    #a = field('a', 10, 10)
    #a.randomPopulation(.2)
    #a.beanPopulate(bean.getBeans())

    #print(a)
    #print(A.getX(), A.getY())
    #print(A.pathFind(a))

    C = hungry_bean('c', 1, 1, 1)
    c = field('c', 20, 20)
    c.randomPopulation(.002)
    c.beanPopulate([C])
    print(C.getPos())
    while C.nextSquare(c, hungry_bean.pathFind) != C.getPos():
        print(c)
        print(C.getPos())
        c.moveBean(C, C.nextSquare(c, hungry_bean.pathFind))
    #print(c)

def animation():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    image = logo

    pygame.display.set_icon(logo)
    pygame.display.set_caption('test')


    screen = pygame.display.set_mode((400, 400))
    screen.fill((0,120,255))
    screen.blit(image, (240-32,180-32))

    C = bozo_bean('c', 1, 1, 1, stomach=1)
    A = bozo_bean('a', 1, 1, 1, stomach=1)
    c = field('c', 20, 20)
    c.randomPopulation(.01)
    c.controlledHouse([(10,10)])
    c.beanPopulate(bean.aliveInstances)
    count = 0
    playing = True
    while playing:
        if count == 100:
            count = 0
        if count%25 == 0:
            c.randomPopulation(.002)
        c.display(screen)
        for individualBean in bean.aliveInstances:
            c.moveBean(individualBean, individualBean.nextSquare(c, type(individualBean).pathFind))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    playing = False
                    pygame.quit()
                    #sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    break
        c.beanEat(bean.aliveInstances)
        c.beanReproduce(bean.aliveInstances)
        count += 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

animation()