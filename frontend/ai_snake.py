import pygame
from snake import Snake_Head
from ai_tail import AI_Snake_Tail

class AI_Snake_Head(Snake_Head):

    def __init__(self, x_pos: int, y_pos: int, screen: pygame.Surface) -> None:
        super().__init__(x_pos, y_pos, screen)
        self.image = pygame.image.load(f"utils/ai_snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        

    def add_tail(self) -> None:
        """
        Adds a tail to the ai snake.
        """
        if self.tails.sprites() == []:
            if self.facing == "up":            
                self.tails.add(AI_Snake_Tail(self.x_pos, self.y_pos + 25, "up", self.speed))
            elif self.facing == "down":
                self.tails.add(AI_Snake_Tail(self.x_pos, self.y_pos - 25, "down", self.speed))
            elif self.facing == "right":            
                self.tails.add(AI_Snake_Tail(self.x_pos - 25, self.y_pos, "right", self.speed))
            elif self.facing == "left":        
                self.tails.add(AI_Snake_Tail(self.x_pos + 25, self.y_pos, "left", self.speed))
        else:
            if self.tails.sprites()[-1].get_direction() == "up":
                self.tails.add(AI_Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] + 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "down":
                self.tails.add(AI_Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] - 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "right":
                self.tails.add(AI_Snake_Tail(self.tails.sprites()[-1].get_pos()[0] - 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "left":
                self.tails.add(AI_Snake_Tail(self.tails.sprites()[-1].get_pos()[0] + 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
    

    def set_facing(self, facing:str) -> None:
        """
        Sets the facing direction of the snake head.

        Parameters:
            facing (str): The direction the snake head will face.
        """
        self.facing = facing
        self.image = pygame.image.load(f"utils/ai_snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))