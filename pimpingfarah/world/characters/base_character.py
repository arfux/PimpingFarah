from world.object import Object

class BaseCharacter(Object):
    def __init__(self,char,x,y,fg,name,desc='Unknown person') -> None:
        super().__init__(x=x,y=y,collidable=False,char=char,fg=fg,desc=desc)
        self.name = name