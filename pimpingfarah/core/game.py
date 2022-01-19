from core.rendering.renderer import Renderer
from core.rendering.sprite import Sprite
from world.world import World
from core.player import Player
from core.eventmanager import EventManager
from core.actions import Action, EscapeAction, MovementAction, InteractionAction
from ui.narrator import Narrator

import tcod

class Game:
    def __init__(self) -> None:
        self.narrator = Narrator()
        self.renderer = Renderer(self.narrator)
        self.world = World()
        self.running = True
        self.player = Player(4,18,self.world)
        self.eventManager = EventManager()
        self.testSpr = Sprite(25,25,500,500,self.renderer.getTexture('test'))

    def start(self) -> None:
        while self.running:
            self.update()

    def update(self) -> None:

        for event in tcod.event.wait(timeout=0.001):
            action = self.eventManager.dispatch(event)

            if action is None:
                continue
            
            if isinstance(action,MovementAction) and not self.narrator.displaying:
                self.player.move(action.dx,action.dy)
                

            elif isinstance(action,EscapeAction):
                raise SystemExit()

            elif isinstance(action,InteractionAction):
                #test
                if self.narrator.displaying:
                    self.narrator.clear()
                else:
                    self.narrator.narrate("You see suddenly a bright line from the alleyway, it casting shadows from nearby trash cans and lamposts. It blinds you for a few seconds, and once you can see again, it is gone.")

        if self.narrator.displaying:
            self.narrator.update()
        
        self.renderer.updateCamera(self.player)

        for t in self.world.tiles:
            self.renderer.drawTile(t)
        for o in self.world.objects:
            self.renderer.drawObject(o)
        for c in self.world.characters:
            self.renderer.drawCharacter(c)

        self.renderer.drawSprite(self.testSpr)
        self.renderer.drawChar(self.player.x,self.player.y,'@',fg=self.player.fg)
        self.testSpr.setPosition(self.testSpr.getPosition()[0]+1,self.testSpr.getPosition()[1])

        self.renderer.drawUI()
        
        self.renderer.render()
