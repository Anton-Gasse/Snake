import pygame
from tail import Snake_Tail

class AI_Snake_Tail(Snake_Tail):

    def __init__(self, x_pos: int, y_pos: int, facing: int, speed: int) -> None:
        super().__init__(x_pos, y_pos, facing, speed)
        if self.facing == "up" or self.facing == "down":
            self.image = pygame.image.load("utils/ai_snake_tail_top_down.png").convert_alpha()
        elif self.facing == "right" or self.facing == "left":
            self.image = pygame.image.load("utils/ai_snake_tail_left_right.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)


    def set_direction(self, facing:str) -> None:
        """
        Sets the facing direction of the ai snake tail segment and updates its image accordingly.

        Parameters:
            facing (str): The new direction in which the tail segment should face ('up', 'down', 'left', 'right').
        """
        self.facing = facing
        if self.facing == "up" or self.facing == "down":    
            self.image = pygame.image.load("utils/ai_snake_tail_top_down.png").convert_alpha()
        
        elif self.facing == "right" or self.facing == "left":
            self.image = pygame.image.load("utils/ai_snake_tail_left_right.png").convert_alpha()
        
        self.image.set_colorkey((127, 127, 127))