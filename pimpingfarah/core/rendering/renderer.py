import tcod
import math
from ui.narrator import Narrator
from core.interactionmanager import InteractionManager
from core.talkingmanager import TalkingManager
from core.rendering.texturemanager import TextureManager
from core.rendering.sprite import Sprite
import pygame
from sdl2 import *
import imageio as iio


WIDTH,HEIGHT = 80,48
BOTTOM_UI_HEIGHT = 10
SIDE_UI_WIDTH = 20
TOP_UI_BAR_HEIGHT = 1

class Renderer:
    def __init__(self, narrator: Narrator, interactionManager: InteractionManager, talkingmanager: TalkingManager) -> None:
        self.context = tcod.context.new(columns=WIDTH,rows=HEIGHT,renderer=tcod.context.RENDERER_SDL2)
        self.console = self.context.new_console(order="F")
        self.cameraX = 0
        self.cameraY = 0
        self.narrator = narrator
        self.sdlRenderer = tcod.lib.SDL_GetRenderer(self.context.sdl_window_p)
        self.texMgr = TextureManager(self.sdlRenderer)
        self.texMgr.loadTexture('pimpingfarah/assets/test.png','test')
        self.spritesToDraw = []
        self.interactionManager = interactionManager
        self.talkingmanager = talkingmanager

    def getTexture(self,tex):
        return self.texMgr.texDictionary[tex]

    def updateCamera(self,player) -> None:
        self.cameraX = player.x - math.floor(WIDTH/2)
        self.cameraY = player.y - math.floor(HEIGHT/2)

    def viewportCheck(self,x,y) -> bool:
        if (x-self.cameraX)<WIDTH-SIDE_UI_WIDTH and (y-self.cameraY)>=TOP_UI_BAR_HEIGHT:
            return True
        else:
             return False

    def drawChar(self,x,y,char,fg=(255,255,255)) -> None:
        if self.viewportCheck(x,y):
            self.console.print(x=(x-self.cameraX),y=(y-self.cameraY),string=char,fg=fg)

    def drawTile(self, tile) -> None:
        self.drawChar(x=tile.x,y=tile.y,char=tile.char,fg=tile.fg)

    def drawObject(self,obj) -> None:
        self.drawChar(x=obj.x,y=obj.y,char=obj.char,fg=obj.fg)

    def drawCharacter(self,chara) -> None:
        self.drawChar(x=chara.x,y=chara.y,char=chara.char,fg=chara.fg)

    def drawSprite(self,spr) -> None:
        self.spritesToDraw.append(spr)
        
    def printInteractionBox(self,interaction='normal') -> None:
        interBox = (math.floor(WIDTH/2) -10,math.floor(HEIGHT/2)-10,20,20)

        if self.interactionManager.interacting:
            match self.interactionManager.currentInteraction:
                
                case _:
                    self.console.print_frame(interBox[0],interBox[1],interBox[2],interBox[3],self.interactionManager.getCurrentInteraction()["name"])
                    actions = self.interactionManager.interactions[self.interactionManager.currentInteraction]["options"]
                    for idx,action in enumerate(actions):
                        label = action["label"] if "label" in action else action
                        bg = (0,0,0) if idx != self.interactionManager.interactionIdx else (255,255,255)
                        fg = (0,0,0) if idx == self.interactionManager.interactionIdx else (255,255,255)
                        self.console.print(interBox[0]+1,interBox[1]+1+idx, ("E" if not idx else str(idx)), fg=(125,0,125), bg=bg)
                        self.console.print(interBox[0]+2,interBox[1]+1+idx, label,fg=fg,bg=bg)

    def printTalkingBox(self) -> None:
        talkBox = (math.floor(WIDTH/2) -25,math.floor(HEIGHT/2)-10,50,20)

        if self.talkingmanager.talking:
                
            self.console.print_frame(talkBox[0],talkBox[1],talkBox[2],talkBox[3],"Talking")
            self.console.print_box(talkBox[0]+1,talkBox[1]+1,talkBox[2],talkBox[3], self.talkingmanager.getCurrentPhrase())
            self.console.hline(talkBox[0]+1,talkBox[1]+10,48,20)
            for idx,option in enumerate(self.talkingmanager.currentNode["options"]):
                bg = (0,0,0) if idx != self.talkingmanager.selectedOption else (255,255,255)
                fg = (0,0,0) if idx == self.talkingmanager.selectedOption else (255,255,255)
                self.console.print(talkBox[0]+1,talkBox[1]+11+idx, option["label"],fg=fg,bg=bg)



    def drawUI(self) -> None:
        #Game title
        self.console.vline(WIDTH-SIDE_UI_WIDTH,0,HEIGHT)
        self.console.print(math.floor(WIDTH-SIDE_UI_WIDTH + (SIDE_UI_WIDTH/2)), 0,"Pimping Farah v0.1",bg=(25,0,25), alignment=tcod.CENTER)

        if self.narrator.displaying:
            self.console.print_frame(0,HEIGHT-BOTTOM_UI_HEIGHT,WIDTH-SIDE_UI_WIDTH,BOTTOM_UI_HEIGHT)
            self.console.print_box(1,HEIGHT-BOTTOM_UI_HEIGHT+1,WIDTH-SIDE_UI_WIDTH-2,BOTTOM_UI_HEIGHT-2, self.narrator.textToDraw)
        
        if self.interactionManager.interacting:
            self.printInteractionBox()
        
        if self.talkingmanager.talking:
            self.printTalkingBox()
        


    def render(self) -> None:
        
        tcod.lib.SDL_RenderClear( self.sdlRenderer )
        self.context._context_p.c_accumulate_(self.context._context_p,self.console.console_c,tcod.ffi.NULL)
        for spr in self.spritesToDraw:
            tcod.lib.SDL_RenderCopy(self.sdlRenderer,spr.getTexture(),tcod.ffi.NULL, spr.getRect())
        self.spritesToDraw.clear()
        tcod.lib.SDL_RenderPresent(self.sdlRenderer)
        self.console.clear()




