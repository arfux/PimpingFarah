from core.rendering.renderer import Renderer
from world.world import World
from core.player import Player
from core.eventmanager import EventManager
from core.actions import Action, EscapeAction, MovementAction
import tcod

class Game:
    def __init__(self) -> None:
        self.renderer = Renderer()
        self.world = World()
        self.running = True
        self.player = Player(5,25,self.world)
        self.eventManager = EventManager()

    def start(self) -> None:
        while self.running:
            self.update()

    def update(self) -> None:
        for event in tcod.event.wait():
            action = self.eventManager.dispatch(event)

            if action is None:
                continue
            
            if isinstance(action,MovementAction):
                self.player.move(action.dx,action.dy)
                

            elif isinstance(action,EscapeAction):
                raise SystemExit()

        self.renderer.updateCamera(self.player)

        for t in self.world.tiles:
            self.renderer.drawTile(t)
        for o in self.world.objects:
            self.renderer.drawObject(o)
        self.renderer.drawChar(self.player.x,self.player.y,'@')

        self.renderer.drawUI()
        
        self.renderer.render()
