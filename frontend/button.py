import pygame
from pygame.sprite import AbstractGroup

class Button(pygame.sprite.Sprite):

    def __init__(self, x_pos:int, y_pos:int, screen:pygame.Surface, image_path:str) -> None:
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey((127, 127, 127))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)

    
    def draw(self) -> None:
        """
        Draws the button on the screen.
        """
        self.screen.blit(self.image, self.rect)