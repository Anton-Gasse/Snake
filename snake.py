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
    def __init__(self, x_pos:int, y_pos:int, screen:pygame.Surface) -> None:
        """
        Initializes a Snake_Head object.

        Parameters:
            x_pos (int): The x-coordinate position of the snake head on the screen.
            y_pos (int): The y-coordinate position of the snake head on the screen.
            screen (pygame.Surface): The surface where the snake head will be drawn.
        """
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tails = pygame.sprite.Group()
        self.facing = "up"
        self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        self.screen = screen
        self.speed = 5


    def add_tail(self) -> None:
        """
        Adds a tail to the snake.
        """
        if self.tails.sprites() == []:
            if self.facing == "up":            
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos + 25, "up", self.speed))
            
            elif self.facing == "down":
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos - 25, "down", self.speed))
            elif self.facing == "right":            
                self.tails.add(Snake_Tail(self.x_pos - 25, self.y_pos, "right", self.speed))
            elif self.facing == "left":        
                self.tails.add(Snake_Tail(self.x_pos + 25, self.y_pos, "left", self.speed))
        else:
            if self.tails.sprites()[-1].get_direction() == "up":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] + 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "down":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] - 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "right":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] - 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "left":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] + 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
    
    
    def check_tails(self) -> None:
        """
        Checks the tails of the snake and adjusts their directions accordingly.
        """
        if self.x_pos % 25 == 0 and self.y_pos % 25 == 0:
            tail:Snake_Tail
            for i, tail in enumerate(self.tails):
                if i == 0:                   
                    tail.set_direction(self.compare_tails(tail.get_pos()[0], tail.get_pos()[1], self.x_pos, self.y_pos))                                        
                else:
                    tail.set_direction(self.compare_tails(tail.get_pos()[0], tail.get_pos()[1] , self.tails.sprites()[i-1].get_pos()[0], self.tails.sprites()[i-1].get_pos()[1]))
                    

    def compare_tails(self, x1:int, y1:int, x2:int, y2:int) -> str: 
        """
        Compares the positions of two points and determines the direction from the second to the first point.

        Parameters:
            x1 (int): The x-coordinate of the first point.
            y1 (int): The y-coordinate of the first point.
            x2 (int): The x-coordinate of the second point.
            y2 (int): The y-coordinate of the second point.

        Returns:
            str: The direction from the second point to the first point.
        """
        if x1 == x2 and y1 < y2:
            return "down"
        if x1 == x2 and y1 > y2:
            return "up"    
        if x1 < x2 and y1 == y2:
            return "right"
        if x1 > x2 and y1 == y2:
            return "left"
    

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
        self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey("white")


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
    