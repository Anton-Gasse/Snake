import pygame

class Snake_Tail(pygame.sprite.Sprite):
    """
    A class representing a segment of the snake's tail.

    Attributes:
        x_pos (int): The x-coordinate position of the snake tail segment.
        y_pos (int): The y-coordinate position of the snake tail segment.
        facing (str): The direction in which the tail segment is facing ('up', 'down', 'left', 'right').
        speed (int): The speed at which the tail segment moves.
        image (pygame.Surface): The image representing the snake tail segment.
        rect (pygame.Rect): The rectangular area occupied by the snake tail segment image on the screen.
    """

    def __init__(self, x_pos:int, y_pos:int, facing:int, speed:int) -> None:
        """
        Initializes a Snake_Tail object.

        Parameters:
            x_pos (int): The x-coordinate position of the snake tail segment.
            y_pos (int): The y-coordinate position of the snake tail segment.
            facing (str): The direction in which the tail segment is facing ('up', 'down', 'left', 'right').
            speed (int): The speed at which the tail segment moves.
        """
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = facing

        if self.facing == "up" or self.facing == "down":
            self.image = pygame.image.load("utils/snake_tail_top_down.png").convert_alpha()
        elif self.facing == "right" or self.facing == "left":
            self.image = pygame.image.load("utils/snake_tail_left_right.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)
        self.speed = speed
    
    
    def get_pos(self) -> tuple[int, int]:
        """
        Returns the current position of the snake tail segment.

        Returns:
            tuple: A tuple containing the x and y coordinates of the snake tail segment.
        """
        return (self.x_pos, self.y_pos)
    

    def move(self) -> None:
        """
        Moves the snake tail segment based on its current facing direction and speed.
        """
        if self.facing == "up":
            self.y_pos -= self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)                           
        elif self.facing == "down":
            self.y_pos += self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)            
        elif self.facing == "right":
            self.x_pos += self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)                
        elif self.facing == "left":
            self.x_pos -= self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)


    def get_direction(self) -> str:
        """
        Returns the current facing direction of the snake tail segment.

        Returns:
            str: The direction in which the tail segment is facing ('up', 'down', 'left', 'right').
        """
        return self.facing
    

    def set_direction(self, facing:str) -> None:
        """
        Sets the facing direction of the snake tail segment and updates its image accordingly.

        Parameters:
            facing (str): The new direction in which the tail segment should face ('up', 'down', 'left', 'right').
        """
        self.facing = facing
        if self.facing == "up" or self.facing == "down":
            self.image = pygame.image.load("utils/snake_tail_top_down.png").convert_alpha()
        
        elif self.facing == "right" or self.facing == "left":
            self.image = pygame.image.load("utils/snake_tail_left_right.png").convert_alpha()
        
        self.image.set_colorkey((127, 127, 127))
    
    def set_pos(self, x:int, y:int) -> None:
        """
        Sets the x and y position of the tail
        """
        self.x_pos = x
        self.y_pos = y
        self.rect.topleft = (self.x_pos, self.y_pos) 