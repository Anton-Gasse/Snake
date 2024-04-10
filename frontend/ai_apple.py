import pygame
from apple import Apple

class AI_Apple(Apple):

    def __init__(self, x_pos: int, y_pos: int, screen: pygame.Surface) -> None:
        super().__init__(x_pos, y_pos, screen)
        self.image = pygame.image.load("utils/ai_apple.png").convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)