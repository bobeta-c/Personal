import random

class bean:
    
    instances = []
    aliveInstances = []
    names = []
    def __init__(self, name, height, weight, fertility, parent1 = None, parent2 = None, posX = None, posY = None):
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
        bean.aliveInstances.append(self)
        bean.updateInstances()
    def getX(self):
        return self.posX
    def getY(self):
        return self.posY
    def getPos(self):
        return (self.posX, self.posY)
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
    def reproduce(bean1, bean2, name = None):
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
            return (bean(newname, newheight, newweight, newfertility, bean1, bean2))
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
        if goalLoc[0] != self.getX():
            if goalLoc[0] < self.getX():
                return (self.getX()-1,self.getY())
            return (self.getX()+1, self.getY())
        elif goalLoc[1] != self.getY():
            if goalLoc[1] < self.getY():
                return (self.getX(), self.getY()-1)
            return (self.getX(),self.getY()+1)
        return (self.getX(),self.getY())

class hungry_bean(bean):
    def pathFind(self, field):
        closest = None
        location = None
        for x in field.plot:
            if field.plot[x][0] >= 1:
                dist = ((x[0]-self.getX())**2 + (x[1]-self.getY())**2)**(1/2)
                if (not closest) or dist < closest:
                    closest = dist
                    location = x
        return location
            
class field:
    def __init__(self, name, sizeX, sizeY):
        self.name = name
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.plot = {}
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.plot[(x, y)] = [0, []]
    def randomPopulation(self, percentChance = .3):
        for x in self.plot:
            if (random.random() <= percentChance):
                self.plot[x][0] = 1
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
        return string
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
        self.updateLocs(beans)
    def moveBean(self, beanUsed, newPos):
        beanUsed.posX = newPos[0]
        beanUsed.posY = newPos[1]
        self.updateLocs([beanUsed])
    def updateLocs(self, beans):
        for x in beans:
            if not x in self.plot[(x.posX, x.posY)][1]:
                self.plot[x.posX, x.posY][1].append(x)
        
        for x in self.plot:
            for y in range(len(self.plot[x][1])):
                if issubclass(type(self.plot[x][1][y]), bean) and self.plot[x][1][y].getPos() != x:  
                    self.plot[x][1].remove(y)


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
c = field('c', 5, 5)
c.randomPopulation(.2)
c.beanPopulate([C])
print(c)
#print(issubclass(type(C), bean))
print(C.getPos())
print(C.pathFind(c))
print(C.nextSquare(c, hungry_bean.pathFind))

print("\n\n")
c.moveBean(C, C.nextSquare(c, hungry_bean.pathFind))
print(c)
print(C.getPos())
