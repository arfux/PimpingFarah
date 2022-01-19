import tcod

class Sprite:
    def __init__(self,x=0,y=0,w=0,h=0,tex=tcod.ffi.NULL) -> None:
        self.__x = y
        self.__y = x
        self.__w = w
        self.__h = h
        self.rect=tcod.ffi.new("SDL_Rect*", (x,y,w,h))
        self.texture=tex

    def setPosition(self,x,y) -> None:
        self.__x=x
        self.__y=y
        self.rect.x=x
        self.rect.y=y

    def setSize(self,w,h) -> None:
        self.__w = w
        self.__h = h
        self.rect.w = w
        self.rect.h = h
    
    def getSize(self):
        return (self.__w,self.__h)

    def getPosition(self):
        return (self.__x,self.__y)

    def getRect(self):
        return self.rect

    def getTexture(self):
        return self.texture