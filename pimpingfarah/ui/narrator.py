import time

class Narrator:
    def __init__(self) -> None:
        self.displaying = False
        self.lastScrollTime = time.time()
        self.scrollCharTime = 0.015
        self.scrollChars = 0
        self.scrollText = ''
        self.textToDraw = ''
    
    def update(self) -> None:
        if time.time() - self.lastScrollTime > self.scrollCharTime:
            self.lastScrollTime = time.time()
            self.scrollChars+=1

        self.textToDraw = self.scrollText[0:self.scrollChars]

    def narrate(self, string) -> None:
        self.scrollText = string
        self.displaying = True

    def clear(self) -> None:
        self.scrollText = ''
        self.textToDraw = ''
        self.displaying = False
        self.scrollChars = 0