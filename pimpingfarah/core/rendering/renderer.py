import tcod
import math

WIDTH,HEIGHT = 80,48
BOTTOM_UI_HEIGHT = 10
SIDE_UI_WIDTH = 20
TOP_UI_BAR_HEIGHT = 1

class Renderer:
    def __init__(self) -> None:
        self.context = tcod.context.new(columns=WIDTH,rows=HEIGHT)
        self.console = self.context.new_console(order="F")
        self.cameraX = 0
        self.cameraY = 0

    def updateCamera(self,player) -> None:
        self.cameraX = player.x - math.floor(WIDTH/2)
        self.cameraY = player.y - math.floor(HEIGHT/2)

    def viewportCheck(self,x,y) -> bool:
        if (y-self.cameraY)<HEIGHT-BOTTOM_UI_HEIGHT and (x-self.cameraX)<WIDTH-SIDE_UI_WIDTH and (y-self.cameraY)>=TOP_UI_BAR_HEIGHT:
            return True
        else:
             return False

    def drawChar(self,x,y,char) -> None:
        if self.viewportCheck(x,y):
            self.console.print(x=(x-self.cameraX),y=(y-self.cameraY),string=char)

    def drawTile(self, tile) -> None:
        self.drawChar(x=tile.x,y=tile.y,char=tile.char)

    def drawObject(self,obj) -> None:
        self.drawChar(x=obj.x,y=obj.y,char=obj.char)

    def drawUI(self) -> None:
        #Game title

        for y in range (0,HEIGHT):
            self.console.print(WIDTH-SIDE_UI_WIDTH,y,'║')
        self.console.print(math.floor(WIDTH/3)*2, 0,"Pimping Farah v0.1")
        

    def render(self) -> None:
        self.context.present(self.console)
        self.console.clear()


