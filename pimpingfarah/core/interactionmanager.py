from world.world import World
import math

class InteractionManager:
    def __init__(self,world,player) -> None:
        self.player = player
        self.world = world
        self.interacting = False
        self.interactionIdx = 0
        self.actions = []
        self.currentInteraction = "interactionChoice"
        self.interactions = {
            "interactionChoice": {
                "name" : "Interact",
                "id":"interactionChoice",
                "options":[{"id":"talkTo","label":"Talk to"},{"id":"lookAt","label":"Look at"}]
            },
            "talkTo": {
                "name" : "Talk to",
                "id":"talkTo",
                "final":"true",
                "options" : [],
            },
            "lookAt": {
                "name" : "Talk to",
                "id":"talkTo",
                "final":"true",
                "options" : [],
            },
        }

    def getCurrentInteraction(self)-> None:
        return self.interactions[self.currentInteraction]

    def update(self) -> None:
        
        self.clampInteractionIdx()
        if len(self.interactions[self.currentInteraction]["options"])>0:
            self.selectedOption = self.interactions[self.currentInteraction]["options"][self.interactionIdx]

        self.updateTalkTo()
        
    def updateTalkTo(self):
        self.interactions["talkTo"]["options"] = []
        for char in self.world.characters:        
            if abs(self.player.x - char.x) <=2 and abs(self.player.y - char.y)<=2:
                self.interactions["talkTo"]["options"].append(char.name)
    
    def clampInteractionIdx(self)-> None:
        if self.interactionIdx > len(self.interactions[self.currentInteraction]["options"])-1:
            self.interactionIdx = 0
        elif self.interactionIdx < 0:
            self.interactionIdx = len(self.interactions[self.currentInteraction]["options"])-1


    def isCurrentInteractionFinal(self):
        return "final" in self.interactions[self.currentInteraction]

    def action(self, action,option):
        self.actions.append({"action":action, "option":option})


    def click(self) -> None:

        #Switch current interaction
        if not self.isCurrentInteractionFinal():
                assert self.currentInteraction in self.interactions
                self.interactionIdx=0
                self.currentInteraction=self.selectedOption["id"]
        else:
            self.action(self.currentInteraction,self.selectedOption)

    def reset(self) -> None:
        self.interacting = False
        self.currentInteraction = "interactionChoice"



    