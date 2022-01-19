from world.tile import Tile
from world.object import Object
from world.characters.char_farah import CharFarah
import random
import math

class World:
    def __init__(self) -> None:
        self.tiles =[]
        self.objects = []
        self.characters = []

        self.createPlaceholder()
    def createWall(self,x1,y1, x2,y2):
        vx = x2-x1
        vy = y2-y1
        vs = math.sqrt((vx*vx)+(vy*vy))
        vx/=vs
        vy/=vs

        if vx < vy:
            vy/=vy
            vx/=vy
            for y in range(y1,y2):
                valY = y - y1
                x = x1 + math.floor(valY*vx)
                self.objects.append(Object(x,y,True,'A wall','#'))
        else:
            vy/=vx
            vx/=vx
            for x in range(x1,x2):
                valX = x - x1
                y = y1 + math.floor(valX*vy)
                self.objects.append(Object(x,y,True,'A wall','#'))
        
    def createPlaceholder(self) -> None:
        for i in range(-25,100):
            for j in range(-25,100):
                self.tiles.append(Tile(i,j,'.' if random.randint(0,1) else ',', 'Floor'))

        
        self.createWall(5,5,15,5)
        self.createWall(15,5,15,15)
        self.createWall(5,15,15,15)

        self.characters.append(CharFarah(x=12,y=12))
    
    def update(self) -> None:
        for obj in self.objects:
            obj.update()
        for char in self.characters:
            char.update()

    