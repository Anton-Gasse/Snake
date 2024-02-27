import pygame

class Apple(pygame.sprite.Sprite):
    """
    A class representing an apple object.

    Attributes:
        x_pos (int): The x-coordinate position of the apple on the screen.
        y_pos (int): The y-coordinate position of the apple on the screen.
        screen (pygame.Surface): The surface where the apple will be drawn.
        image (pygame.Surface): The image representing the apple.
        rect (pygame.Rect): The rectangular area occupied by the apple image on the screen.
    """
    def __init__(self, x_pos:int, y_pos:int, screen:pygame.Surface) -> None:
        """
        Initializes an Apple object.

        Parameters:
            x_pos (int): The x-coordinate position of the apple on the screen.
            y_pos (int): The y-coordinate position of the apple on the screen.
            screen (pygame.Surface): The surface where the apple will be drawn.
        """
        super().__init__()
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load("utils/apple.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)

        
    def draw(self) -> None:
        """
        Draws the apple on the screen.
        """
        self.screen.blit(self.image, self.rect)