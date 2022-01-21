import random

class TalkingManager:
    def __init__(self) -> None:
        self.talking = False
        self.selectedOption = 0
        self.currentNodeId = "1"
        self.currentNode={}

        #Test conversation. Move to json structure later
        self.currentConversation = {
            "1": {"unique":True, "author":"MC", "phrases":["Hey, are you okay Miss?"],"options":[],"nextnode":"2"},
            "2": {"unique":True, "author":"MC", "phrases":["..."],"options":[],"nextnode":"3"},
            "3": {"unique":True, "author":"MC", "phrases":["...Hello?"],"options":[],"nextnode":"4"},
            "4": {"unique":True, "author":"Farah", "phrases":["...Ah... what happened..? Where am i?"],"options":[
                {"label":"You're at Blue street, are you alright?", "command":"addTrust", "commandarg":1, "nextnode":"5"},
                {"label":"Get up bitch!", "command":"addTrust", "commandarg":-1, "nextnode":"6"},]
            },
            "5": {"unique":True, "author":"Farah", "phrases":["... What? What is this strange city?","...Blue street? Are we in Thebes?"],"options":[],"nextnode":"7"},
            "6": {"unique":True, "author":"Farah", "phrases":["...!","Ah..! Don't yell at me, please!"],"options":[],"nextnode":"7"},

            "7": {"unique":True, "author":"Farah", "phrases":["Ah.. I'm sorry ... I don't know how I got here..."],"options":[],"nextnode":"8"},
            "8": {"unique":True, "author":"", "phrases":["Woman tries to stand up, swaying side to side like she's about to faint, not noticing one of her breasts hanging outside of her dress."],"options":[
                {"label":"Help her get up", "command":"addTrust", "commandarg":1, "nextnode":"-1"},
                {"label":"Stand your ground", "command":"addFear", "commandarg":1, "nextnode":"-1"}]
            }
        }

    def update(self):
        if self.currentNodeId == "-1":
            self.stopTalking()
        try:
            assert self.currentNodeId in self.currentConversation
        except AssertionError as e:
            e.args += (self.currentConversation,self.currentNodeId)
            raise
        self.currentNode = self.currentConversation[self.currentNodeId]
        if self.selectedOption>len(self.currentNode["options"])-1:
            self.selectedOption = 0
        elif self.selectedOption <0:
            self.selectedOption = len(self.currentNode["options"])-1

    def generatePhrase(self):
        return (self.currentNode["author"] + ": " if self.currentNode["author"] != "" else "")  + self.currentNode["phrases"][random.randint(0,len(self.currentNode["phrases"])-1)]

    def getCurrentPhrase(self):
        if "phrase" in self.currentNode:
            return self.currentNode["phrase"]
        else:
            return self.currentNode["phrases"][0]

    def getCurrentChoices(self):
        return self.currentNode["options"]

    def talk(self):
        if len(self.currentNode["options"])>0:
            self.currentNodeId = self.currentNode["options"][self.selectedOption]["nextnode"]
        else:
            self.currentNodeId = self.currentNode["nextnode"]

        self.update()
        self.currentNode["phrase"] = self.generatePhrase()

    def stopTalking(self):
        self.talking = False
        self.optionChoice = 0
        self.currentNodeId = "1"
        self.currentNode={}

    


    