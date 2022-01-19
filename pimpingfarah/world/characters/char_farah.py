from world.characters.base_character import BaseCharacter


class CharFarah(BaseCharacter):
    def __init__(self,x,y,desc='A dark skinned woman in her 40s with a voluptous figure, dressed in robes.'):
        super().__init__(x=x,y=y,char='F',fg=(185,120,55),name='Farah',desc=desc)