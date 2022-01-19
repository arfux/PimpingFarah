class Tile:
    def __init__(self,x,y,char,desc,fg=(255,255,255)) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.desc = desc
        self.fg=fg
    