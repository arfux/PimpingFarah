from core.rendering.renderer import Renderer
from core.rendering.sprite import Sprite
from world.world import World
from core.player import Player
from core.eventmanager import EventManager
from core.interactionmanager import InteractionManager
from core.talkingmanager import TalkingManager
from core.actions import Action, EscapeAction, MovementAction, InteractionAction
from ui.narrator import Narrator

import tcod

class Game:
    def __init__(self) -> None:
        self.narrator = Narrator()
        self.world = World()
        self.player = Player(4,18,self.world)
        self.talkingmanager = TalkingManager()
        self.interactionmanager = InteractionManager(self.world,self.player)
        self.mode = "inperson"
        self.renderer = Renderer(self.narrator,self.interactionmanager, self.talkingmanager)
        self.running = True
        self.eventManager = EventManager()
        self.testSpr = Sprite(25,25,153,169,self.renderer.getTexture('test'))

    def start(self) -> None:
        while self.running:
            self.update()

    def setMode(self,mode) -> None:
        self.mode = mode
        self.renderer.mode =mode

    def updateActions(self) -> None:
        for action in self.interactionmanager.actions:
            print(action)
            if action["action"] == "talkTo":
                print("Talking now!")
                self.talkingmanager.talking = True
                self.interactionmanager.reset()

        self.interactionmanager.actions.clear()

    def update(self) -> None:

        for event in tcod.event.wait(timeout=0.001):
            action = self.eventManager.dispatch(event)

            if action is None:
                continue
            
            if isinstance(action,MovementAction):
                if self.talkingmanager.talking:
                    self.talkingmanager.selectedOption+=action.dy
                else:
                    if self.interactionmanager.interacting:
                        self.interactionmanager.interactionIdx+=action.dy
                    else:
                        self.player.move(action.dx,action.dy)
                

            elif isinstance(action,EscapeAction):
                if self.interactionmanager.interacting:
                    self.interactionmanager.reset()
                else:
                    raise SystemExit()

            elif isinstance(action,InteractionAction):
                if self.talkingmanager.talking:
                    print("talking")
                    self.talkingmanager.talk()
                else:
                    print("not talking")
                    if not self.interactionmanager.interacting:
                        self.interactionmanager.interacting = True
                    else:
                        self.interactionmanager.click()
                

        self.interactionmanager.update()
        self.talkingmanager.update()

        if self.narrator.displaying:
            self.narrator.update()
        

        
        self.updateActions()
        
        self.renderer.updateCamera(self.player)

        for t in self.world.tiles:
            self.renderer.drawTile(t)
        for o in self.world.objects:
            self.renderer.drawObject(o)
        for c in self.world.characters:
            self.renderer.drawCharacter(c)

        self.renderer.drawSprite(self.testSpr)
        self.renderer.drawChar(self.player.x,self.player.y,'@',fg=self.player.fg)

        self.renderer.drawUI()
        
        self.renderer.render()
