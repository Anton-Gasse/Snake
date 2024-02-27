import pygame

class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("utils/border.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def get_pos(self):
        return self.rect.topleft