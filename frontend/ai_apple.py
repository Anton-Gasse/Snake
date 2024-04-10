import pygame
from apple import Apple

class AI_Apple(Apple):
    """
    A class representing an AI apple object.

    Attributes:
        x_pos (int): The x-coordinate position of the apple on the screen.
        y_pos (int): The y-coordinate position of the apple on the screen.
        screen (pygame.Surface): The surface where the apple will be drawn.
        image (pygame.Surface): The image representing the apple.
        rect (pygame.Rect): The rectangular area occupied by the apple image on the screen.
    """

    def __init__(self, x_pos: int, y_pos: int, screen: pygame.Surface) -> None:
        super().__init__(x_pos, y_pos, screen)
        self.image = pygame.image.load("utils/ai_apple.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)