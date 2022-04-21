'''

World Generation Test :)
lets see what works!

'''
import math
from PIL import Image

class Block(object):
            
    def __init__(self, name, color):
        self.color = color
        self.name = name
    def getColor(self):
        return self.color
    def __str__(self):
        return '[{}]'.format(self.color)

class World(object):
    def __init__(self, width, height, base):
        self.width = width
        self.height = height
        self.base = base
        self.blockDict = {}
        self.widthRange = range(math.floor(-width/2), math.ceil(width/2))
        for x in self.widthRange:
            for y in range(height):
                self.blockDict[(x, y)] = base
    
    def represent(self):
        for y in reversed(range(0, self.height)):
            print('\n')
            for x in self.widthRange:
                print(self.blockDict[(x, y)], x, y, end = ' ')
                    
    def setBlock(self, x, y, block):
        self.blockDict[(x, y)] = block
    def getCorners(self):
        return ((self.widthRange[0], 0), (self.widthRange[0], self.height-1), (self.widthRange[-1], 0), (self.widthRange[-1], self.height-1))

class Player(object):
    pass


grass = Block('grass','green')
dirt = Block('dirt','brown')
air = Block('air','clear')
world1 = World(12, 5, dirt)