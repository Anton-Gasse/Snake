import pygame
from tail import Snake_Tail

class Snake_Head(pygame.sprite.Sprite):
    """
    A class representing the head of the snake.

    Attributes:
        x_pos (int): The x-coordinate position of the snake head on the screen.
        y_pos (int): The y-coordinate position of the snake head on the screen.
        screen (pygame.Surface): The surface where the snake head will be drawn.
        tails (pygame.sprite.Group): A group containing all the snake tails.
        facing (str): The direction the snake head is facing.
        image (pygame.Surface): The image representing the snake head.
        rect (pygame.Rect): The rectangular area occupied by the snake head image on the screen.
        speed (int): The speed at which the snake moves.
    """
    def __init__(self, x_pos:int, y_pos:int, screen:pygame.Surface, ai:bool) -> None:
        """
        Initializes a Snake_Head object.

        Parameters:
            x_pos (int): The x-coordinate position of the snake head on the screen.
            y_pos (int): The y-coordinate position of the snake head on the screen.
            screen (pygame.Surface): The surface where the snake head will be drawn.
            ai (bool): Determines if the snake head will be controlled by an ai
        """
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tails = pygame.sprite.Group()
        self.facing = "up"
        self.ai = ai
        if self.ai:
            self.image = pygame.image.load(f"utils/ai_snake_head_{self.facing}.png").convert_alpha()
        else:
            self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        self.screen = screen
        self.speed = 6.25


    def add_tail(self) -> None:
        """
        Adds a tail to the snake.
        """
        if self.tails.sprites() == []:
            if self.facing == "up":            
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos + 25, "up", self.speed, ai=self.ai))
            
            elif self.facing == "down":
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos - 25, "down", self.speed, ai=self.ai))
            elif self.facing == "right":            
                self.tails.add(Snake_Tail(self.x_pos - 25, self.y_pos, "right", self.speed, ai=self.ai))
            elif self.facing == "left":        
                self.tails.add(Snake_Tail(self.x_pos + 25, self.y_pos, "left", self.speed, ai=self.ai))
        else:
            if self.tails.sprites()[-1].get_direction() == "up":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] + 25, self.tails.sprites()[-1].get_direction(), self.speed, ai=self.ai))
            elif self.tails.sprites()[-1].get_direction() == "down":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] - 25, self.tails.sprites()[-1].get_direction(), self.speed, ai=self.ai))
            elif self.tails.sprites()[-1].get_direction() == "right":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] - 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed, ai=self.ai))
            elif self.tails.sprites()[-1].get_direction() == "left":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] + 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed, ai=self.ai))
    
    
    def check_tails(self) -> None:
        """
        Checks the tails of the snake and adjusts their directions accordingly.
        """
        if self.x_pos % 25 == 0 and self.y_pos % 25 == 0:
            tail:Snake_Tail
            for i, tail in enumerate(self.get_tails().sprites()[::-1]):
                if i == len(self.tails)-1:                   
                    tail.set_direction(self.facing)                                        
                else:
                    tail.set_direction(self.get_tails().sprites()[::-1][i+1].get_direction())
                

    def move(self) -> None:
        """
        Moves the snake head and its tails according to its current direction.
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
        for tail in self.tails:
            tail.move()


    def set_facing(self, facing:str) -> None:
        """
        Sets the facing direction of the snake head.

        Parameters:
            facing (str): The direction the snake head will face.
        """
        self.facing = facing
        if self.ai:
            self.image = pygame.image.load(f"utils/ai_snake_head_{self.facing}.png").convert_alpha()
        else:
            self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))


    def draw(self) -> None:
        """
        Draws the snake head and its tails on the screen.
        """
        self.tails.draw(self.screen)
        self.screen.blit(self.image, self.rect)
        

    def get_pos(self) -> tuple[int, int]:
        """
        Returns the current position of the snake head.

        Returns:
            tuple: The x and y coordinates of the snake head.
        """
        return (self.x_pos, self.y_pos)
    

    def get_tails(self) -> pygame.sprite.Group:
        """
        Returns the group of tails attached to the snake head.

        Returns:
            pygame.sprite.Group: The group of snake tails.
        """
        return self.tails
    

    def set_pos(self, x, y) -> None:
        """
        Sets the x and y position of the snake head
        """
        self.x_pos = x
        self.y_pos = y
        self.rect.topleft = (self.x_pos, self.y_pos) 