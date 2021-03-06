class Player:
    def __init__(self,x,y,worldRef,fg=(255,0,255)) -> None:
        self.x=x
        self.y=y
        self.worldRef = worldRef
        self.fg=fg

    def move(self,dx,dy) -> None:
        moveCheck = True
        for o in self.worldRef.objects:
            if o.x == self.x+dx and o.y == self.y+dy:
                moveCheck = False
                break

        if moveCheck:
            self.x+=dx
            self.y+=dy
